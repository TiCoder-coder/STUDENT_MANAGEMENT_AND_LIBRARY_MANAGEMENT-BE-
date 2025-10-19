from services.coursesService import CourseService
def course_menu(course_service, current_user):
    while True:
        print("\n=== COURSE MENU ===")

        # Neu teacher login thi hieu du CRUD
        if current_user["role"]:
            print("1. Add Course")
            print("2. Update Course")
            print("3. Delete Course")
            print("4. Search Course")
            print("5. List All Courses")
            print("0. Back")
        else:
            # Student chi cho xem va tim kiem thong tin 
            print("1. Search Course")
            print("2. List All Courses")
            print("0. Back")

        choice = input("Select: ").strip()

        try:
            # TEACHER MODE
            if current_user["role"]:
                if choice == "1":
                    add_course_view(course_service)
                elif choice == "2":
                    update_course_view(course_service)
                elif choice == "3":
                    delete_course_view(course_service)
                elif choice == "4":
                    search_course_view(course_service)
                elif choice == "5":
                    list_all_courses_view(course_service)
                elif choice == "0":
                    break
                else:
                    print("Invalid choice, please try again.")

            # STUDENT MODE
            else:
                if choice == "1":
                    search_course_view(course_service)
                elif choice == "2":
                    list_all_courses_view(course_service)
                elif choice == "0":
                    break
                else:
                    print("Invalid choice, please try again.")

        except Exception as e:
            print(f"Error in Course menu: {e}")


# Them khoa hoc
def add_course_view(svc):
    print("\n=== ADD COURSE ===")
    data = {
        "courseId": input("Course ID: ").strip(),
        "courseName": input("Course Name: ").strip(),
        "description": input("Description: ").strip(),
        "credits": input("Credits: ").strip(),
        "teacherId": input("Teacher ID (optional): ").strip() or None
    }
    svc.add_course(data)

# Tim kiem khoa hoc
def search_course_view(svc: CourseService):
    print("\n=== SEARCH COURSE ===")
    course_id = input("Enter course ID: ").strip()
    result = svc.search_course(course_id)

    if not result:
        print(f"[INFO] Course ID '{course_id}' not found.")
        return

    # In thong tin cua ket qua neu co
    if isinstance(result, dict):
        print(f"ID: {result['courseId']}, Name: {result['courseName']}, Desc: {result['description']}, Credits: {result['credits']}, TeacherID: {result['teacherId']}")
    else:
        print(f"ID: {result[0]}, Name: {result[1]}, Desc: {result[2]}, Credits: {result[3]}, TeacherID: {result[4]}")


# Liet ke tat ca cac khoa hoc
def list_all_courses_view(svc):
    print("\n=== COURSE LIST ===")
    result = svc.get_all_courses()

    if not result:
        print("[INFO] No courses found.")
        return

    for c in result:
        if isinstance(c, dict):
            print(f"ID: {c['courseId']}, Name: {c['courseName']}, Desc: {c['description']}, Credits: {c['credits']}, TeacherID: {c['teacherId']}")
        else:
            print(f"ID: {c[0]}, Name: {c[1]}, Desc: {c[2]}, Credits: {c[3]}, TeacherID: {c[4]}")

# Cap nhap tat ca cac khoa hoc
def update_course_view(svc):
    print("\n=== UPDATE COURSE ===")
    data = {
        "courseId": input("Enter course ID to update: ").strip(),
        "courseName": input("New Course Name (optional): ").strip() or None,
        "description": input("New Description (optional): ").strip() or None,
        "credits": input("New Credits (optional): ").strip() or None,
        "teacherId": input("New Teacher ID (optional): ").strip() or None
    }
    svc.update_course(data)

# Xoa khoa hoc
def delete_course_view(svc):
    print("\n=== DELETE COURSE ===")
    course_id = input("Enter course ID to delete: ").strip()
    svc.delete_course(course_id)



