import re
import bcrypt
from datetime import datetime

# DANH SACH CAC NHA MANG PHO BIEN DUNG ĐE KIEM TRA SO ĐIEN THOAI CO HOP LE KHONG ----------------------------------------
NHA_MANG_DI_DONG = {
    'Viettel': ('096', '097', '098', '086', '032', '033', '034', '035', '036', '037', '038', '039'),
    'MobiFone': ('090', '093', '089', '070', '079', '077', '076', '078'),
    'VinaPhone': ('091', '094', '088', '083', '084', '085', '081', '082'),
    'Vietnamobile': ('092', '056', '058'),
    'Gmobile': ('099', '059'),
    'I-Telecom': ('087',),
    'Wintel': ('055',)
}

# HAM CHUÂA HOA HO TEN ĐE VIET HOA ĐUNG CU CAI ĐAU ---------------------------------------------------------------------
def chuan_hoa_ho_ten(ho_ten_raw: str) -> str:
    words = ho_ten_raw.strip().split()
    return " ".join([word.capitalize() for word in words])

# HAM KIEM TRA EMAIL CO ĐUNG ĐINH DANG VA PHAI LA GMAIL -----------------------------------------------------------------
def kiem_tra_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    return re.match(pattern, email) is not None

# HAM KIEM TRA SO ĐIEN THOAI HOP LE VA XAC ĐINH NHA MANG ----------------------------------------------------------------
def kiem_tra_so_dien_thoai(sdt: str) -> dict:
    sdt_sach = re.sub(r'\D', '', sdt)

    if sdt_sach.startswith('84'):
        sdt_sach = '0' + sdt_sach[2:]

    if not sdt_sach.startswith('0') or len(sdt_sach) != 10:
        return {'valid': False, 'reason': 'Phone number must have 10 digits and start with 0.'}

    dau_so = sdt_sach[:3]
    for ten_mang, cac_dau_so in NHA_MANG_DI_DONG.items():
        if dau_so in cac_dau_so:
            return {'valid': True, 'network': ten_mang, 'sdt_chuan_hoa': sdt_sach}

    if dau_so.startswith('02'):
        return {'valid': True, 'network': 'Desktop computer', 'sdt_chuan_hoa': sdt_sach}

    return {'valid': False, 'reason': f'Prefix number {dau_so} was not exited.'}

# CLASS MANAGER: DUNG ĐE QUAN LY CAC THONG TIN CUA MANAGER TRONG HE THONG ---------------------------------------------
class Manager:
    
    # Ham khoi tao cac thuoc tinh cho manager --------------------------------------------------------------------------
    def __init__(self, manager_id, full_name, email, username, password, phoneNumber, created_at=None):
        self.manager_id = manager_id
        self.full_name = chuan_hoa_ho_ten(full_name)
        self.email = email
        self.username = username
        self.password = password
        self.phoneNumber = phoneNumber
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # HAM DUNG ĐE KIEM TRA TINH HOP LE TRƯOC KHI THEM MOT MANAGER -------------------------------------------------------
    def validate(self, db):
        # Kiem tra xem id da ton tai hay chua
        existing_id = db.fetch_one("SELECT manager_id FROM managers WHERE manager_id=%s", (self.manager_id,))
        if existing_id:
            raise ValueError(f"Manager ID '{self.manager_id}' already exists in the system.")

        # Kiem tra userName co trung khong
        existing_username = db.fetch_one("SELECT username FROM managers WHERE username=%s", (self.username,))
        if existing_username:
            raise ValueError(f"Username '{self.username}' already exists in the system.")

        # Kiem tra email co trung hay sai dinh dang khong
        existing_email = db.fetch_one("SELECT email FROM managers WHERE email=%s", (self.email,))
        if existing_email:
            raise ValueError(f"Email '{self.email}' already exists in the system.")
        if not kiem_tra_email(self.email):
            raise ValueError("Email is not valid. Must be valid and end with @gmail.com.")

        # Kiem tra so dien thoai co hop le khong
        kq_sdt = kiem_tra_so_dien_thoai(self.phoneNumber)
        if not kq_sdt["valid"]:
            raise ValueError(f"Invalid phone number: {kq_sdt.get('reason', 'Not determined.')}")

    # HAM DUNG DE THEM MOT MANAGER MOI VAO DATABASE ---------------------------------------------------------------------------
    def add_manager(self, db):
        try:
            # Kiem tra hop le truoc khi them
            self.validate(db)

            # Hash password truoc khi cap nhap vao database
            hashed_pw = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            sql = """
                INSERT INTO managers (manager_id, full_name, email, username, password, phoneNumber, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(sql, (
                self.manager_id, self.full_name, self.email, self.username,
                hashed_pw, self.phoneNumber, self.created_at
            ))
            print(f"[SUCCESS] Manager '{self.full_name}' was added successfully!")
        except Exception as e:
            raise Exception(f"[ERROR] Cannot add Manager: {e}")

    # HAM TIM KIEM MANAGER THEO ID -------------------------------------------------------------------------------------
    @staticmethod
    def search_manager(db, manager_id):
        try:
            sql = "SELECT * FROM managers WHERE manager_id=%s"
            return db.fetch_one(sql, (manager_id,))
        except Exception as e:
            raise Exception(f"[ERROR] Search Manager: {e}")

    # HAM LAY TOAN BO DANH SACH MANAGER -------------------------------------------------------------------------------
    @staticmethod
    def get_all_managers(db):
        try:
            sql = "SELECT * FROM managers ORDER BY created_at DESC"
            return db.fetch_all(sql)
        except Exception as e:
            raise Exception(f"[ERROR] Get list of Manager: {e}")

    # HAM CAP NHAP THONG TIN CHO MANAGER -------------------------------------------------------------------------------
    def update_manager(self, db):
        try:
            # Hash password roi cap nhap lai
            hashed_pw = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            sql = """
                UPDATE managers
                SET full_name=%s, email=%s, username=%s, password=%s, phoneNumber=%s
                WHERE manager_id=%s
            """
            db.execute_query(sql, (
                self.full_name, self.email, self.username, hashed_pw, self.phoneNumber, self.manager_id
            ))
            print(f"[SUCCESS] Manager '{self.manager_id}' updated successfully.")
        except Exception as e:
            raise Exception(f"[ERROR] Update Manager: {e}")

    # HAM XOA MOT MANAGER KHOI DATABASE --------------------------------------------------------------------------------
    @staticmethod
    def delete_manager(db, manager_id):
        try:
            check = db.fetch_one("SELECT * FROM managers WHERE manager_id=%s", (manager_id,))
            if not check:
                raise ValueError(f"Manager ID '{manager_id}' was not existed.")
            db.execute_query("DELETE FROM managers WHERE manager_id=%s", (manager_id,))
            print(f"[SUCCESS] Manager has ID '{manager_id}' was deleted successfully.")
        except Exception as e:
            raise Exception(f"[ERROR] Delete Manager: {e}")
