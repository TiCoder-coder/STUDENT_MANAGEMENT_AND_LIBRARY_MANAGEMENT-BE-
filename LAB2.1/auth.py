from decouple import config
from services.teacherService import TeacherService
import bcrypt


# Bien toan cuc luu thong tin nguoi dang nhap hien tai
current_user = {
    "username": None,
    "role": None
}

# DANG NHAP
def login(db=None):
    
    # yeu cau nguoi dung nhap tai khoan va kiem tra database/env
    global current_user

    # Neu da ton tai thi ---> True
    if current_user.get("username"):
        print(f"Already logged in as {current_user['username']}.")
        return True

    print("\n=== LOGIN REQUIRED ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    try:
        # Kiem tra trong .env 
        env_user = config("USER_NAME", default=None)
        env_pass = config("PASSWORD", default=None)
        if username == env_user and password == env_pass:
            current_user["username"] = username
            current_user["role"] = "teacher"
            print(f"[ADMIN LOGIN] Welcome {username}!")
            return True

        # Kiem tra trong database teacher
        if db:
            svc = TeacherService(db)
            
            # Lay teacher theo userName ( khoa khong trung)
            teacher = svc.get_teacher_by_username(username)
            if teacher:
                # Chuan lai mat khau cu de kiem tra
                if bcrypt.checkpw(password.encode('utf-8'), teacher.password.encode('utf-8')):
                    current_user["username"] = teacher.username
                    current_user["role"] = "teacher"
                    print(f"Login successful. Welcome, {teacher.name}!")
                    return True

        print("Invalid username or password.")
        return False

    except Exception as e:
        print(f"️ Login error: {e}")
        return False


# DANG XUAT
def logout():
    global current_user
    if current_user["username"]:
        print(f"Logged out ({current_user['username']})")
    current_user["username"] = None
    current_user["role"] = None

# KIEM TRA GIAO VIEN
def require_teacher(db=None):
    global current_user

    if not current_user.get("username"):
        print("This action requires teacher login.")
        logged_in = login(db)
        if not logged_in:
            print("Access denied.")
            return False

    if current_user.get("role") != "teacher":
        print("Permission denied: Only teachers can perform this action.")
        return False

    return True
