from models.studentsModel import Student
from auth import require_teacher # Goi ham kiem tra quyen tu auth de kiem tra 

# CLASS STUDENTSERVICE SE GOI LAI CAC HAM CUA MODEL VA THUC THI NO VA PHAN QUYEN SU DUNG--------
class StudentService:
    
    # Khoi tao phuong tuc
    def __init__(self, db):
        self.db = db

    # Goi ham them cac student --- CHI CO TEACHER THUC HIEN
    def add_student(self, data: dict):
        try:
            # Kiem tra quyen 
            require_teacher()
            required = ["studentId", "fullName", "birthday", "email", "phoneNumber", "address"]
            for f in required:
                if not data.get(f):
                    print(f"[VALIDATION] Missing field: {f}")
                    return

            student = Student(**data)
            student.add_student(self.db)
        except PermissionError as e:
            print(f"[AUTH ERROR] {e}")
        except Exception as e:
            print(f"[SERVICE ERROR] {e}")

    # Goi ham tim kiem thong tin cac sinh vien --- CHI CO TEACHER THUC HIEN
    def search_student(self, studentId: str):
        try:
            return Student.search_student(self.db, studentId)
        except Exception as e:
            print(f"[SERVICE ERROR] {e}")
            return []

    # Goi ham hien thi thong tin cua tat ca cac sinh vien --- CHI CO TEACHER THUC HIEN
    def get_all_students(self):
        try:
            return Student.get_all_students(self.db)
        except Exception as e:
            print(f"[SERVICE ERROR] {e}")
            return []
        
    # Goi lai ham lay tat ca de thuc thi
    def fetch_all(self, *args, **kwargs):
        return self.get_all_students()
   
   
    # Goi lai ham cap nhap thong tin cho student --- CHI CO TEACHER THUC HIEN 
    def update_student(self, data: dict):
        try:
            # Kiem tra quyen 
            require_teacher()
            if not data.get("studentId"):
                print("[VALIDATION] Missing studentId.")
                return

            student = Student(**data)
            student.update_student(self.db)
        except PermissionError as e:
            print(f"[AUTH ERROR] {e}")
        except Exception as e:
            print(f"[SERVICE ERROR] {e}")

    # Goi lai ham xoa thong tin cho student --- CHI CO TEACHER THUC HIEN 
    def delete_student(self, studentId: str):
        try:
            # Kiem tra quyen 
            require_teacher()
            Student.delete_student(self.db, studentId)
        except PermissionError as e:
            print(f"[AUTH ERROR] {e}")
        except Exception as e:
            print(f"[SERVICE ERROR] {e}")

    