from services.managersService import ManagerService
import bcrypt
from decouple import config

current_user = {
    "username": None,
    "role": None
}


# ---------------------------------------------------------------------------------------------------
# HAM DUNG DE DANG  NHAP TREN HE THONG
# ---------------------------------------------------------------------------------------------------
def login(db=None):
    global current_user

    # Neu da dang nhap roi thi khong can dang nhap lai
    if current_user.get("username"):
        print(f"Already logged in as {current_user['username']} ({current_user['role']}).")
        return True

    print("\n=== LOGIN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    try:
        # --------------------- DANG NHAP BANG .ENV (MANAGER ADMIN MAC DINH) ---------------------
        env_user = config("USER_NAME", default=None)
        env_pass = config("PASSWORD", default=None)

        if username == env_user and password == env_pass:
            current_user["username"] = username
            current_user["role"] = "manager"
            print(f"[ADMIN LOGIN] Welcome, {username}!")
            return True

        # --------------------- DANG NHAP TU  DATABASE (MANAGER HOẶC MEMBER) ---------------------
        if db:
            svc = ManagerService(db)

            # Lay thong tin manager trong database
            sql_manager = db.fetch_one(
                "SELECT * FROM managers WHERE username = %s", (username,)
            )

            # Lay thong tin member trong database
            sql_member = db.fetch_one(
                "SELECT * FROM members WHERE username = %s", (username,)
            )

            # ---- KIEM TRA MANAGER ----
            if sql_manager:
                stored_hash = sql_manager["password"].encode("utf-8")
                if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                    current_user["username"] = sql_manager["username"]
                    current_user["role"] = "manager"
                    print(f"Login successful! Welcome Manager {sql_manager['full_name']}!")
                    return True

            # ---- KIEM TRA MEMBER ----
            elif sql_member:
                stored_hash = sql_member["password"].encode("utf-8")
                if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                    current_user["username"] = sql_member["username"]
                    current_user["role"] = "member"
                    print(f"Login successful! Welcome Member {sql_member['full_name']}!")
                    return True

        # Neu khong tim thay thi tai khoan khong hop le
        print("Invalid username or password.")
        return False

    except Exception as e:
        print(f"[AUTH ERROR] Login failed: {e}")
        return False


# ---------------------------------------------------------------------------------------------------
# HAM DUNG DE DANG XUAT
# ---------------------------------------------------------------------------------------------------
def logout():
    global current_user
    if current_user["username"]:
        print(f"Logged out ({current_user['username']}) successfully.")
    else:
        print("No user currently logged in.")
    current_user["username"] = None
    current_user["role"] = None


# ---------------------------------------------------------------------------------------------------
# KIEM TRA QUYEN MANAGER (ADMIN)
# ---------------------------------------------------------------------------------------------------
def require_manager(db=None):

    global current_user

    if not current_user.get("username"):
        print("This action requires manager login.")
        if not login(db):
            print("Access denied.")
            return False

    if current_user.get("role") != "manager":
        print("Permission denied: Only managers can perform this action.")
        return False

    return True


# ---------------------------------------------------------------------------------------------------
# KIEM TRA QUYEN MEMBER 
# ---------------------------------------------------------------------------------------------------
def require_member(db=None):

    global current_user

    if not current_user.get("username"):
        print("This action requires member login.")
        if not login(db):
            print("Access denied.")
            return False

    if current_user.get("role") != "member":
        print("Permission denied: Only members can perform this action.")
        return False

    return True
