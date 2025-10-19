from models.borrowsModel import Borrow
from auth import require_manager  # Goi ham kiem tra quyen (chi manager duoc muon/tra sach)

# CLASS BORROWSSERVICE: GỌI LẠI CÁC HÀM CỦA MODEL VÀ THỰC THI NÓ CÓ KIỂM TRA QUYỀN -----------------------------
class BorrowsService:

    # Khoi tao service
    def __init__(self, db):
        self.db = db

    # Ham dung de tao ra mot borrow, ham nay se goi lai ham tao o model va them phan quyen  --- Chi co manager moi duoc tao
    def add_borrow(self, data: dict):
        try:
            # Kiem tra quyen truy cap
            try:
                require_manager()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            # Kiem tra du lieu dau vao
            member_id = data.get("member_id")
            book_id = data.get("book_id")
            borrow_date = data.get("borrow_date")
            due_date = data.get("due_date")
            return_date = data.get("return_date")

            if not member_id or not book_id or not due_date:
                print("[VALIDATION ERROR] member_id, book_id, and due_date are required.")
                return

            # Tao mot doi tuong borrow voi cac thong tin o tren de them vao db
            borrow = Borrow(
                member_id=member_id,
                book_id=book_id,
                borrow_date=borrow_date,
                due_date=due_date,
                return_date=return_date
            )

            # Goi ham o service de thuc thi
            result = borrow.add_borrow(self.db)
            print(result)

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to add borrow: {e}")

    # Ham dung de tim kiem mot cuon sach ham nay se goi lai search_borrows o model
    def search_borrows(self, borrow_id=None, member_id=None, book_id=None, overdue_only=False):
        try:
            if not any([borrow_id, member_id, book_id, overdue_only]):
                print("[INFO] Please provide at least one search condition.")
                return

            results = Borrow.search_borrows(
                self.db, borrow_id=borrow_id,
                member_id=member_id,
                book_id=book_id,
                overdue_only=overdue_only
            )

            if not results:
                print("[INFO] No borrow records found.")
                return

            # In ra cac headler de dep hon
            print("\n{:<10} {:<10} {:<10} {:<12} {:<12} {:<12} {:<15} {:<15}".format(
                "BorrowID", "MemberID", "BookID", "BorrowDate", "DueDate", "ReturnDate", "MemberName", "BookTitle"
            ))
            print("-" * 95)

            for r in results:
                borrow_id = r.get("borrow_id", "-")
                member_id = r.get("member_id", "-")
                book_id = r.get("book_id", "-")
                borrow_date = str(r.get("borrow_date") or "-")
                due_date = str(r.get("due_date") or "-")
                return_date = str(r.get("return_date") or "-")
                member_name = r.get("member_name", "-")
                book_title = r.get("book_title", "-")

                print("{:<10} {:<10} {:<10} {:<12} {:<12} {:<12} {:<15} {:<15}".format(
                    borrow_id, member_id, book_id, borrow_date, due_date, return_date, member_name, book_title
                ))

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to search borrows: {e}")

    # Ham dung de lay tat ca thong tin cua borrow 
    def list_borrows(self):
        try:
            rows = Borrow.get_all_borrows(self.db)
            if not rows:
                print("[INFO] No borrows found.")
                return

            print("\n{:<10} {:<10} {:<10} {:<12} {:<12} {:<12} {:<15} {:<15}".format(
                "BorrowID", "MemberID", "BookID", "BorrowDate", "DueDate", "ReturnDate", "MemberName", "BookTitle"
            ))
            print("-" * 95)

            for r in rows:
                print("{:<10} {:<10} {:<10} {:<12} {:<12} {:<12} {:<15} {:<15}".format(
                    r.get("borrow_id", "-"),
                    r.get("member_id", "-"),
                    r.get("book_id", "-"),
                    str(r.get("borrow_date") or "-"),
                    str(r.get("due_date") or "-"),
                    str(r.get("return_date") or "-"),
                    r.get("member_name", "-"),
                    r.get("book_title", "-")
                ))

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to list borrows: {e}")

    # Ham dung de goi update_borrow o model va thuc hien them phan quyen (Chi co manager moi duoc thuc hien)
    def update_borrow(self, borrow_id, data: dict):
        try:
            try:
                require_manager()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            result = Borrow.update_borrow(
                self.db,
                borrow_id=borrow_id,
                member_id=data.get("member_id"),
                book_id=data.get("book_id"),
                borrow_date=data.get("borrow_date"),
                due_date=data.get("due_date"),
                return_date=data.get("return_date")
            )

            print(result)

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to update borrow: {e}")

    # Goi ham return_book o model (chi co manager moi duoc goi)
    def return_book(self, borrow_id, return_date=None):
        try:
            try:
                require_manager()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            result = Borrow.return_book(self.db, borrow_id, return_date)
            print(result)

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to return book: {e}")

    # Ham dung de goi ham delete_borrow o model (chi co manager moi duoc goi)
    def delete_borrow(self, borrow_id):
        try:
            try:
                require_manager()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            success = Borrow.delete_borrow(self.db, borrow_id)
            if success:
                print("[SUCCESS] Borrow deleted successfully.")
            else:
                print("[ERROR] Borrow ID not found or deletion failed.")

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to delete borrow: {e}")
