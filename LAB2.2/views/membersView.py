# ============================================
# File: views/membersView.py
# Description: View hiển thị và thao tác với MEMBER trong thư viện
# ============================================

from services.membersService import MemberService
from auth import current_user, require_manager


# --------------------------------------------
# MENU CHÍNH CỦA MEMBER
# --------------------------------------------
def member_menu(db, current_user):

    svc = MemberService(db)

    # --- GUEST MODE (Không phải teacher) ---
    if not current_user or not isinstance(current_user, dict) or current_user.get("role") not in ["manager", "admin"]:

        print("\n=== MEMBER MENU (Guest Mode) ===")
        print("1. Search member by ID / Name / Email")
        print("2. List all members")
        print("0. Back")

        while True:
            choice = input("Select: ").strip()
            if choice == "1":
                search_member_view(svc)
            elif choice == "2":
                list_members_view(svc)
            elif choice == "0":
                break
            else:
                print("Invalid choice, try again.")
        return

    # --- TEACHER MODE ---
    while True:
        print("\n=== MEMBER MENU (Teacher Mode) ===")
        print("1. Add member")
        print("2. Update member")
        print("3. Delete member")
        print("4. Search member by ID / Name / Email")
        print("5. List all members")
        print("0. Back")

        choice = input("Select: ").strip()

        if choice == "1":
            add_member_view(svc)
        elif choice == "2":
            update_member_view(svc)
        elif choice == "3":
            delete_member_view(svc)
        elif choice == "4":
            search_member_view(svc)
        elif choice == "5":
            list_members_view(svc)
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")


# --------------------------------------------
# HIỂN THỊ DANH SÁCH MEMBER
# --------------------------------------------
def list_members_view(svc: MemberService):
    print("\n=== MEMBER LIST ===")
    members = svc.get_all_members()
    if not members:
        print("[INFO] No members found.")
        return

    for m in members:
        if isinstance(m, dict):
            print(f"ID: {m['member_id']}, Name: {m['name']}, Birthday: {m['birthday']}, "
                  f"Email: {m['email']}, Phone: {m['phoneNumber']}")
        else:
            # Trong trường hợp kết quả trả về là tuple (tuỳ DB)
            print(f"ID: {m[0]}, Name: {m[1]}, Birthday: {m[2]}, "
                  f"Email: {m[3]}, Phone: {m[4]}")


# --------------------------------------------
# THÊM MỘT MEMBER MỚI (Teacher Only)
# --------------------------------------------
def add_member_view(svc: MemberService):
    print("\n=== ADD MEMBER ===")
    data = {
        "name": input("Full Name: ").strip(),
        "birthday": input("Birthday (YYYY-MM-DD): ").strip(),
        "email": input("Email: ").strip(),
        "phoneNumber": input("Phone: ").strip()
    }
    svc.add_member(data)


# --------------------------------------------
# CẬP NHẬT THÔNG TIN MEMBER (Teacher Only)
# --------------------------------------------
def update_member_view(svc: MemberService):
    print("\n=== UPDATE MEMBER ===")
    data = {
        "member_id": input("Member ID: ").strip(),
        "name": input("New Name (leave blank to keep): ").strip(),
        "birthday": input("New Birthday (YYYY-MM-DD): ").strip(),
        "email": input("New Email: ").strip(),
        "phoneNumber": input("New Phone: ").strip()
    }
    svc.update_member(data)


# --------------------------------------------
# XÓA MEMBER (Teacher Only)
# --------------------------------------------
def delete_member_view(svc: MemberService):
    print("\n=== DELETE MEMBER ===")
    member_id = input("Enter member ID to delete: ").strip()
    svc.delete_member(member_id)


# --------------------------------------------
# TÌM KIẾM MEMBER
# --------------------------------------------
def search_member_view(svc: MemberService):
    print("\n=== SEARCH MEMBER ===")
    member_id = input("Enter member ID (or leave blank): ").strip()
    name = input("Enter name (or leave blank): ").strip()
    email = input("Enter email (or leave blank): ").strip()

    results = svc.search_member(member_id=member_id, name=name, email=email)
    if not results:
        print("[INFO] Member not found.")
        return

    for m in results:
        if isinstance(m, dict):
            print(f"ID: {m['member_id']}, Name: {m['name']}, Birthday: {m['birthday']}, "
                  f"Email: {m['email']}, Phone: {m['phoneNumber']}")
        else:
            print(f"ID: {m[0]}, Name: {m[1]}, Birthday: {m[2]}, "
                  f"Email: {m[3]}, Phone: {m[4]}")
