from services.managersService import ManagerService
import bcrypt
from decouple import config

current_user = {
    "username": None,
    "role": None
}


# ---------------------------------------------------------------------------------------------------
# HÀM ĐĂNG NHẬP HỆ THỐNG
# ---------------------------------------------------------------------------------------------------
def login(db=None):
    """
    Cho phép người dùng đăng nhập với username + password.
    Kiểm tra:
        - Manager đăng nhập từ .env hoặc database.
        - Member đăng nhập từ database.
    """
    global current_user

    # Nếu đã đăng nhập rồi thì không cần login lại
    if current_user.get("username"):
        print(f"✅ Already logged in as {current_user['username']} ({current_user['role']}).")
        return True

    print("\n=== 🔐 LOGIN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    try:
        # --------------------- ĐĂNG NHẬP BẰNG .ENV (MANAGER ADMIN MẶC ĐỊNH) ---------------------
        env_user = config("USER_NAME", default=None)
        env_pass = config("PASSWORD", default=None)

        if username == env_user and password == env_pass:
            current_user["username"] = username
            current_user["role"] = "manager"
            print(f"[ADMIN LOGIN] Welcome, {username}!")
            return True

        # --------------------- ĐĂNG NHẬP TỪ DATABASE (MANAGER HOẶC MEMBER) ---------------------
        if db:
            svc = ManagerService(db)

            # Lấy thông tin manager trong database
            sql_manager = db.fetch_one(
                "SELECT * FROM managers WHERE username = %s", (username,)
            )

            # Lấy thông tin member trong database
            sql_member = db.fetch_one(
                "SELECT * FROM members WHERE username = %s", (username,)
            )

            # ---- KIỂM TRA MANAGER ----
            if sql_manager:
                stored_hash = sql_manager["password"].encode("utf-8")
                if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                    current_user["username"] = sql_manager["username"]
                    current_user["role"] = "manager"
                    print(f"✅ Login successful! Welcome Manager {sql_manager['full_name']}!")
                    return True

            # ---- KIỂM TRA MEMBER ----
            elif sql_member:
                stored_hash = sql_member["password"].encode("utf-8")
                if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                    current_user["username"] = sql_member["username"]
                    current_user["role"] = "member"
                    print(f"✅ Login successful! Welcome Member {sql_member['full_name']}!")
                    return True

        # Nếu không tìm thấy tài khoản hợp lệ
        print("❌ Invalid username or password.")
        return False

    except Exception as e:
        print(f"[AUTH ERROR] Login failed: {e}")
        return False


# ---------------------------------------------------------------------------------------------------
# HÀM ĐĂNG XUẤT HỆ THỐNG
# ---------------------------------------------------------------------------------------------------
def logout():
    """
    Đăng xuất khỏi hệ thống, reset lại current_user.
    """
    global current_user
    if current_user["username"]:
        print(f"👋 Logged out ({current_user['username']}) successfully.")
    else:
        print("No user currently logged in.")
    current_user["username"] = None
    current_user["role"] = None


# ---------------------------------------------------------------------------------------------------
# KIỂM TRA QUYỀN MANAGER (ADMIN)
# ---------------------------------------------------------------------------------------------------
def require_manager(db=None):
    """
    Dùng để kiểm tra quyền của Manager.
    Nếu chưa đăng nhập -> yêu cầu login.
    Nếu không phải Manager -> từ chối quyền truy cập.
    """
    global current_user

    if not current_user.get("username"):
        print("⚠️ This action requires manager login.")
        if not login(db):
            print("🚫 Access denied.")
            return False

    if current_user.get("role") != "manager":
        print("🚫 Permission denied: Only managers can perform this action.")
        return False

    return True


# ---------------------------------------------------------------------------------------------------
# KIỂM TRA QUYỀN MEMBER (NGƯỜI DÙNG THƯỜNG)
# ---------------------------------------------------------------------------------------------------
def require_member(db=None):
    """
    Dùng để kiểm tra quyền của Member.
    Nếu chưa đăng nhập -> yêu cầu login.
    Nếu không phải Member -> từ chối quyền truy cập.
    """
    global current_user

    if not current_user.get("username"):
        print("⚠️ This action requires member login.")
        if not login(db):
            print("🚫 Access denied.")
            return False

    if current_user.get("role") != "member":
        print("🚫 Permission denied: Only members can perform this action.")
        return False

    return True
