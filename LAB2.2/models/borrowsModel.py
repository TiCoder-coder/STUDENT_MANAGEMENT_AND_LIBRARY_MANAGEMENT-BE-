from datetime import datetime, date
from enums.enums import BookStatus

# CLASS BORROW: DUNG DE QUAN LY THONG TIN MUON/TRA SACH -------------------------------------------------------------
class Borrow:
    
    # Khoi tao cac thuoc tinh cho Borrrow
    def __init__(self, member_id, book_id, borrow_date=None, due_date=None, return_date=None, borrow_id=None):
        self.borrow_id = borrow_id
        self.member_id = member_id
        self.book_id = book_id
        # Neu khong truyen borrow_date -> mac đinh la ngay hien tai
        self.borrow_date = borrow_date or date.today().strftime("%Y-%m-%d")
        # due_date bat buôc nen truyen khi tao; mac đinh None đe linh hoat
        self.due_date = due_date
        self.return_date = return_date

    # Ham helper: parse input (str/date) -> date object
    @staticmethod
    def _to_date(d):
        if d is None:
            return None
        if isinstance(d, date):
            return d
        # neu truyen datetime
        if isinstance(d, datetime):
            return d.date()
        # parse tU string yyyy-mm-dd hoac yyyy-mm-dd HH:MM:SS
        try:
            # Try full datetime first
            dt = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
            return dt.date()
        except Exception:
            try:
                dt = datetime.strptime(d, "%Y-%m-%d")
                return dt.date()
            except Exception:
                return None

    # Ham dung de them mot borrow (muon sach) ---------------------------------------------------------------------------------
    def add_borrow(self, db):
        try:
            # Kiem tra borrow_id --- Neu ton tai -> False
            if self.borrow_id:
                existing = db.fetch_one("SELECT * FROM borrows WHERE borrow_id=%s", (self.borrow_id,))
                if existing:
                    return "[ERROR] Borrow ID already exists."

            # Kiem tra memberId co ton tai khong --- Neu co -> Dung
            member = db.fetch_one("SELECT * FROM members WHERE member_id=%s", (self.member_id,))
            if not member:
                return "[ERROR] Member ID not found."

            # Kiem tra bookId xem co ton tai khong --- Neu co -> Dung
            book = db.fetch_one("SELECT * FROM books WHERE book_id=%s", (self.book_id,))
            if not book:
                return "[ERROR] Book ID not found."

            # Kiem tra sach co dang o trang thai available khong
            # Nếu status != available -> loi
            if int(book.get("status", 0)) != BookStatus.AVAILABLE.value:
                return "[ERROR] Book is not available for borrowing."

            # Kiem tra ngay
            b_date = self._to_date(self.borrow_date)
            if b_date is None:
                return "[ERROR] Invalid borrow_date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS."

            today = date.today()
            if b_date > today:
                return "[ERROR] borrow_date cannot be in the future."

            if not self.due_date:
                return "[ERROR] due_date is required."
            d_date = self._to_date(self.due_date)
            if d_date is None:
                return "[ERROR] Invalid due_date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS."

            if d_date <= today:
                return "[ERROR] due_date must be greater than current date."

            # Ngay muon <= Ngay tra <= Ngay doi
            if self.return_date:
                r_date = self._to_date(self.return_date)
                if r_date is None:
                    return "[ERROR] Invalid return_date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS."
                if not (b_date <= r_date <= d_date):
                    return "[ERROR] return_date must be between borrow_date and due_date."

            # Them vao database
            sql = """
                INSERT INTO borrows (member_id, book_id, borrow_date, due_date, return_date)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                int(self.member_id),
                int(self.book_id),
                b_date.strftime("%Y-%m-%d"),
                d_date.strftime("%Y-%m-%d"),
                self.return_date and self._to_date(self.return_date).strftime("%Y-%m-%d") or None
            )
            db.execute_query(sql, params)

            # Neu muon thi cap nhap lai trang thai cua sach la da muon
            db.execute_query("UPDATE books SET status=%s WHERE book_id=%s", (BookStatus.BORROWED.value, int(self.book_id)))

            return "[SUCCESS] Borrow record added successfully!"
        except Exception as e:
            return f"[ERROR] Failed to add borrow: {e}"

    # Ham dung de tim kiem cac ban ghi borrows theo cac tieu chi ----------------------------------------------------------------
    @staticmethod
    def search_borrows(db, borrow_id=None, member_id=None, book_id=None, overdue_only=False):
        try:
            sql = "SELECT b.*, m.name as member_name, bo.title as book_title FROM borrows b " \
                  "LEFT JOIN members m ON b.member_id = m.member_id " \
                  "LEFT JOIN books bo ON b.book_id = bo.book_id WHERE "
            params, conditions = [], []

            # Borrrow_id
            if borrow_id:
                conditions.append("b.borrow_id=%s")
                params.append(borrow_id)
            
            # Member_id
            if member_id:
                conditions.append("b.member_id=%s")
                params.append(member_id)
            
            # Book_id
            if book_id:
                conditions.append("b.book_id=%s")
                params.append(book_id)

            # Due
            if overdue_only:
                conditions.append("b.return_date IS NULL AND b.due_date < %s")
                params.append(date.today().strftime("%Y-%m-%d"))

            if not conditions:
                return []

            sql += " OR ".join(conditions)
            return db.fetch_all(sql, tuple(params))
        except Exception:
            return []

    # Ham dung de lay tat ca cac borrows -------------------------------------------------------------------------------------
    @staticmethod
    def get_all_borrows(db):
        try:
            sql = "SELECT b.*, m.name as member_name, bo.title as book_title FROM borrows b " \
                  "LEFT JOIN members m ON b.member_id = m.member_id " \
                  "LEFT JOIN books bo ON b.book_id = bo.book_id " \
                  "ORDER BY b.borrow_date DESC"
            return db.fetch_all(sql)
        except Exception:
            return []

    # Ham dung de cap nhat thong tin borrow (vd: thay doi due_date, return_date) ------------------------------------------------
    @staticmethod
    def update_borrow(db, borrow_id, member_id=None, book_id=None, borrow_date=None, due_date=None, return_date=None):
        try:
            # Kiem tra xem borrow co ton tai khong
            existing = db.fetch_one("SELECT * FROM borrows WHERE borrow_id=%s", (borrow_id,))
            if not existing:
                return "[ERROR] Borrow ID not found."

            # Neu đoi book_id -> kiem tra book tôn tai & phai co trang thai AVAILABLE (tru khi book_id bang book hien tai)
            if book_id is not None and int(book_id) != int(existing["book_id"]):
                new_book = db.fetch_one("SELECT * FROM books WHERE book_id=%s", (book_id,))
                if not new_book:
                    return "[ERROR] New Book ID not found."
                if int(new_book.get("status", 0)) != BookStatus.AVAILABLE.value:
                    return "[ERROR] New book is not available for borrowing."

            # 3) Neu đoi member_id -> kiem tra ton tai
            if member_id is not None:
                mem = db.fetch_one("SELECT * FROM members WHERE member_id=%s", (member_id,))
                if not mem:
                    return "[ERROR] Member ID not found."

            # Kiem tra ngay hop le neu nhap vao
            b_date = Borrow._to_date(borrow_date) if borrow_date else Borrow._to_date(existing.get("borrow_date"))
            d_date = Borrow._to_date(due_date) if due_date else Borrow._to_date(existing.get("due_date"))
            r_date = Borrow._to_date(return_date) if return_date else Borrow._to_date(existing.get("return_date"))

            if b_date is None:
                return "[ERROR] Invalid borrow_date."
            if d_date is None:
                return "[ERROR] Invalid due_date."
            today = date.today()
            if b_date > today:
                return "[ERROR] borrow_date cannot be in the future."
            if d_date <= today:
                return "[ERROR] due_date must be greater than current date."
            if r_date:
                if not (b_date <= r_date <= d_date):
                    return "[ERROR] return_date must be between borrow_date and due_date."

            # Neu co thong tin can cap nhap thi luu tru vao 2 list va cap nhap 1 lan
            fields, params = [], []
            if member_id is not None:
                fields.append("member_id=%s"); params.append(int(member_id))
            if book_id is not None:
                fields.append("book_id=%s"); params.append(int(book_id))
            if borrow_date is not None:
                fields.append("borrow_date=%s"); params.append(b_date.strftime("%Y-%m-%d"))
            if due_date is not None:
                fields.append("due_date=%s"); params.append(d_date.strftime("%Y-%m-%d"))
            if return_date is not None:
                fields.append("return_date=%s"); params.append(r_date.strftime("%Y-%m-%d"))

            if not fields:
                return "[INFO] No fields to update."

            sql = f"UPDATE borrows SET {', '.join(fields)} WHERE borrow_id=%s"
            params.append(borrow_id)
            db.execute_query(sql, tuple(params))

            if book_id is not None and int(book_id) != int(existing["book_id"]):
                # old book -> available
                db.execute_query("UPDATE books SET status=%s WHERE book_id=%s", (BookStatus.AVAILABLE.value, int(existing["book_id"])))
                # new book -> borrowed
                db.execute_query("UPDATE books SET status=%s WHERE book_id=%s", (BookStatus.BORROWED.value, int(book_id)))

            # Neu set return_date (nguoi tre) -> cap nhap trang thai sach -> AVAILABLE
            if return_date is not None:
                db.execute_query("UPDATE books SET status=%s WHERE book_id=%s", (BookStatus.AVAILABLE.value, int(existing["book_id"] if book_id is None else book_id)))

            return "[SUCCESS] Borrow updated successfully!"
        except Exception as e:
            return f"[ERROR] Failed to update borrow: {e}"

    # Ham dung de tra sach (set return_date) ----------------------------------------------------------------------------------
    @staticmethod
    def return_book(db, borrow_id, return_date=None):
        try:
            rec = db.fetch_one("SELECT * FROM borrows WHERE borrow_id=%s", (borrow_id,))
            if not rec:
                return "[ERROR] Borrow ID not found."

            # parse return_date, default = today
            r_date = Borrow._to_date(return_date) if return_date else date.today()
            if r_date is None:
                return "[ERROR] Invalid return_date format."

            b_date = Borrow._to_date(rec.get("borrow_date"))
            d_date = Borrow._to_date(rec.get("due_date"))

            # return_date phai nam trong khoang [borrow_date, due_date]
            if not (b_date <= r_date <= d_date):
                
                # Neu tra sau due_date -> thong bao qua han nhung van cho phep cap nhap return_date
                if r_date > d_date:
                    
                    # Cập nhật return_date nhưng trả về cảnh báo quá hạn
                    db.execute_query("UPDATE borrows SET return_date=%s WHERE borrow_id=%s", (r_date.strftime("%Y-%m-%d"), borrow_id))
                    # Cap nhap return_date nhung tra ve canh bao qua han
                    db.execute_query("UPDATE books SET status=%s WHERE book_id=%s", (BookStatus.AVAILABLE.value, int(rec["book_id"])))
                    return "[INFO] Book returned but was overdue. Please handle fines/notifications."
                else:
                    return "[ERROR] return_date must be on or after borrow_date."

            # Neu hop le -> cap nhap return_date va trang thai sach
            db.execute_query("UPDATE borrows SET return_date=%s WHERE borrow_id=%s", (r_date.strftime("%Y-%m-%d"), borrow_id))
            db.execute_query("UPDATE books SET status=%s WHERE book_id=%s", (BookStatus.AVAILABLE.value, int(rec["book_id"])))

            return "[SUCCESS] Book returned successfully!"
        except Exception as e:
            return f"[ERROR] Failed to return book: {e}"

    # Ham dung de xoa borrow theo borrow_id ----------------------------------------------------------------------------------
    @staticmethod
    def delete_borrow(db, borrow_id):
        try:
            rec = db.fetch_one("SELECT * FROM borrows WHERE borrow_id=%s", (borrow_id,))
            if not rec:
                return False

            # Neu sach chua đươc tra (return_date IS NULL) -> khi xoa can cap nhap trang thai sach ve AVAILABLE
            if rec.get("return_date") is None:
                db.execute_query("UPDATE books SET status=%s WHERE book_id=%s", (BookStatus.AVAILABLE.value, int(rec["book_id"])))

            db.execute_query("DELETE FROM borrows WHERE borrow_id=%s", (borrow_id,))
            return True
        except Exception:
            return False
