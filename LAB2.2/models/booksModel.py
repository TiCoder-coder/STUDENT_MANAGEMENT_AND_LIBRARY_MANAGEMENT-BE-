from datetime import datetime
from enums.enums import BookStatus, BookType, EducationLevel

# CLASS BOOK: DÙNG ĐỂ QUẢN LÝ THÔNG TIN CỦA CÁC CUỐN SÁCH --------------------------------------------------------------
class Book:

    def __init__(self, title, author, pages, publish_year,
                 book_type, status=BookStatus.AVAILABLE,
                 genre=None, subject=None, level=None, field=None,
                 created_at=None, book_id=None):
        # Các thuộc tính cơ bản của sách
        self.book_id = book_id
        self.title = title
        self.author = author
        self.pages = pages
        self.publish_year = publish_year

        self.book_type = book_type
        self.status = status

        self.genre = genre        # cho novel
        self.subject = subject    # cho textbook
        self.level = level        # cho textbook (primary/secondary/highschool)
        self.field = field        # cho science

        # Tự động tạo created_at nếu không có
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ham dung de them mot book vao database ---------------------------------------------------------------------------------
    def add_book(self, db):
        try:
            # 1) Validate book_id (nếu có) xem da ton tai chua
            if self.book_id:
                existing = db.fetch_one("SELECT * FROM books WHERE book_id=%s", (self.book_id,))
                if existing:
                    return "[ERROR] Book ID already exists."

            # 2) Validate pages > 0
            try:
                if int(self.pages) <= 0:
                    return "[ERROR] Pages must be greater than 0."
            except Exception:
                return "[ERROR] Pages must be an integer greater than 0."

            # 3) Validate publish_year <= current year
            current_year = datetime.now().year
            try:
                if int(self.publish_year) > current_year:
                    return f"[ERROR] publish_year cannot be greater than current year ({current_year})."
            except Exception:
                return "[ERROR] publish_year must be an integer."

            # 4) Validate book_type using enums
            bt_value = None
            if isinstance(self.book_type, BookType):
                bt_value = self.book_type.value
            else:
                # allow passing string like 'novel'
                try:
                    bt_value = BookType(self.book_type).value
                except Exception:
                    # try map from string
                    valid = [e.value for e in BookType]
                    return f"[ERROR] Invalid book_type. Valid types: {valid}"

            # 5) Validate status using enums
            st_value = None
            if isinstance(self.status, BookStatus):
                st_value = self.status.value
            else:
                # allow integer or string that maps to enum name/value
                if isinstance(self.status, int):
                    if self.status in [s.value for s in BookStatus]:
                        st_value = self.status
                    else:
                        return f"[ERROR] Invalid status. Valid statuses: {[s.value for s in BookStatus]}"
                else:
                    # maybe user passed enum name like 'AVAILABLE'
                    try:
                        st_value = BookStatus[self.status].value
                    except Exception:
                        return f"[ERROR] Invalid status. Valid statuses: {[s.value for s in BookStatus]}"

            # 6) Validate level if provided (must be in EducationLevel)
            level_value = None
            if self.level:
                if isinstance(self.level, EducationLevel):
                    level_value = self.level.value
                else:
                    try:
                        level_value = EducationLevel(self.level).value
                    except Exception:
                        valid_levels = [e.value for e in EducationLevel]
                        return f"[ERROR] Invalid level. Valid levels: {valid_levels}"

            # 7) Prepare SQL INSERT (chỉ insert các cột phù hợp)
            sql = """
                INSERT INTO books
                (title, author, pages, publish_year, status, book_type, genre, subject, level, field, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self.title,
                self.author,
                int(self.pages),
                int(self.publish_year),
                int(st_value),
                bt_value,
                self.genre,
                self.subject,
                level_value,
                self.field,
                self.created_at
            )

            db.execute_query(sql, params)
            return "[SUCCESS] Book added successfully!"
        except Exception as e:
            return f"[ERROR] Failed to add book: {e}"

    # Ham dung de tim kiem thong tin sach theo cac tieu chi (id, title, author, type, status) -------------------------------
        # Ham dung de tim kiem thong tin sach theo cac tieu chi (id, title, author, type, status) -------------------------------
    @staticmethod
    def search_books(db, book_id=None, title=None, author=None, book_type=None, status=None):
        try:
            sql = "SELECT * FROM books WHERE 1=1"
            params = []

            if book_id:
                sql += " AND book_id=%s"
                params.append(book_id)

            if title:
                title = title.strip().lower()
                sql += " AND LOWER(title) LIKE %s"
                params.append(f"%{title}%")

            if author:
                author = author.strip().lower()
                sql += " AND LOWER(author) LIKE %s"
                params.append(f"%{author}%")

            if book_type:
                book_type = book_type.strip().lower()
                try:
                    bt_val = BookType(book_type).value if not isinstance(book_type, BookType) else book_type.value
                    sql += " AND book_type=%s"
                    params.append(bt_val)
                except Exception:
                    valid = [e.value for e in BookType]
                    print(f"[VALIDATION] Invalid book_type. Valid types: {valid}")
                    return []

            if status is not None and status != "":
                try:
                    st_val = status.value if isinstance(status, BookStatus) else int(status)
                    if st_val not in [s.value for s in BookStatus]:
                        print(f"[VALIDATION] Invalid status. Valid statuses: {[s.value for s in BookStatus]}")
                        return []
                    sql += " AND status=%s"
                    params.append(st_val)
                except Exception:
                    print("[VALIDATION] Invalid status format.")
                    return []

            # Thực thi truy vấn
            return db.fetch_all(sql, tuple(params))
        except Exception as e:
            print(f"[MODEL ERROR] search_books failed: {e}")
            return []


    # Ham dung de lay tat ca cac sach ---------------------------------------------------------------------------------------
    @staticmethod
    def get_all_books(db):
        try:
            return db.fetch_all("SELECT * FROM books ORDER BY created_at DESC")
        except Exception:
            return []

    # Ham dung de cap nhat thong tin sach theo book_id -----------------------------------------------------------------------
    @staticmethod
    def update_book(db, book_id, title=None, author=None, pages=None, publish_year=None,
                    book_type=None, status=None, genre=None, subject=None, level=None, field=None):
        try:
            # Kiem tra book ton tai
            existing = db.fetch_one("SELECT * FROM books WHERE book_id=%s", (book_id,))
            if not existing:
                return "[ERROR] Book ID not found."

            fields, params = [], []

            if title:
                fields.append("title=%s")
                params.append(title)
            if author:
                fields.append("author=%s")
                params.append(author)
            if pages is not None:
                try:
                    if int(pages) <= 0:
                        return "[ERROR] Pages must be greater than 0."
                    fields.append("pages=%s")
                    params.append(int(pages))
                except Exception:
                    return "[ERROR] Pages must be an integer greater than 0."
            if publish_year is not None:
                try:
                    current_year = datetime.now().year
                    if int(publish_year) > current_year:
                        return f"[ERROR] publish_year cannot be greater than current year ({current_year})."
                    fields.append("publish_year=%s")
                    params.append(int(publish_year))
                except Exception:
                    return "[ERROR] publish_year must be an integer."

            if book_type:
                try:
                    bt_val = book_type.value if isinstance(book_type, BookType) else BookType(book_type).value
                    fields.append("book_type=%s")
                    params.append(bt_val)
                except Exception:
                    valid = [e.value for e in BookType]
                    return f"[ERROR] Invalid book_type. Valid types: {valid}"

            if status is not None:
                # status can be enum or int
                try:
                    if isinstance(status, BookStatus):
                        st_val = status.value
                    else:
                        st_val = int(status)
                    if st_val not in [s.value for s in BookStatus]:
                        return f"[ERROR] Invalid status. Valid statuses: {[s.value for s in BookStatus]}"
                    fields.append("status=%s")
                    params.append(st_val)
                except Exception:
                    return f"[ERROR] Invalid status value."

            if genre is not None:
                fields.append("genre=%s")
                params.append(genre)
            if subject is not None:
                fields.append("subject=%s")
                params.append(subject)
            if level is not None:
                try:
                    lvl_val = level.value if isinstance(level, EducationLevel) else EducationLevel(level).value
                    fields.append("level=%s")
                    params.append(lvl_val)
                except Exception:
                    valid_levels = [e.value for e in EducationLevel]
                    return f"[ERROR] Invalid level. Valid levels: {valid_levels}"
            if field is not None:
                fields.append("field=%s")
                params.append(field)

            if not fields:
                return "[INFO] No fields to update."

            # Thuc hien cap nhat
            sql = f"UPDATE books SET {', '.join(fields)} WHERE book_id=%s"
            params.append(book_id)
            db.execute_query(sql, tuple(params))
            return "[SUCCESS] Book updated successfully!"
        except Exception as e:
            return f"[ERROR] Failed to update book: {e}"

    # Ham dung de xoa sach theo book_id -------------------------------------------------------------------------------------
    @staticmethod
    def delete_book(db, book_id):
        try:
            # Kiem tra ton tai
            existing = db.fetch_one("SELECT * FROM books WHERE book_id=%s", (book_id,))
            if not existing:
                return False

            db.execute_query("DELETE FROM books WHERE book_id=%s", (book_id,))
            return True
        except Exception:
            return False
