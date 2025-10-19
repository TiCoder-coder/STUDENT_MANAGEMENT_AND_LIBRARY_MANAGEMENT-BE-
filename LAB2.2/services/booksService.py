from models.booksModel import Book
from enums.enums import BookStatus, BookType, EducationLevel
from auth import require_manager  # Khai bao mot ham trong auth dung de kiem tra quyen truy cap (manager/admin)

class BookService:
    def __init__(self, db):
        self.db = db

    # Dung de them mot book vao he thong  --- Chi co manager moi duoc tao
    def add_book(self, data: dict):
        try:
            # Kiem tra quyen co phai la admin/manager khong
            try:
                require_manager()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            # Chuan hoa lai cac input
            title = data.get("title")
            author = data.get("author")
            pages = data.get("pages")
            publish_year = data.get("publish_year")
            book_type = data.get("book_type")
            status = data.get("status", BookStatus.AVAILABLE)
            genre = data.get("genre")
            subject = data.get("subject")
            level = data.get("level")
            field = data.get("field")
            book_id = data.get("book_id")
            created_at = data.get("created_at")

            # Basic normalization
            title = title.strip().title() if isinstance(title, str) else title
            author = author.strip().title() if isinstance(author, str) else author

            # pages / publish_year -> int (neu co)
            try:
                if pages is not None and pages != "":
                    pages = int(pages)
            except Exception:
                print("[VALIDATION] 'pages' must be an integer.")
                return

            try:
                if publish_year is not None and publish_year != "":
                    publish_year = int(publish_year)
            except Exception:
                print("[VALIDATION] 'publish_year' must be an integer.")
                return

            # Neu view truyen enum (BookType, BookStatus), giu nguyen; neu truyen object enum value, model xu ly.
            # Tao object Book va goi model.add_book
            book = Book(
                title=title,
                author=author,
                pages=pages,
                publish_year=publish_year,
                book_type=book_type,
                status=status,
                genre=genre,
                subject=subject,
                level=level,
                field=field,
                created_at=created_at,
                book_id=book_id
            )

            result = book.add_book(self.db)
            print(result)
            return result

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to add book: {e}")

    # Tra va danh sach cac cuon sach
    def get_all_books(self):
        try:
            return Book.get_all_books(self.db)
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to fetch books: {e}")
            return []

    # Su dung lai ham get_all_books nhung dinh dang lai kieu in ra cho dep hon
    def list_books(self):
        try:
            rows = Book.get_all_books(self.db)
            if not rows:
                print("[INFO] No books found.")
                return

            print("\n{:<5} {:<25} {:<20} {:<10} {:<12} {:<10} {:<10} {:<15}".format(
                "ID", "Title", "Author", "Pages", "Year", "Type", "Status", "Created_At"
            ))
            print("-" * 115)

            for r in rows:
                if isinstance(r, dict):
                    book_id = r.get("book_id")
                    title = r.get("title")
                    author = r.get("author")
                    pages = r.get("pages")
                    year = r.get("publish_year")
                    book_type = r.get("book_type")
                    status = r.get("status")
                    created_at = r.get("created_at")
                else:
                    # tuple fallback
                    book_id, title, author, pages, year, status, book_type, created_at = r[:8]

                print("{:<5} {:<25} {:<20} {:<10} {:<12} {:<10} {:<10} {:<15}".format(
                    str(book_id), str(title), str(author), str(pages), str(year),
                    str(book_type), str(status), str(created_at)
                ))
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to list books: {e}")

    # Ham dung de tim kiem mot cuon sach
    def search_books(self, filters: dict):
        try:
            book_id = filters.get("book_id")
            title = filters.get("title")
            author = filters.get("author")
            book_type = filters.get("book_type")
            status = filters.get("status")

            results = Book.search_books(
                self.db,
                book_id=book_id,
                title=title,
                author=author,
                book_type=book_type,
                status=status
            )

            return results or []

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to search books: {e}")
            return []

    # Ham dung de update mot cuon sach --- Chi co manager moi duoc cap nhap
    def update_book(self, book_id: str, data: dict):
        try:
            try:
                require_manager()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            result = Book.update_book(
                self.db,
                book_id,
                title=data.get("title"),
                author=data.get("author"),
                pages=data.get("pages"),
                publish_year=data.get("publish_year"),
                book_type=data.get("book_type"),
                status=data.get("status"),
                genre=data.get("genre"),
                subject=data.get("subject"),
                level=data.get("level"),
                field=data.get("field")
            )
            print(result)
            return result

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to update book: {e}")

    # Ham dung de delete mot cuon sach --- Chi co manager moi duoc xoa
    def delete_book(self, book_id: str):
        try:
            try:
                require_manager()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            success = Book.delete_book(self.db, book_id)
            if success:
                print("[SUCCESS] Book deleted successfully.")
            else:
                print("[ERROR] Book ID not found.")
            return success
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to delete book: {e}")
            return False
