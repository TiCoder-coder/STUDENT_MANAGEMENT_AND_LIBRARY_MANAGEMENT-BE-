from auth import login, logout, current_user
from db_connection import Database
from views.booksView import books_menu
from views.membersView import member_menu
from views.borrowsView import borrows_menu
from views.managersView import manager_menu
from services.booksService import BookService
from services.membersService import MemberService
from services.borrowsService import BorrowsService


def main_menu(db):
    # Khoi tao service mot lan
    book_service = BookService(db)
    member_service = MemberService(db)
    borrow_service = BorrowsService(db)

    while True:
        print("\n=== LIBRARY MANAGEMENT SYSTEM ===")
        user_display = current_user["username"] if current_user["username"] else "Guest"
        role_display = current_user["role"] if current_user["role"] else "None"
        print(f"Current User: {user_display} ({role_display})")
        print("--------------------------------------")

        # Neu chua dang nhap thi la khach
        if not current_user["role"]:
            print("1. View Books")
            print("2. Borrow Books")
            print("3. Login")
            print("0. Exit")

            choice = input("\nSelect: ").strip()
            print()

            try:
                if choice == "1":
                    books_menu(book_service, current_user)
                elif choice == "2":
                    borrows_menu(borrow_service, current_user)
                elif choice == "3":
                    login(db)
                elif choice == "0":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice, please try again.")
            except Exception as e:
                print(f"[SYSTEM ERROR] {e}")

        # Neu da dang nhap thi chuyen sang menu manager
        else:
            print("1. Manage Members")
            print("2. Manage Books")
            print("3. Manage Borrow/Return")
            print("4. Manage managers")
            print("5. Logout")
            print("0. Exit")

            choice = input("\nSelect: ").strip()
            print()

            try:
                if choice == "1":
                    member_menu(db, current_user)
                elif choice == "2":
                    books_menu(db, current_user)

                elif choice == "3":
                    borrows_menu(db, current_user)
                elif choice == "4":
                   manager_menu(db, current_user) 
                elif choice == "5":
                    logout()
                elif choice == "0":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice, please try again.")
            except Exception as e:
                print(f"[SYSTEM ERROR] {e}")


if __name__ == "__main__":
    print("=== STARTING LIBRARY MANAGEMENT SYSTEM ===")
    db = Database()
    print("Database connected successfully.")
    main_menu(db)
