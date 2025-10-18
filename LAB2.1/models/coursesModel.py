# CLASS COURSE: QUAN LI THONG TIN CAC KHOA HOC --------------------------------------------------------------------------

class Course:
    
    # Ham khoi tao dung de khoi tao cac thuoc tinh cho Course ----------------------------------------------------------
    def __init__(self, courseId, courseName, description, credits, teacherId=None):
        self.courseId = courseId
        self.courseName = courseName
        self.description = description
        self.credits = credits
        self.teacherId = teacherId


    # Them mot khoa hoc moi ---------------------------------------------------------------------------------------------
    def add_course(self, db):
        try:
            # Kiem tra courseId da ton tai hay chua --- Neu ton tai -> False
            existing = db.fetch_one("SELECT * FROM courses WHERE courseId = %s", (self.courseId,))
            if existing:
                print(f"[ERROR] Course ID '{self.courseId}' already exists.")
                return

            # Kiem tra teacherId co ton tai khong --- Neu co -> True
            if self.teacherId:
                teacher_exists = db.fetch_one("SELECT * FROM teachers WHERE teacherId = %s", (self.teacherId,))
                if not teacher_exists:
                    print(f"[ERROR] Teacher ID '{self.teacherId}' does not exist.")
                    return

            # Them course vao database
            sql = """
                INSERT INTO courses (courseId, courseName, description, credits, teacherId)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            # Goi ham excite_query de thuc thi
            db.execute_query(sql, (self.courseId, self.courseName, self.description, self.credits, self.teacherId))
            print(f"[SUCCESS] Course '{self.courseName}' added successfully!")

        # Bat loi neu co loi xay ra
        except Exception as e:
            print(f"[ERROR] Failed to add course: {e}")


    # Tim kiem mot khoa hoc theo courseId---------------------------------------------------------------------------------
    @staticmethod
    def search_course(db, courseId):
        try:
            sql = "SELECT * FROM courses WHERE courseId = %s"
            result = db.fetch_one(sql, (courseId,))
            return result
        except Exception as e:
            print(f"[ERROR] Failed to search course: {e}")
            return None


    # Lay thong tin tat ca cac khoa hoc ----------------------------------------------------------------------------------
    @staticmethod
    def get_all_courses(db):
        try:
            # Goi request lay tat ca cac thong tin
            courses = db.fetch_all("SELECT * FROM courses")
            
            # Neu khong co courses nao (database rong) -> tra ve rong
            if not courses:
                print("[INFO] No courses found.")
                return []
            # Neu co thi tra ve courses
            return courses
        
        # Bat loi khi lay tat ca thong tin
        except Exception as e:
            print(f"[ERROR] Failed to fetch courses: {e}")
            return []


    # Cap nhap thong tin khoa hoc (cac thuoc tinh cap nhap -- tuy chon )--------------------------------------------------
    @staticmethod
    def update_course(db, courseId, courseName=None, description=None, credits=None, teacherId=None):
        try:
            
            # Kiem tra xem courseId co ton tai khong --- Neu ton tai -> True: co the xoa
            existing = db.fetch_one("SELECT * FROM courses WHERE courseId = %s", (courseId,))
            if not existing:
                print(f"[ERROR] Course ID '{courseId}' does not exist.")
                return

            # Tao 2 list dung de luu tru cac thuoc tinh can cap nhap va luu tru lai cap nhap mot lan
            updates = []
            params = []

            # Kiem tra co nhap courseName moi khong
            if courseName:
                updates.append("courseName=%s")
                params.append(courseName)
                
            # Kiem tra co nhap description moi khong
            if description:
                updates.append("description=%s")
                params.append(description)
            
            # Kiem tra co nhap credits moi khong
            if credits is not None:
                updates.append("credits=%s")
                params.append(credits)
            
            # Kiem tra co nhap teacherId moi khong --- Neu co nhap thi kiem tra xem teacherId do co ton tai khong
            if teacherId:
                teacher_exists = db.fetch_one("SELECT * FROM teachers WHERE teacherId = %s", (teacherId,))
                if not teacher_exists:
                    print(f"[ERROR] Teacher ID '{teacherId}' does not exist.")
                    return
                # Neu dung co teacherId do thi cap nhap lai
                updates.append("teacherId=%s")
                params.append(teacherId)

            # Neu list rong --> khong co thong tin nao de cap nhap 
            if not updates:
                print("[INFO] No fields provided to update.")
                return

            # Neu co thi cap nhap
            sql = f"UPDATE courses SET {', '.join(updates)} WHERE courseId=%s"
            params.append(courseId)
            db.execute_query(sql, tuple(params))
            print(f"[SUCCESS] Course '{courseId}' updated successfully!")
        
        # Bat loi neu xay ra loi khi update
        except Exception as e:
            print(f"[ERROR] Failed to update course: {e}")


    # Xoa mot khoa hoc --- Xoa theo courseId------------------------------------------------------------------------------
    @staticmethod
    def delete_course(db, courseId):
        try:
            # Kiem tra courseId co ton tai trong database khong
            existing = db.fetch_one("SELECT * FROM courses WHERE courseId = %s", (courseId,))
            
            # Neu khong co thi bao loi
            if not existing:
                print(f"[ERROR] Course ID '{courseId}' does not exist.")
                return
            
            # Thc thi lenh xoa
            db.execute_query("DELETE FROM courses WHERE courseId = %s", (courseId,))
            print(f"[SUCCESS] Course '{courseId}' deleted successfully!")

        # Bat loi neu xay ra loi
        except Exception as e:
            print(f"[ERROR] Failed to delete course: {e}")
