from services.enrollmentsService import EnrollmentService
from auth import current_user

# ENROLLMENT MENU
def enrollment_menu(service, current_user):
    svc = service

    while True:
        print("\n=== ENROLLMENT MENU ===")
        # Neu chua login thi chi cho xem va tim kiem thong tin
        if not current_user["role"]:
            print("1. Search Enrollment")
            print("2. List All Enrollments")
            print("0. Back to Main Menu")
            choice = input("Select: ").strip()

            if choice == "1":
                search_enrollment_view(svc)
            elif choice == "2":
                list_enrollments_view(svc)
            elif choice == "0":
                break
            else:
                print("Invalid choice, please try again.")
        else:
            # Khi da login (Teacher mode)
            print("1. Add Enrollment")
            print("2. Delete Enrollment")
            print("3. Update Enrollment")
            print("4. Search Enrollment")
            print("5. List All Enrollments")
            print("0. Back")

            choice = input("Select: ").strip()

            if choice == "1":
                add_enrollment_view(svc)
            elif choice == "2":
                delete_enrollment_view(svc)
            elif choice == "3":
                update_enrollment_view(svc)
            elif choice == "4":
                search_enrollment_view(svc)
            elif choice == "5":
                list_enrollments_view(svc)
            elif choice == "0":
                break
            else:
                print("Invalid choice, please try again.")


# ADD ENROLLMENT
def add_enrollment_view(svc: EnrollmentService):
    print("\n=== ADD ENROLLMENT ===")
    enrollmentId = input("enrollment Id: ").strip()
    student_id = input("Student ID: ").strip()
    course_id = input("Course ID: ").strip()
    enrollment_day = input("Enrollment Day (YYYY-MM-DD): ").strip()
    grade = input("Grade (optional): ").strip()

    data = {
        "enrollmentId": enrollmentId,
        "studentId": student_id,
        "courseId": course_id,
        "enrollmentDay": enrollment_day,
        "grade": grade if grade else None
    }

    svc.add_enrollment(data)

 
# DELETE ENROLLMENT
def delete_enrollment_view(svc: EnrollmentService):
    print("\n=== DELETE ENROLLMENT ===")
    enrollment_id = input("Enter Enrollment ID to delete: ").strip()
    svc.delete_enrollment(enrollment_id)


# UPDATE ENROLLMENT
def update_enrollment_view(svc: EnrollmentService):
    print("\n=== UPDATE ENROLLMENT ===")
    enrollment_id = input("Enter Enrollment ID to update: ").strip()
    student_id = input("New Student ID (press Enter to skip): ").strip() or None
    course_id = input("New Course ID (press Enter to skip): ").strip() or None
    enrollment_day = input("New Enrollment Date (YYYY-MM-DD, press Enter to skip): ").strip() or None
    grade = input("New Grade (press Enter to skip): ").strip() or None

    data = {
        "studentId": student_id,
        "courseId": course_id,
        "enrollmentDay": enrollment_day,
        "grade": grade if grade else None
    }

    svc.update_enrollment(enrollment_id, data)


# SEARCH ENROLLMENT
def search_enrollment_view(svc: EnrollmentService):
    print("\n=== SEARCH ENROLLMENT ===")
    enrollment_id = input("Enter Enrollment ID: ").strip()
    svc.search_enrollment(enrollment_id)


# LIST ALL ENROLLMENTS
def list_enrollments_view(svc: EnrollmentService):
    print("\n=== ALL ENROLLMENTS ===")
    svc.list_enrollments()
