from models.teachersModels import Teacher
import bcrypt

# CLASS TEACHERSERVICE SE GOI LAI CAC HAM CUA MODEL VA THUC THI NO VA PHAN QUYEN SU DUNG--------
class TeacherService:
    
    # Khoi tao phuong tuc
    def __init__(self, db):
        self.db = db

    # Goi ham them cac teacher --- CHI CO TEACHER THUC HIEN
    def add_teacher(self, data: dict):
        try:
            required_fields = [
                "teacherId", "fullName", "birthday",
                "email", "phoneNumber", "address",
                "userName", "password"
            ]
            
            for field in required_fields:
                if not data.get(field):
                    print(f"[VALIDATION ERROR] Missing required field: {field}")
                    return False

            # Dam bao db luon la doi tuong database
            db_conn = self.db
            
            # Lay du lieu
            t = Teacher(
                teacherId=data.get("teacherId"),
                fullName=data.get("fullName"),
                birthday=data.get("birthday"),
                email=data.get("email"),
                phoneNumber=data.get("phoneNumber"),
                address=data.get("address"),
                userName=data.get("userName"),
                password=data.get("password")
            )
            t.add_teacher(db_conn)
            print(f"[INFO] Teacher '{data.get('fullName')}' added successfully.")
            return True
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to add teacher: {e}")
            return False

    # Ham dung de lay thong tin cua tat ca cac giao vien --- Chi co giao vien moi thuc hien duoc
    def get_all_teachers(self):
        try:
            teachers = Teacher.get_all_teachers(self.db)
            if not teachers:
                print("[INFO] No teachers found in database.")
                return []
            return teachers
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to list teachers: {e}")
            return []

    # Ham dung de tim kiem thong tin cua cac giao vien --- Chi co giao vien moi thuc hien duoc
    def search_teacher(self, teacherId: str):
        try:
            teacher = Teacher.search_teacher(self.db, teacherId)
            if not teacher:
                print(f"[INFO] No teacher found with ID '{teacherId}'.")
                return None
            return teacher
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to search teacher: {e}")
            return None
        
        
    # Ham dung de cap nhap thong tin cua cac giao vien --- Chi co giao vien moi thuc hien duoc
    def update_teacher(self, data: dict):
        try:
            if not data.get("teacherId"):
                print("[VALIDATION ERROR] Missing teacherId for update.")
                return False
            
            # Lay du lieu
            t = Teacher(
                teacherId=data.get("teacherId"),
                fullName=data.get("fullName"),
                birthday=data.get("birthday"),
                email=data.get("email"),
                phoneNumber=data.get("phoneNumber"),
                address=data.get("address"),
                userName=data.get("userName"),
                password=data.get("password")
            )
            t.update_teacher(self.db)
            print(f"[INFO] Teacher '{data.get('teacherId')}' updated successfully.")
            return True
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to update teacher: {e}")
            return False

    # Ham dung de xoa thong tin cua cac giao vien --- Chi co giao vien moi thuc hien duoc
    def delete_teacher(self, teacherId: str):
        try:
            Teacher.delete_teacher(self.db, teacherId)
            print(f"[INFO] Teacher '{teacherId}' deleted successfully.")
            return True
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to delete teacher: {e}")
            return False

    

    

    def login(self, userName: str, password: str):
        try:
            # Lay thong tin user theo userName
            sql_teacher = self.db.fetch_one(
                "SELECT * FROM teachers WHERE userName=%s", (userName,)
            )

            # Kiem tra xem teacher do co ton tai khong
            if not sql_teacher:
                print("Invalid username or password.")
                return False

            # Lay password hash tu database
            stored_hash = sql_teacher["password"].encode("utf-8")

            # Kiem tra password
            if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                print(f"Login successful! Welcome {sql_teacher['fullName']}!")
                return True
            else:
                print("Invalid username or password.")
                return False

        except Exception as e:
            print(f"[SERVICE ERROR] Error during teacher login: {e}")
            return False

