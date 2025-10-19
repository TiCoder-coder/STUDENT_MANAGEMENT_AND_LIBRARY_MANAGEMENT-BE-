from services.managersService import ManagerService

# --------------------------------------------
# MENU QUAN LY MANAGER
# --------------------------------------------
def manager_menu(db, current_user):
    svc = ManagerService(db)

    # Kiem tra quyen truy cap --- Chi co manager moi duoc truy cap menu nay 
    if not current_user or current_user.get("role") != "manager":
        print("Access denied! Only MANAGER can manage managers.")
        return

    while True:
        print("\n=== MANAGER MANAGEMENT MENU ===")
        print("1. Add manager")
        print("2. Update manager")
        print("3. Delete manager")
        print("4. Search manager by ID")
        print("5. List all managers")
        print("6. Manager login test")
        print("0. Back")

        choice = input("Select: ").strip()

        try:
            # --------------------------------------------
            # THEM MOT MANAGER MOI
            # --------------------------------------------
            if choice == "1":
                data = {
                    "manager_id": input("Manager ID: ").strip(),
                    "full_name": input("Full Name: ").strip(),
                    "email": input("Email: ").strip(),
                    "username": input("Username: ").strip(),
                    "password": input("Password: ").strip(),
                    "phoneNumber": input("Phone number: ").strip(),
                    "created_at": input("Created at (YYYY-MM-DD) [optional]: ").strip() or None
                }
                svc.add_manager(data)

            # --------------------------------------------
            # CAP NHAP THONG TIN MANAGER
            # --------------------------------------------
            elif choice == "2":
                manager_id = input("Manager ID to update: ").strip()
                old_manager = svc.search_manager(manager_id)
                if not old_manager:
                    print("Manager not found.")
                    continue

                print("\nLeave blank to keep the current value.\n")

                full_name = input(f"Full Name [{old_manager['full_name']}]: ").strip() or old_manager['full_name']
                email = input(f"Email [{old_manager['email']}]: ").strip() or old_manager['email']
                username = input(f"Username [{old_manager['username']}]: ").strip() or old_manager['username']
                password = input("New Password (leave blank to keep current): ").strip() or old_manager['password']
                phoneNumber = input(f"Phone number [{old_manager['phoneNumber']}]: ").strip() or old_manager['phoneNumber']
                created_at = input(f"Created at [{old_manager.get('created_at', '')}]: ").strip() or old_manager.get('created_at', None)

                data = {
                    "manager_id": manager_id,
                    "full_name": full_name,
                    "email": email,
                    "username": username,
                    "password": password,
                    "phoneNumber": phoneNumber,
                    "created_at": created_at
                }

                svc.update_manager(data)

            # --------------------------------------------
            # XOA MOT MANAGER
            # --------------------------------------------
            elif choice == "3":
                manager_id = input("Manager ID to delete: ").strip()
                confirm = input(f"Are you sure to delete manager '{manager_id}'? (y/n): ").strip().lower()
                if confirm == "y":
                    svc.delete_manager(manager_id)
                else:
                    print("Cancelled.")

            # --------------------------------------------
            # TIM KIEM MANAGER THEO ID
            # --------------------------------------------
            elif choice == "4":
                manager_id = input("Enter Manager ID to search: ").strip()
                manager = svc.search_manager(manager_id)
                if manager:
                    print(
                        f"\nFound manager:\n"
                        f"   ID: {manager['manager_id']}\n"
                        f"   Name: {manager['full_name']}\n"
                        f"   Email: {manager['email']}\n"
                        f"   Username: {manager['username']}\n"
                        f"   Phone: {manager['phoneNumber']}\n"
                        f"   Created at: {manager.get('created_at', 'N/A')}"
                    )
                else:
                    print("Manager not found.")

            # --------------------------------------------
            # HIEN THI DANH SACH TAT CA MANAGER
            # --------------------------------------------
            elif choice == "5":
                managers = svc.get_all_managers()
                if managers:
                    print("\n=== MANAGER LIST ===")
                    for m in managers:
                        print(
                            f"ID: {m['manager_id']}, "
                            f"Name: {m['full_name']}, "
                            f"Email: {m['email']}, "
                            f"Username: {m['username']}, "
                            f"Phone: {m['phoneNumber']}, "
                            f"Created at: {m.get('created_at', 'N/A')}"
                        )
                else:
                    print("No managers found.")

            # --------------------------------------------
            # KIEM TRA DANG NHAP MANAGER (HASH CHECK)
            # --------------------------------------------
            elif choice == "6":
                print("\n=== MANAGER LOGIN ===")
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                svc.login(username, password)

            # --------------------------------------------
            # THOAT KHOI MENU MENU
            # --------------------------------------------
            elif choice == "0":
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"[VIEW ERROR] {e}")