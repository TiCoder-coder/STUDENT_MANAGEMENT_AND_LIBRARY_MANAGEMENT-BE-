# models/borrowsModel.py
from datetime import datetime, date
from enums.enums import BookStatus

# CLASS BORROW: DÙNG ĐỂ QUẢN LÝ THÔNG TIN MƯỢN/TRẢ SÁCH -------------------------------------------------------------
class Borrow:
    """
    Borrow model quản lý bảng borrows.
    Các phương thức tuân theo convention trả về:
      - "[SUCCESS] ..." hoặc "[ERROR] ..." cho các thao tác CRUD,
      - True/False cho các hàm xóa/không thành công,
      - danh sách dict cho các truy vấn.
    """

    def __init__(self, member_id, book_id, borrow_date=None, due_date=None, return_date=None, borrow_id=None):
        self.borrow_id = borrow_id
        self.member_id = member_id
        self.book_id = book_id
        # Nếu không truyền borrow_date -> mặc định là ngày hiện tại
        self.borrow_date = borrow_date or date.today().strftime("%Y-%m-%d")
        # due_date bắt buộc nên truyền khi tạo; nhưng vẫn cho mặc định None để linh hoạt
        self.due_date = due_date
        self.return_date = return_date

    # Hàm helper: parse input (str/date) -> date object
    @staticmethod
    def _to_date(d):
        if d is None:
            return None
        if isinstance(d, date):
            return d
        # nếu truyền datetime
        if isinstance(d, datetime):
            return d.date()
        # cố gắng parse từ string yyyy-mm-dd hoặc yyyy-mm-dd HH:MM:SS
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
            # 1) Kiểm tra borrow_id (nếu có) đã tồn tại chưa
            if self.borrow_id:
                existing = db.fetch_one("SELECT * FROM borrows WHERE borrow_id=%s", (self.borrow_id,))
                if existing:
                    return "[ERROR] Borrow ID already exists."

            # 2) Kiểm tra member_id tồn tại
            member = db.fetch_one("SELECT * FROM members WHERE member_id=%s", (self.member_id,))
            if not member:
                return "[ERROR] Member ID not found."

            # 3) Kiểm tra book_id tồn tại
            book = db.fetch_one("SELECT * FROM books WHERE book_id=%s", (self.book_id,))
            if not book:
                return "[ERROR] Book ID not found."

            # 4) Kiểm tra sách hiện có trạng thái có sẵn (AVAILABLE)
            # Nếu status != AVAILABLE -> lỗi (đã bị mượn hoặc trạng thái khác)
            if int(book.get("status", 0)) != BookStatus.AVAILABLE.value:
                return "[ERROR] Book is not available for borrowing."

            # 5) Kiểm tra ngày (borrow_date, due_date)
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

            # 6) Nếu return_date được cung cấp (không bắt buộc khi tạo borrow), kiểm tra nằm trong khoảng
            if self.return_date:
                r_date = self._to_date(self.return_date)
                if r_date is None:
                    return "[ERROR] Invalid return_date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS."
                if not (b_date <= r_date <= d_date):
                    return "[ERROR] return_date must be between borrow_date and due_date."

            # 7) Thêm bản ghi borrow vào DB
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

            # 8) Cập nhật trạng thái sách -> BORROWED
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

            if borrow_id:
                conditions.append("b.borrow_id=%s")
                params.append(borrow_id)
            if member_id:
                conditions.append("b.member_id=%s")
                params.append(member_id)
            if book_id:
                conditions.append("b.book_id=%s")
                params.append(book_id)

            if overdue_only:
                # Borrows with no return_date and due_date < today
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
            # 1) Kiểm tra tồn tại borrow
            existing = db.fetch_one("SELECT * FROM borrows WHERE borrow_id=%s", (borrow_id,))
            if not existing:
                return "[ERROR] Borrow ID not found."

            # 2) Nếu đổi book_id -> kiểm tra book tồn tại & phải có trạng thái AVAILABLE (trừ khi book_id bằng book hiện tại)
            if book_id is not None and int(book_id) != int(existing["book_id"]):
                new_book = db.fetch_one("SELECT * FROM books WHERE book_id=%s", (book_id,))
                if not new_book:
                    return "[ERROR] New Book ID not found."
                if int(new_book.get("status", 0)) != BookStatus.AVAILABLE.value:
                    return "[ERROR] New book is not available for borrowing."

            # 3) Nếu đổi member_id -> kiểm tra tồn tại
            if member_id is not None:
                mem = db.fetch_one("SELECT * FROM members WHERE member_id=%s", (member_id,))
                if not mem:
                    return "[ERROR] Member ID not found."

            # 4) Kiểm tra ngày hợp lệ nếu có truyền
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

            # 5) Build update fields
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

            # 6) Nếu đổi book_id thì cần cập nhật trạng thái sách cũ -> AVAILABLE, sách mới -> BORROWED
            if book_id is not None and int(book_id) != int(existing["book_id"]):
                # old book -> available
                db.execute_query("UPDATE books SET status=%s WHERE book_id=%s", (BookStatus.AVAILABLE.value, int(existing["book_id"])))
                # new book -> borrowed
                db.execute_query("UPDATE books SET status=%s WHERE book_id=%s", (BookStatus.BORROWED.value, int(book_id)))

            # 7) Nếu set return_date (người trả) -> cập nhật trạng thái sách -> AVAILABLE
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

            # return_date phải nằm trong khoảng [borrow_date, due_date]
            if not (b_date <= r_date <= d_date):
                # Nếu trả sau due_date -> thông báo quá hạn nhưng vẫn cho phép cập nhật return_date
                if r_date > d_date:
                    # Cập nhật return_date nhưng trả về cảnh báo quá hạn
                    db.execute_query("UPDATE borrows SET return_date=%s WHERE borrow_id=%s", (r_date.strftime("%Y-%m-%d"), borrow_id))
                    # Cập nhật trạng thái sách -> AVAILABLE
                    db.execute_query("UPDATE books SET status=%s WHERE book_id=%s", (BookStatus.AVAILABLE.value, int(rec["book_id"])))
                    return "[INFO] Book returned but was overdue. Please handle fines/notifications."
                else:
                    return "[ERROR] return_date must be on or after borrow_date."

            # Nếu hợp lệ -> cập nhật return_date và trạng thái sách
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

            # Nếu sách chưa được trả (return_date IS NULL) -> khi xóa cần cập nhật trạng thái sách về AVAILABLE
            if rec.get("return_date") is None:
                db.execute_query("UPDATE books SET status=%s WHERE book_id=%s", (BookStatus.AVAILABLE.value, int(rec["book_id"])))

            db.execute_query("DELETE FROM borrows WHERE borrow_id=%s", (borrow_id,))
            return True
        except Exception:
            return False
