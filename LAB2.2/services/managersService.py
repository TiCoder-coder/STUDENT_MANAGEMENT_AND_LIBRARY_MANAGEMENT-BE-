from models.managersModel import Manager
import bcrypt

# CLASS MANAGERSERVICE SE GOI LAI CAC HAM CUA MODEL VA THUC THI NO VA PHAN QUYEN SU DUNG -------------------------------
class ManagerService:
    
    # Ham khoi tao phuong thuc ----------------------------------------------------------------------------------------
    def __init__(self, db):
        self.db = db

    # Ham dung de them mot manager moi --- CHI CO ADMIN THUC HIEN -----------------------------------------------------
    def add_manager(self, data: dict):
        try:
            # Kiem tra cac truong bat buoc
            required_fields = [
                "manager_id", "full_name", "email",
                "username", "password", "phoneNumber"
            ]
            for field in required_fields:
                if not data.get(field):
                    print(f"[VALIDATION ERROR] Missing required field: {field}")
                    return False

            # Tao doi tuong Manager tu du lieu dau vao
            m = Manager(
                manager_id=data.get("manager_id"),
                full_name=data.get("full_name"),
                email=data.get("email"),
                username=data.get("username"),
                password=data.get("password"),
                phoneNumber=data.get("phoneNumber"),
                created_at=data.get("created_at")
            )

            # Goi ham add_manager trong model
            m.add_manager(self.db)
            print(f"[INFO] Manager '{data.get('full_name')}' added successfully.")
            return True

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to add manager: {e}")
            return False

    # Ham dung de lay thong tin tat ca cac manager --- CHI CO ADMIN THUC HIEN -----------------------------------------
    def get_all_managers(self):
        try:
            managers = Manager.get_all_managers(self.db)
            if not managers:
                print("[INFO] No managers found in database.")
                return []
            return managers
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to list managers: {e}")
            return []

    # Ham dung de tim kiem manager theo ID --- CHI CO ADMIN THUC HIEN --------------------------------------------------
    def search_manager(self, manager_id: str):
        try:
            manager = Manager.search_manager(self.db, manager_id)
            if not manager:
                print(f"[INFO] No manager found with ID '{manager_id}'.")
                return None
            return manager
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to search manager: {e}")
            return None

    # Ham dung de cap nhat thong tin cua mot manager --- CHI CO ADMIN THUC HIEN ----------------------------------------
    def update_manager(self, data: dict):
        try:
            if not data.get("manager_id"):
                print("[VALIDATION ERROR] Missing manager_id for update.")
                return False

            m = Manager(
                manager_id=data.get("manager_id"),
                full_name=data.get("full_name"),
                email=data.get("email"),
                username=data.get("username"),
                password=data.get("password"),
                phoneNumber=data.get("phoneNumber"),
                created_at=data.get("created_at")
            )

            m.update_manager(self.db)
            print(f"[INFO] Manager '{data.get('manager_id')}' updated successfully.")
            return True

        except Exception as e:
            print(f"[SERVICE ERROR] Failed to update manager: {e}")
            return False

    # Ham dung de xoa mot manager --- CHI CO ADMIN THUC HIEN ------------------------------------------------------------
    def delete_manager(self, manager_id: str):
        try:
            Manager.delete_manager(self.db, manager_id)
            print(f"[INFO] Manager '{manager_id}' deleted successfully.")
            return True
        except Exception as e:
            print(f"[SERVICE ERROR] Failed to delete manager: {e}")
            return False

    # Ham dung de dang nhap vao he thong bang username + password (hash bcrypt) ----------------------------------------
    def login(self, username: str, password: str):
        try:
            # Kiem tra thong tin manager bang userName
            sql_manager = self.db.fetch_one(
                "SELECT * FROM managers WHERE username=%s", (username,)
            )

            # Kiem tra xem manager co ton tai khong
            if not sql_manager:
                print("Invalid username or password.")
                return False

            # Lay password hash tu database len de kiem tra
            stored_hash = sql_manager["password"].encode("utf-8")

            # So sanh mat khau trong database voi nguoi dung nhap xem co dung khong
            if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                print(f"Login successful! Welcome, {sql_manager['full_name']}!")
                return True
            else:
                print("Invalid username or password.")
                return False

        except Exception as e:
            print(f"[SERVICE ERROR] Error during manager login: {e}")
            return False
