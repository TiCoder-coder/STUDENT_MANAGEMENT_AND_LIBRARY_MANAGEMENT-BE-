# FILE: views/borrowsView.py
from services.borrowsService import BorrowsService
from auth import current_user


# ================================= BORROWS MENU =====================================
def borrows_menu(db, current_user):
    svc = BorrowsService(db)

    while True:
        print("\n=== BORROW MANAGEMENT MENU ===")

        # Nếu là member (chưa đăng nhập hoặc không có quyền manager)
        if not current_user["role"] or current_user["role"] != "manager":
            print("1. Search Borrow")
            print("2. List All Borrows")
            print("3. View Overdue Borrows")
            print("0. Back to Main Menu")

            choice = input("Select: ").strip()

            if choice == "1":
                search_borrow_view(svc)
            elif choice == "2":
                list_borrows_view(svc)
            elif choice == "3":
                overdue_borrows_view(svc)
            elif choice == "0":
                break
            else:
                print("Invalid choice, please try again.")
        else:
            # Nếu là manager (được phép thao tác thêm, sửa, xóa, trả)
            print("1. Add Borrow (Borrow Book)")
            print("2. Return Book")
            print("3. Update Borrow Info")
            print("4. Delete Borrow")
            print("5. Search Borrow")
            print("6. List All Borrows")
            print("7. View Overdue Borrows")
            print("0. Back")

            choice = input("Select: ").strip()

            if choice == "1":
                add_borrow_view(svc)
            elif choice == "2":
                return_book_view(svc)
            elif choice == "3":
                update_borrow_view(svc)
            elif choice == "4":
                delete_borrow_view(svc)
            elif choice == "5":
                search_borrow_view(svc)
            elif choice == "6":
                list_borrows_view(svc)
            elif choice == "7":
                overdue_borrows_view(svc)
            elif choice == "0":
                break
            else:
                print("Invalid choice, please try again.")


# ================================ ADD BORROW (MANAGER) =================================
def add_borrow_view(svc: BorrowsService):
    print("\n=== ADD NEW BORROW (Borrow Book) ===")
    member_id = input("Member ID: ").strip()
    book_id = input("Book ID: ").strip()
    borrow_date = input("Borrow Date (YYYY-MM-DD, press Enter for today): ").strip() or None
    due_date = input("Due Date (YYYY-MM-DD): ").strip()
    return_date = input("Return Date (optional, YYYY-MM-DD): ").strip() or None

    data = {
        "member_id": member_id,
        "book_id": book_id,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "return_date": return_date
    }

    svc.add_borrow(data)


# ================================ RETURN BOOK (MANAGER) ================================
def return_book_view(svc: BorrowsService):
    print("\n=== RETURN BOOK ===")
    borrow_id = input("Enter Borrow ID to return: ").strip()
    return_date = input("Return Date (YYYY-MM-DD, press Enter for today): ").strip() or None
    svc.return_book(borrow_id, return_date)


# ================================ UPDATE BORROW (MANAGER) ==============================
def update_borrow_view(svc: BorrowsService):
    print("\n=== UPDATE BORROW INFORMATION ===")
    borrow_id = input("Enter Borrow ID to update: ").strip()

    member_id = input("New Member ID (press Enter to skip): ").strip() or None
    book_id = input("New Book ID (press Enter to skip): ").strip() or None
    borrow_date = input("New Borrow Date (YYYY-MM-DD, press Enter to skip): ").strip() or None
    due_date = input("New Due Date (YYYY-MM-DD, press Enter to skip): ").strip() or None
    return_date = input("New Return Date (YYYY-MM-DD, press Enter to skip): ").strip() or None

    data = {
        "member_id": member_id,
        "book_id": book_id,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "return_date": return_date
    }

    svc.update_borrow(borrow_id, data)


# ================================ DELETE BORROW (MANAGER) ==============================
def delete_borrow_view(svc: BorrowsService):
    print("\n=== DELETE BORROW RECORD ===")
    borrow_id = input("Enter Borrow ID to delete: ").strip()
    svc.delete_borrow(borrow_id)


# ================================ SEARCH BORROW (ALL USERS) ============================
def search_borrow_view(svc: BorrowsService):
    print("\n=== SEARCH BORROW RECORD ===")
    borrow_id = input("Borrow ID (press Enter to skip): ").strip() or None
    member_id = input("Member ID (press Enter to skip): ").strip() or None
    book_id = input("Book ID (press Enter to skip): ").strip() or None
    overdue_only_input = input("Show only overdue borrows? (y/n): ").strip().lower()
    overdue_only = overdue_only_input == "y"

    svc.search_borrows(
        borrow_id=borrow_id,
        member_id=member_id,
        book_id=book_id,
        overdue_only=overdue_only
    )


# ================================ LIST ALL BORROWS (ALL USERS) =========================
def list_borrows_view(svc: BorrowsService):
    print("\n=== ALL BORROW RECORDS ===")
    svc.list_borrows()


# ================================ OVERDUE BORROWS (ALL USERS) ==========================
def overdue_borrows_view(svc: BorrowsService):
    print("\n=== OVERDUE BORROW RECORDS ===")
    svc.search_borrows(overdue_only=True)
