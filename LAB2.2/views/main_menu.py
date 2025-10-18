# /home/voanhnhat/Documents/LAB_2/LAB2.2/views/main_menu.py
# ---------------------------------------------------------------------------------------------------
# MODULE: main_menu.py
# MÔ TẢ:
#   - Đây là giao diện menu chính của hệ thống Library Management System.
#   - Giao diện chia làm 2 phần: 
#       + Guest (người chưa đăng nhập)
#       + Manager và Member (đã đăng nhập, có quyền khác nhau)
#   - Giao diện được chia nhỏ, gọi đến các view khác như booksView, borrowsView, managersView, membersView.
# ---------------------------------------------------------------------------------------------------

from views import booksView, borrowsView, managersView, membersView
from auth import login, logout, current_user

# ---------------------------------------------------------------------------------------------------
# MENU KHÁCH (CHƯA ĐĂNG NHẬP)
# ---------------------------------------------------------------------------------------------------
def guest_menu(db):
    while True:
        print("\n=== 📚 LIBRARY MANAGEMENT SYSTEM ===")
        print("--------------------------------------")
        print("1. View Books")
        print("2. Login to System")
        print("0. Exit")

        choice = input("\nSelect: ").strip()

        if choice == "1":
            booksView.view_books(db)
        elif choice == "2":
            if login(db):  # Nếu đăng nhập thành công thì chuyển sang main menu
                main_menu(db)
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice, please try again.")


# ---------------------------------------------------------------------------------------------------
# MENU CHÍNH SAU KHI ĐĂNG NHẬP (Manager hoặc Member)
# ---------------------------------------------------------------------------------------------------
def main_menu(db):
    role = current_user.get("role", "guest")

    # Hiển thị thông tin người dùng hiện tại
    print(f"\n🔑 Logged in as: {role.capitalize()} ({current_user['username']})")

    # Manager có quyền cao nhất: quản lý sách, mượn sách, member, manager
    if role == "manager":
        manager_main_menu(db)
    # Member chỉ có quyền quản lý mượn sách và xem sách
    elif role == "member":
        member_main_menu(db)
    else:
        print("⚠️ Invalid role or unauthorized access.")
        logout()


# ---------------------------------------------------------------------------------------------------
# MENU DÀNH CHO MANAGER (ADMIN)
# ---------------------------------------------------------------------------------------------------
def manager_main_menu(db):
    while True:
        print("\n=== 🧑‍💼 MANAGER DASHBOARD ===")
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
            print("🔒 Logged out successfully.")
            break
        elif choice == "0":
            print("↩ Returning to guest mode...")
            logout()
            guest_menu(db)
            break
        else:
            print("❌ Invalid choice, please try again.")


# ---------------------------------------------------------------------------------------------------
# MENU DÀNH CHO MEMBER (NGƯỜI DÙNG THƯỜNG)
# ---------------------------------------------------------------------------------------------------
def member_main_menu(db):
    while True:
        print("\n=== 👤 MEMBER DASHBOARD ===")
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
            print("🔒 Logged out successfully.")
            break
        elif choice == "0":
            print("↩ Returning to guest mode...")
            logout()
            guest_menu(db)
            break
        else:
            print("❌ Invalid choice, please try again.")
