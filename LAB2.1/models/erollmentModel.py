from datetime import datetime

# CLASS ENROLLMENT: DUNG DE QUAN LI THONG TIN CUA CAC ENROLLMENT ------------------------------------------------------------------
class Enrollment:
    
    # Ham dung de khoi tao cac thuoc tinh cho enrollment
    def __init__(self, enrollmentId, studentId, courseId, enrollmentDay=None, grade=None):
        self.enrollmentId = enrollmentId
        self.studentId = studentId
        self.courseId = courseId
        self.enrollmentDay = enrollmentDay or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.grade = grade

    # Ham dung de them mot erollment
    def enroll(self, db):
        try:
            
            # Kiem tra enrollmentId da ton tai hay chua -- Neu ton tai -> False
            existing = db.fetch_one("SELECT * FROM enrollments WHERE enrollmentId=%s", (self.enrollmentId,))
            if existing:
                return "[ERROR] Enrollment ID already exists."

            # Kiem tra studentId co ton tai khong --- Neu ton tai -> True
            student_exists = db.fetch_one("SELECT * FROM students WHERE studentId=%s", (self.studentId,))
            if not student_exists:
                return "[ERROR] Student ID not found."

            # Kiem tra courseId co ton tai khong --- Neu ton tai -> True
            course_exists = db.fetch_one("SELECT * FROM courses WHERE courseId=%s", (self.courseId,))
            if not course_exists:
                return "[ERROR] Course ID not found."

            # Sau khi kiem tra neu hop le thi them vao
            sql = """
                INSERT INTO enrollments (enrollmentId, studentId, courseId, enrollmentDay, grade)
                VALUES (%s, %s, %s, %s, %s)
            """
            db.execute_query(sql, (self.enrollmentId, self.studentId, self.courseId, self.enrollmentDay, self.grade))
            return "[SUCCESS] Enrollment added successfully!"
        
        # Bat loi 
        except Exception as e:
            return f"[ERROR] Failed to add enrollment: {e}"

    # Ham dung de tim kiem thong in cua enrollement---------------------------------------------------------------------------------
    @staticmethod
    def search_enrollment(db, enrollmentId=None, studentId=None, courseId=None):
        try:
            sql = "SELECT * FROM enrollments WHERE "
            params, conditions = [], []
            # Ham dung de kiem tra xem nguoi dung muon tim kiem enrollment theo enrollmentId hay studentId hay courseId 
            if enrollmentId:
                conditions.append("enrollmentId=%s")
                params.append(enrollmentId)
            if studentId:
                conditions.append("studentId=%s")
                params.append(studentId)
            if courseId:
                conditions.append("courseId=%s")
                params.append(courseId)

            if not conditions:
                return []

            # Sau khi xac nhan nguoi dung muon tim kiem theo nao thi join vao va thuc thi
            sql += " OR ".join(conditions)
            return db.fetch_all(sql, tuple(params))
        
        # Bat loi chung chung
        except Exception:
            return []

    # Ham dung de lay tat ca cac thong tin cua enrollment---------------------------------------------------------------------------
    @staticmethod
    def get_all_enrollments(db):
        try:
            # Goi toi database de lay tat ca thong tin
            return db.fetch_all("SELECT * FROM enrollments")
        except Exception:
            return []
    
    # Ham dung de cap nhap cho enrollment----------------------------------------------------------------------------------------- 
    @staticmethod
    def update_enrollment(db, enrollmentId, studentId=None, courseId=None, enrollmentDay=None, grade=None):
        try:
            # Kiem tra enrollment co ton tai khong de cap nhap
            existing = db.fetch_one("SELECT * FROM enrollments WHERE enrollmentId=%s", (enrollmentId,))
            if not existing:
                return "[ERROR] Enrollment ID not found."

            # Tao 2 list de luu tru gia tri: cai nao teacher muon cap nhap thi nhap vao >< Bo qua
            fields, params = [], []
            if studentId:
                fields.append("studentId=%s")
                params.append(studentId)
            if courseId:
                fields.append("courseId=%s")
                params.append(courseId)
            if enrollmentDay:
                fields.append("enrollmentDay=%s")
                params.append(enrollmentDay)
            if grade is not None:
                fields.append("grade=%s")
                params.append(grade)

            if not fields:
                return "[INFO] No fields to update."

            # Cap nhap cac thuoc tinh can cap nhap
            sql = f"UPDATE enrollments SET {', '.join(fields)} WHERE enrollmentId=%s"
            params.append(enrollmentId)
            db.execute_query(sql, tuple(params))
            return "[SUCCESS] Enrollment updated successfully!"
        # Bat loi cap nhap
        except Exception as e:
            return f"[ERROR] Failed to update enrollment: {e}"

 
    # Ham dung de xoa thong tin cua 1 enrollement theo enrollementId-----------------------------------------------------------------
    @staticmethod
    def delete_enrollment(db, enrollmentId):
        try:
            # Check xem enrollmentId do co ton tai khong de xoa
            check = db.fetch_one("SELECT * FROM enrollments WHERE enrollmentId=%s", (enrollmentId,))
            if not check:
                return False
            # Neu co thi goi phuong thuc delete toi database de xoa
            db.execute_query("DELETE FROM enrollments WHERE enrollmentId=%s", (enrollmentId,))
            return True
        
        # Bat loi xoa
        except Exception:
            return False

    