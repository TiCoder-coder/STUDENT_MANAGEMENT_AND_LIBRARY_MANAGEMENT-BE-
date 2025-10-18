from views import studentsView, coursesView, enrollementsView, teachersView
from auth import login, logout, current_user

def guest_menu():
    while True:
        print("\n=== STUDENT MANAGEMENT SYSTEM ===")
        print(f"Current User: {current_user['role'].capitalize()} ({current_user['username']})")
        print("---------------------------------------")
        print("1. View Students")
        print("2. View Courses")
        print("3. View Enrollments")
        print("4. Teacher Management (Require Login)")
        print("0. Exit")
        choice = input("\nSelect: ")

        if choice == "1":
            studentsView.view_students()
        elif choice == "2":
            coursesView.view_courses()
        elif choice == "3":
            enrollementsView.view_enrollments()
        elif choice == "4":
            if login():
                teacher_main_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

def teacher_main_menu():
    while True:
        print("\n=== TEACHER MANAGEMENT ===")
        print(f"Current User: {current_user['username']}")
        print("--------------------------------")
        print("1. Manage Courses")
        print("2. Manage Enrollments")
        print("3. Manage Students")
        print("4. Manage Teachers")
        print("5. Logout")
        print("0. Back to Guest Mode")
        choice = input("Select: ")

        if choice == "1":
            coursesView.course_menu()
        elif choice == "2":
            enrollementsView.enrollment_menu()
        elif choice == "3":
            studentsView.student_menu()
        elif choice == "4":
            teachersView.teacher_menu()
        elif choice == "5":
            logout()
            break
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
