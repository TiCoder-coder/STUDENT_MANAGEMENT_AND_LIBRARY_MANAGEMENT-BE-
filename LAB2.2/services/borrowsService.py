# FILE: services/borrowsService.py
from models.borrowsModel import Borrow
from auth import require_manager  # Goi ham kiem tra quyen (chi manager duoc muon/tra sach)

# CLASS BORROWSSERVICE: GỌI LẠI CÁC HÀM CỦA MODEL VÀ THỰC THI NÓ CÓ KIỂM TRA QUYỀN -----------------------------
class BorrowsService:

    # Khởi tạo service
    def __init__(self, db):
        self.db = db

    # GỌI HÀM THÊM BORROW (mượn sách) --- CHỈ MANAGER MỚI ĐƯỢC GỌI
    def add_borrow(self, data: dict):
        try:
            # 1. Kiểm tra quyền
            try:
                require_manager()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            # 2. Kiểm tra dữ liệu đầu vào
            member_id = data.get("member_id")
            book_id = data.get("book_id")
            borrow_date = data.get("borrow_date")
            due_date = data.get("due_date")
            return_date = data.get("return_date")

            if not member_id or not book_id or not due_date:
                print("[VALIDATION ERROR] member_id, book_id, and due_date are required.")
                return

            # 3. Tạo đối tượng Borrow
            borrow = Borrow(
                member_id=member_id,
                book_id=book_id,
                borrow_date=borrow_date,
                due_date=due_date,
                return_date=return_date
            )

            # 4. Gọi model để thêm borrow
            result = borrow.add_borrow(self.db)
            print(result)

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to add borrow: {e}")

    # GỌI HÀM TÌM KIẾM BORROW THEO ID HOẶC MEMBER, BOOK --- HÀM MỞ, AI CŨNG DÙNG ĐƯỢC
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

            # In header
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

    # GỌI HÀM LẤY TẤT CẢ BORROWS --- HÀM MỞ
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

    # GỌI HÀM CẬP NHẬT BORROW --- CHỈ MANAGER ĐƯỢC GỌI
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

    # GỌI HÀM TRẢ SÁCH --- CHỈ MANAGER ĐƯỢC GỌI
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

    # GỌI HÀM XÓA BORROW --- CHỈ MANAGER ĐƯỢC GỌI
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
