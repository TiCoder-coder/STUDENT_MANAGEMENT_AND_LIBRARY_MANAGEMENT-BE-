from models.coursesModel import Course
from auth import require_teacher # Goi ham kiem tra quyen tu auth de kiem tra 

# CLASS COURSESERVICE SE GOI LAI CAC HAM CUA MODEL VA THUC THI NO VA PHAN QUYEN SU DUNG--------
class CourseService:
    
    # Khoi tao phuong tuc
    def __init__(self, db):
        self.db = db

    # Goi ham them cac khoa hoc --- CHI CO TEACHER THUC HIEN
    def add_course(self, data: dict):
        try:
            # Kiem tra quyen 
            try:
                require_teacher()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            # Lay du lieu
            course = Course(
                courseId=data.get("courseId"),
                courseName=data.get("courseName"),
                description=data.get("description"),
                credits=data.get("credits"),
                teacherId=data.get("teacherId")
            )
            
            # Neu hop le thi them moi
            course.add_course(self.db)

        # Bat loi khi them moi
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to add course: {e}")

    # Goi ham hien thi thong tin cac khoa hoc --- Ham mo ai cung duoc goi
    def search_course(self, courseId: str):
        try:
            result = Course.search_course(self.db, courseId)
            return result
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to search course: {e}")
            return None


    # Goi ham hien thi thong tin tat ca cac khoa hoc --- Ham mo ai cung duoc goi
    def get_all_courses(self):
        try:
            courses = Course.get_all_courses(self.db)
            if not courses:
                print("[INFO] No courses available.")
                return []
            return courses
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to get courses: {e}")
            return []

    
    # Goi ham cap nhap cac khoa hoc --- CHI CO TEACHER THUC HIEN 
    def update_course(self, data):
        try:
            # Kiem tra quyen 
            require_teacher()

            courseId = data.get("courseId")
            if not courseId:
                print("[VALIDATION ERROR] Course ID is required.")
                return

            Course.update_course(
                self.db,
                courseId=courseId,
                courseName=data.get("courseName"),
                description=data.get("description"),
                credits=data.get("credits"),
                teacherId=data.get("teacherId")
            )
        # Bat loi khong dung quyen
        except PermissionError as e:
            print(f"[AUTH ERROR] {e}")
        # Bat loi chung chuhng 
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to update course: {e}")


    # Goi ham xoa thong tin cac khoa hoc --- CHI CO TEACHER THUC HIEN 
    def delete_course(self, courseId: str):
        try:
            try:
                require_teacher()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            Course.delete_course(self.db, courseId)

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to delete course: {e}")

