from auth import login, logout, current_user
from db_connection import Database
from views.studentsView import student_menu
from views.coursesView import course_menu
from views.enrollementsView import enrollment_menu
from views.teachersView import teacher_menu
from services.studentsServices import StudentService
from services.coursesService import CourseService
from services.enrollmentsService import EnrollmentService
from services.teacherService import TeacherService


def main_menu(db):
    # Khoi tao server 1 lan dung lai xuyen suot
    student_service = StudentService(db)
    course_service = CourseService(db)
    enrollment_service = EnrollmentService(db)
    teacher_service = TeacherService(db)

    while True:
        print("\n=== STUDENT MANAGEMENT SYSTEM ===")
        user_display = current_user["username"] if current_user["username"] else "Guest"
        role_display = current_user["role"] if current_user["role"] else "None"
        print(f"Current User: {user_display} ({role_display})")
        print("---------------------------------------")
        print("1. View Students")
        print("2. View Courses")
        print("3. View Enrollments")
        print("4. Teacher Management (Require Login)")
        if current_user["role"]:  # Chi hien khi da login
            print("5. Logout")
        print("0. Exit")

        choice = input("\nSelect: ").strip()
        print()

        try:
            if choice == '1':
                student_menu(student_service, current_user)
            elif choice == "2":
                course_menu(course_service, current_user)
            elif choice == '3':
                enrollment_menu(enrollment_service, current_user)
            elif choice == '4':
                if not current_user["role"]:
                    print("Teacher login required.")
                    if not login(db):
                        continue

                # Sau khi login thanh cong
                while True:
                    print("\n=== MANAGEMENT MENU ===")
                    print("1. Manage Students")
                    print("2. Manage Courses")
                    print("3. Manage Enrollments")
                    print("4. Manage Teachers")
                    print("0. Back")
                    sub_choice = input("Select: ").strip()

                    if sub_choice == "1":
                        student_menu(student_service, current_user)
                    elif sub_choice == "2":
                        course_menu(course_service, current_user)
                    elif sub_choice == "3":
                        enrollment_menu(enrollment_service, current_user)
                    elif sub_choice == "4":
                        teacher_menu(teacher_service, current_user)
                    elif sub_choice == "0":
                        break
                    else:
                        print("Invalid choice, please try again.")

                logout()  # Logout sau khi back

            elif choice == '5' and current_user["role"]:
                logout()
            elif choice == '0':
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")
        except Exception as e:
            print(f"Error in main menu: {e}")


if __name__ == "__main__":
    db = Database()
    print("Database connected successfully.")
    main_menu(db)
