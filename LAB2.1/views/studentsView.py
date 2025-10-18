from services.studentsServices import StudentService
from auth import current_user, require_teacher

def student_menu(db, search_student=False):
    svc = StudentService(db)

    # STUDENT MODE
    if not current_user or not isinstance(current_user, dict) or current_user.get("role") != "teacher":
        print("\n=== STUDENT MENU (Guest Mode) ===")
        print("1. Search student by ID")
        print("2. List all students")
        print("0. Back")

        while True:
            choice = input("Select: ").strip()
            if choice == "1":
                search_student_view(svc)
            elif choice == "2":
                list_students_view(svc)
            elif choice == "0":
                break
            else:
                print("Invalid choice, try again.")
        return

    # TEACHER MODE
    while True:
        print("\n=== STUDENT MENU (Teacher Mode) ===")
        print("1. Add student")
        print("2. Update student")
        print("3. Delete student")
        print("4. Search student by ID")
        print("5. List all students")
        print("0. Back")

        choice = input("Select: ").strip()

        if choice == "1":
            add_student_view(svc)
        elif choice == "2":
            update_student_view(svc)
        elif choice == "3":
            delete_student_view(svc)
        elif choice == "4":
            search_student_view(svc)
        elif choice == "5":
            list_students_view(svc)
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

# Menu hien thi thong tin cac hoc sinh
def list_students_view(svc: StudentService):
    print("\n=== STUDENT LIST ===")
    students = svc.get_all_students()
    if not students:
        print("[INFO] No students found.")
        return
    for s in students:
        if isinstance(s, dict):
            print(f"ID: {s['studentId']}, Name: {s['fullName']}, Birthday: {s['birthday']}, "
                  f"Email: {s['email']}, Phone: {s['phoneNumber']}, Address: {s['address']}")
        else:
            print(f"ID: {s[0]}, Name: {s[1]}, Birthday: {s[2]}, Email: {s[3]}, Phone: {s[4]}, Address: {s[5]}")


# Menu add mot hoc sinh moi
def add_student_view(svc: StudentService):
    print("\n=== ADD STUDENT ===")
    data = {
        "studentId": input("Student ID: ").strip(),
        "fullName": input("Full Name: ").strip(),
        "birthday": input("Birthday (YYYY-MM-DD): ").strip(),
        "email": input("Email: ").strip(),
        "phoneNumber": input("Phone: ").strip(),
        "address": input("Address: ").strip()
    }
    svc.add_student(data)


def update_student_view(svc: StudentService):
    print("\n=== UPDATE STUDENT ===")
    data = {
        "studentId": input("Student ID: ").strip(),
        "fullName": input("New Full Name (leave blank to keep): ").strip(),
        "birthday": input("New Birthday (YYYY-MM-DD): ").strip(),
        "email": input("New Email: ").strip(),
        "phoneNumber": input("New Phone: ").strip(),
        "address": input("New Address: ").strip()
    }
    svc.update_student(data)


def delete_student_view(svc: StudentService):
    print("\n=== DELETE STUDENT ===")
    student_id = input("Enter student ID to delete: ").strip()
    svc.delete_student(student_id)


def search_student_view(svc: StudentService):
    print("\n=== SEARCH STUDENT ===")
    student_id = input("Enter student ID: ").strip()
    result = svc.search_student(str(student_id).strip())

    if not result:
        print("[INFO] Student not found.")
        return

    s = result[0]
    if isinstance(s, dict):
        print(f"ID: {s['studentId']}, Name: {s['fullName']}, Birthday: {s['birthday']}, "
              f"Email: {s['email']}, Phone: {s['phoneNumber']}, Address: {s['address']}")
    else:
        print(f"ID: {s[0]}, Name: {s[1]}, Birthday: {s[2]}, "
              f"Email: {s[3]}, Phone: {s[4]}, Address: {s[5]}")
