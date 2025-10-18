from services.teacherService import TeacherService
from auth import require_teacher, current_user


def teacher_menu(db, current_user):
    # Kiem tra quyen teacher
    if not require_teacher():
        return

    svc = TeacherService(db)

    while True:
        print("\n=== TEACHER MANAGEMENT MENU ===")
        print("1. Add teacher")
        print("2. Update teacher")
        print("3. Delete teacher")
        print("4. Search teacher by ID")
        print("5. List all teachers")
        print("0. Back")

        choice = input("Select: ").strip()

        try:
            # Them giao vien
            if choice == "1":
                if current_user.get("role") != "teacher":
                    print("Only teachers can add teacher records.")
                    continue

                data = {
                    "teacherId": input("Teacher ID: ").strip(),
                    "fullName": input("Full name: ").strip(),
                    "birthday": input("Birthday (YYYY-MM-DD): ").strip(),
                    "email": input("Email: ").strip(),
                    "phoneNumber": input("Phone number: ").strip(),
                    "address": input("Address: ").strip(),
                    "userName": input("Username (for login): ").strip(),
                    "password": input("Password: ").strip()
                }
                svc.add_teacher(data)
            
            # Tim kiem giao vien
            elif choice == "4":
                teacherId = input("🔍 Teacher ID to search: ").strip()
                teacher = svc.search_teacher(teacherId)
                if teacher:
                    print(
                        f"\nFound teacher:\n"
                        f"   ID: {teacher['teacherId']}\n"
                        f"   Name: {teacher['fullName']}\n"
                        f"   Birthday: {teacher['birthday']}\n"
                        f"   Email: {teacher['email']}\n"
                        f"   Phone: {teacher['phoneNumber']}\n"
                        f"   Address: {teacher['address']}\n"
                        f"   Username: {teacher['userName']}\n"
                        f"   Password: {teacher['password']}"
                    )
                else:
                    print("Teacher not found.")

            # Hien thi danh sach toan bo teacher
            elif choice == "5":
                teachers = svc.get_all_teachers()
                if teachers:
                    print("\n=== 🧾 TEACHER LIST ===")
                    for t in teachers:
                        print(
                            f"ID: {t['teacherId']}, "
                            f"Name: {t['fullName']}, "
                            f"Birthday: {t['birthday']}, "
                            f"Email: {t['email']}, "
                            f"Phone: {t['phoneNumber']}, "
                            f"Address: {t['address']}, "
                            f"Username: {t['userName']}, "
                            f"Password: {t['password']}"
                        )
                else:
                    print("📭 No teachers found.")
            
            # Cap nhap giao vien
            elif choice == "2":
                if current_user.get("role") != "teacher":
                    print("Only teachers can update teacher records.")
                    continue

                teacherId = input("Teacher ID to update: ").strip()
                old_teacher = svc.search_teacher(teacherId)

                if not old_teacher:
                    print("Teacher not found.")
                    continue

                print("\nLeave blank to keep the current value.\n")

                fullName = input(f"Full name [{old_teacher['fullName']}]: ").strip() or old_teacher['fullName']
                birthday = input(f"Birthday (YYYY-MM-DD) [{old_teacher['birthday']}]: ").strip() or old_teacher['birthday']
                email = input(f"Email [{old_teacher['email']}]: ").strip() or old_teacher['email']
                phoneNumber = input(f"Phone number [{old_teacher['phoneNumber']}]: ").strip() or old_teacher['phoneNumber']
                address = input(f"Address [{old_teacher['address']}]: ").strip() or old_teacher['address']
                userName = input(f"Username [{old_teacher['userName']}]: ").strip() or old_teacher['userName']
                password = input(f"Password [{old_teacher['password']}]: ").strip() or old_teacher['password']

                data = {
                    "teacherId": teacherId,
                    "fullName": fullName,
                    "birthday": birthday,
                    "email": email,
                    "phoneNumber": phoneNumber,
                    "address": address,
                    "userName": userName,
                    "password": password
                }

                svc.update_teacher(data)

            # Xoa giao vien
            elif choice == "3":
                if current_user.get("role") != "teacher":
                    print("Only teachers can delete teacher records.")
                    continue

                teacherId = input("Teacher ID to delete: ").strip()
                svc.delete_teacher(teacherId)


            # Thoat
            elif choice == "0":
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"Error: {e}")
