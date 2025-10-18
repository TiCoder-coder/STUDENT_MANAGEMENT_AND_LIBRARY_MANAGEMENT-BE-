from models.erollmentModel import Enrollment
from auth import require_teacher # Goi ham kiem tra quyen tu auth de kiem tra 

# CLASS ENROLLEMENTSERVICE SE GOI LAI CAC HAM CUA MODEL VA THUC THI NO VA PHAN QUYEN SU DUNG--------
class EnrollmentService:
    
    # Khoi tao phuong tuc
    def __init__(self, db):
        self.db = db

   # Goi ham them cac enrollement --- CHI CO TEACHER THUC HIEN
    def add_enrollment(self, data: dict):
        try:
            # Kiem tra quyen 
            try:
                require_teacher()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            # Kiem tra va chuan hoa du lieu
            grade = data.get("grade")
            if grade is not None:
                try:
                    grade = float(grade)
                    if not (0.0 <= grade <= 10.0):
                        print("[VALIDATION ERROR] Grade must be between 0.0 and 10.0.")
                        return
                except ValueError:
                    print("[VALIDATION ERROR] Grade must be a number.")
                    return

            # Lay du lieu
            enrollment = Enrollment(
                enrollmentId=data.get("enrollmentId"),
                studentId=data.get("studentId"),
                courseId=data.get("courseId"),
                enrollmentDay=data.get("enrollmentDay"),
                grade=grade
            )

            result = enrollment.enroll(self.db)
            print(result)

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to add enrollment: {e}")

    
    # Goi ham hien thi thong tin cac enrrollement --- Ham mo ai cung duoc goi
    def search_enrollment(self, enrollmentId):
        try:
            if not enrollmentId:
                print("[ERROR] Enrollment ID is required.")
                return

            # Goi ham tim kiem tu model
            results = Enrollment.search_enrollment(self.db, enrollmentId)
            if not results:
                print("[INFO] No enrollment found with that ID.")
                return

            # In ra cac header de hien thi thong tin theo form
            print("\n{:<15} {:<12} {:<12} {:<20} {:<6}".format(
                "EnrollID", "StudID", "CourseID", "EnrollDay", "Grade"
            ))
            print("-" * 75)

            # Duyet qu cac thong tin va in ra
            for r in results:
                if isinstance(r, dict):
                    eid = r.get("enrollmentId") or r.get("enrollmenId") or r.get("id")  # linh hoạt
                    sid = r.get("studentId")
                    cid = r.get("courseId")
                    eday = r.get("enrollmentDay")
                    grade = r.get("grade")
                else:
                    eid = r[0] if len(r) > 0 else "-"
                    sid = r[1] if len(r) > 1 else "-"
                    cid = r[2] if len(r) > 2 else "-"
                    eday = r[3] if len(r) > 3 else "-"
                    grade = r[4] if len(r) > 4 else None

                # Format lai cho cac gia tri (an toan khi in ra --- tranh cac loi rui ro)
                eday_str = str(eday) if eday is not None else "-"
                grade_str = str(grade) if grade is not None else "-"

                print("{:<15} {:<12} {:<12} {:<20} {:<6}".format(
                    eid, sid, cid, eday_str, grade_str
                ))
        # Bat loi khi tim kiem
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to search enrollment: {e}")



    # Goi ham hien thi thong tin cua tat ca cac enrrollement --- Ham mo ai cung duoc goi
    def list_enrollments(self):
        try:
            rows = Enrollment.get_all_enrollments(self.db)
            if not rows:
                print("[INFO] No enrollments found.")
                return

            # In ra cac header de hien thi thong tin theo form
            print("\n{:<15} {:<12} {:<12} {:<20} {:<6}".format(
                "EnrollID", "StudID", "CourseID", "EnrollDay", "Grade"
            ))
            print("-" * 75)

            # Duyet qu cac thong tin va in ra
            for r in rows:
                if isinstance(r, dict):
                    eid = r.get("enrollmentId") or r.get("id") or "-"
                    sid = r.get("studentId") or "-"
                    cid = r.get("courseId") or "-"
                    eday = r.get("enrollmentDay") or "-"
                    grade = r.get("grade")
                else:
                    eid = r[0] if len(r) > 0 else "-"
                    sid = r[1] if len(r) > 1 else "-"
                    cid = r[2] if len(r) > 2 else "-"
                    eday = r[3] if len(r) > 3 else "-"
                    grade = r[4] if len(r) > 4 else None

                eday_str = str(eday) if eday is not None else "-"
                grade_str = str(grade) if grade is not None else "-"

                # Format lai cho cac gia tri (an toan khi in ra --- tranh cac loi rui ro)
                print("{:<15} {:<12} {:<12} {:<20} {:<6}".format(
                    eid, sid, cid, eday_str, grade_str
                ))
        # Bat loi khi hien thi tat ca cac thong tin 
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to list enrollments: {e}")
    
    
    # Goi ham cap nhap thong tin cua cac enrrollement --- Ham mo ai cung duoc goi
    def update_enrollment(self, enrollmentId: str, data: dict):
        try:
            try:
                # Kiem tra quyen 
                require_teacher()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            grade = data.get("grade")
            if grade is not None:
                try:
                    grade = float(grade)
                    if not (0.0 <= grade <= 10.0):
                        print("[VALIDATION ERROR] Grade must be between 0.0 and 10.0.")
                        return
                except ValueError:
                    print("[VALIDATION ERROR] Grade must be a number.")
                    return
            # Lay du lieu
            result = Enrollment.update_enrollment(
                self.db,
                enrollmentId,
                studentId=data.get("studentId"),
                courseId=data.get("courseId"),
                enrollmentDay=data.get("enrollmentDay"),
                grade=grade
            )
            print(result)
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to update enrollment: {e}")
            
             
    # Goi ham xoa thong tin cua cac enrrollement --- Ham mo ai cung duoc goi
    def delete_enrollment(self, enrollmentId: str):
        try:
            try:
                # Kiem tra quyen 
                require_teacher()
            except PermissionError as e:
                print(f"[AUTH ERROR] {e}")
                return

            success = Enrollment.delete_enrollment(self.db, enrollmentId)
            if success:
                print("[SUCCESS] Enrollment deleted successfully.")
            else:
                print("[ERROR] Enrollment ID not found.")
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to delete enrollment: {e}")

    

    

