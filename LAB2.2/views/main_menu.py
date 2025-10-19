from views import booksView, borrowsView, managersView, membersView
from auth import login, logout, current_user

# ---------------------------------------------------------------------------------------------------
# MENU KHÁCH (CHUA DANG NHAP)
# ---------------------------------------------------------------------------------------------------
def guest_menu(db):
    while True:
        print("\n=== LIBRARY MANAGEMENT SYSTEM ===")
        print("--------------------------------------")
        print("1. View Books")
        print("2. Login to System")
        print("0. Exit")

        choice = input("\nSelect: ").strip()

        if choice == "1":
            booksView.view_books(db)
        elif choice == "2":
            if login(db):  # Neu dang nhap thanh cong thi chuyen sang main menu
                main_menu(db)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


# ---------------------------------------------------------------------------------------------------
# MENU CHINH SAU KHI DANG NHAP
# ---------------------------------------------------------------------------------------------------
def main_menu(db):
    role = current_user.get("role", "guest")

    # Hien thi thong tin nguoi dung hien tai
    print(f"\nLogged in as: {role.capitalize()} ({current_user['username']})")

    # Manager co quyen cao nhat -- co the thuc hien day du chuc nang crud
    if role == "manager":
        manager_main_menu(db)
    # Member chi co quyen muon va xem sach
    elif role == "member":
        member_main_menu(db)
    else:
        print("Invalid role or unauthorized access.")
        logout()


# ---------------------------------------------------------------------------------------------------
# MENU DANH CHO MANAGER 
# ---------------------------------------------------------------------------------------------------
def manager_main_menu(db):
    while True:
        print("\n=== MANAGER DASHBOARD ===")
        print(f"Current User: {current_user['username']}")
        print("--------------------------------------")
        print("1. Manage Books")
        print("2. Manage Borrows")
        print("3. Manage Members")
        print("4. Manage Managers")
        print("5. Logout")
        print("0. Back to Guest Mode")

        choice = input("Select: ").strip()

        if choice == "1":
            booksView.book_menu(db, current_user)
        elif choice == "2":
            borrowsView.borrow_menu(db, current_user)
        elif choice == "3":
            membersView.member_menu(db, current_user)
        elif choice == "4":
            managersView.manager_menu(db, current_user)
        elif choice == "5":
            logout()
            print("Logged out successfully.")
            break
        elif choice == "0":
            print("↩ Returning to guest mode...")
            logout()
            guest_menu(db)
            break
        else:
            print("Invalid choice, please try again.")


# ---------------------------------------------------------------------------------------------------
# MENU DANH CHO MEMEBER
# ---------------------------------------------------------------------------------------------------
def member_main_menu(db):
    while True:
        print("\n=== MEMBER DASHBOARD ===")
        print(f"Current User: {current_user['username']}")
        print("--------------------------------------")
        print("1. View Books")
        print("2. View Borrow History")
        print("3. Borrow a Book")
        print("4. Return a Book")
        print("5. Logout")
        print("0. Back to Guest Mode")

        choice = input("Select: ").strip()

        if choice == "1":
            booksView.view_books(db)
        elif choice == "2":
            borrowsView.view_borrow_history(db, current_user)
        elif choice == "3":
            borrowsView.borrow_book(db, current_user)
        elif choice == "4":
            borrowsView.return_book(db, current_user)
        elif choice == "5":
            logout()
            print("Logged out successfully.")
            break
        elif choice == "0":
            print("Returning to guest mode...")
            logout()
            guest_menu(db)
            break
        else:
            print("Invalid choice, please try again.")
