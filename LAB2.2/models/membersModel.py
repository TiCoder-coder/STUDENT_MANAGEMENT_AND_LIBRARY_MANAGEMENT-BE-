# models/membersModel.py
import re
from datetime import datetime, date

# DANH SACH CAC NHA MANG DI DONG (dung de kiem tra dau so) -----------------------------------------------------------
NHA_MANG_DI_DONG = {
    'Viettel': ('096', '097', '098', '086', '032', '033', '034', '035', '036', '037', '038', '039'),
    'MobiFone': ('090', '093', '089', '070', '079', '077', '076', '078'),
    'VinaPhone': ('091', '094', '088', '083', '084', '085', '081', '082'),
    'Vietnamobile': ('092', '056', '058'),
    'Gmobile': ('099', '059'),
    'I-Telecom': ('087',),
    'Wintel': ('055',)
}

# HAM CHUAN HOA HO TEN -----------------------------------------------------------------------------------------------
def chuan_hoa_ho_ten(ten_raw: str) -> str:
    """
    Chuẩn hoá họ tên: loại bỏ khoảng trắng thừa, viết hoa chữ cái đầu mỗi từ.
    """
    if not ten_raw:
        return ""
    words = ten_raw.strip().split()
    return " ".join([w.capitalize() for w in words])

# HAM KIEM TRA EMAIL (THEO MAU FILE MAU: CHI NHAN GMAIL) --------------------------------------------------------------
def kiem_tra_email_hop_le(email: str) -> bool:
    """
    Kiểm tra email hợp lệ theo pattern (ví dụ: chỉ chấp nhận *@gmail.com như file mẫu).
    """
    if not email:
        return False
    pattern = r'^[A-Za-z0-9._%+-]+@gmail\.com$'
    return bool(re.match(pattern, email))

# HAM KIEM TRA SO DIEN THOAI ------------------------------------------------------------------------------------------
def kiem_tra_so_dien_thoai(sdt: str) -> dict:
    """
    Chuẩn hoá và kiểm tra số điện thoại.
    Trả về dict:
      - valid: True/False
      - sdt_chuan_hoa: số đã chuẩn hoá (vd: 0335052899)
      - nha_mang: tên nhà mạng nếu xác định được
      - reason: lý do không hợp lệ nếu có
    """
    if not sdt:
        return {'valid': False, 'reason': 'Số điện thoại rỗng.'}

    # Loại bỏ ký tự không phải số
    s = re.sub(r'\D', '', sdt)

    # Nếu bắt đầu với 84 (mã quốc gia VN) -> chuyển về dạng 0xxxxxxxxx
    if s.startswith('84') and len(s) >= 11:
        s = '0' + s[2:]

    # Kiểm tra độ dài và bắt đầu bằng 0
    if not s.startswith('0') or len(s) != 10:
        return {'valid': False, 'reason': 'Số điện thoại phải có 10 chữ số và bắt đầu bằng 0.'}

    dau = s[:3]
    for ten_mang, dau_list in NHA_MANG_DI_DONG.items():
        if dau in dau_list:
            return {'valid': True, 'sdt_chuan_hoa': s, 'nha_mang': ten_mang}

    # Nếu đầu số 02* -> có thể là máy bàn
    if dau.startswith('02'):
        return {'valid': True, 'sdt_chuan_hoa': s, 'nha_mang': 'Máy bàn'}

    return {'valid': False, 'reason': f'Đầu số "{dau}" không hợp lệ.'}

# CLASS MEMBER: DUNG DE QUAN LY THONG TIN THANH VIEN ------------------------------------------------------------------
class Member:
    """
    Member model quản lý bảng members.
    Các phương thức in thông báo theo phong cách mẫu (print).
    """

    def __init__(self, name, birthday, email, phoneNumber, member_id=None, created_at=None):
        self.member_id = member_id
        self.name = chuan_hoa_ho_ten(name)
        self.birthday = birthday  # mong muon format 'YYYY-MM-DD' (hoac datetime)
        self.email = email
        self.phoneNumber = phoneNumber
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ham them 1 member moi vao database ---------------------------------------------------------------------------------
    def add_member(self, db):
        try:
            # 1) Kiểm tra nếu có member_id truyền vào -> xem có tồn tại
            if self.member_id:
                ex = db.fetch_one("SELECT * FROM members WHERE member_id=%s", (self.member_id,))
                if ex:
                    print(f"[ERROR] Member ID '{self.member_id}' already exists.")
                    return

            # 2) Kiểm tra định dạng ngày sinh (birthday) và không được lớn hơn hiện tại
            try:
                # Cho phép truyền string 'YYYY-MM-DD' hoặc datetime object
                if isinstance(self.birthday, str):
                    dob = datetime.strptime(self.birthday, "%Y-%m-%d")
                elif isinstance(self.birthday, datetime):
                    dob = self.birthday
                else:
                    print("[ERROR] Invalid birthday format. Use 'YYYY-MM-DD'.")
                    return
                if dob >= datetime.now():
                    print("[ERROR] Birthday must be in the past.")
                    return
            except Exception:
                print("[ERROR] Invalid birthday format. Use 'YYYY-MM-DD'.")
                return

            # 3) Kiểm tra email hợp lệ
            if not kiem_tra_email_hop_le(self.email):
                print(f"[ERROR] Invalid email '{self.email}'. Must be a valid Gmail address.")
                return

            # 4) Kiểm tra số điện thoại
            sdt_info = kiem_tra_so_dien_thoai(self.phoneNumber)
            if not sdt_info.get('valid'):
                print(f"[ERROR] Invalid phone number '{self.phoneNumber}': {sdt_info.get('reason')}")
                return

            # 5) Kiểm tra email có bị trùng trong DB không
            exists_email = db.fetch_one("SELECT * FROM members WHERE email=%s", (self.email,))
            if exists_email:
                print(f"[ERROR] Email '{self.email}' already exists.")
                return

            # 6) Thực hiện insert
            db.execute_query("""
                INSERT INTO members (name, birthday, email, phoneNumber, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                self.name,
                dob.strftime("%Y-%m-%d %H:%M:%S"),
                self.email,
                sdt_info.get('sdt_chuan_hoa'),
                self.created_at
            ))

            print(f"[SUCCESS] Added member '{self.name}' successfully! ({sdt_info.get('nha_mang')})")
        except Exception as e:
            print(f"[ERROR] Failed to add member: {e}")

    # Ham tim kiem member theo cac tieu chi (member_id, name, email) -----------------------------------------------------
    @staticmethod
    def search_member(db, member_id=None, name=None, email=None):
        try:
            sql = "SELECT * FROM members WHERE "
            params, conditions = [], []

            if member_id:
                conditions.append("member_id=%s")
                params.append(member_id)
            if name:
                conditions.append("name LIKE %s")
                params.append(f"%{name}%")
            if email:
                conditions.append("email=%s")
                params.append(email)

            if not conditions:
                return []

            sql += " OR ".join(conditions)
            return db.fetch_all(sql, tuple(params))
        except Exception as e:
            print(f"[ERROR] Failed to search member: {e}")
            return []

    # Ham lay tat ca members ------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all_members(db):
        try:
            return db.fetch_all("SELECT * FROM members ORDER BY created_at DESC")
        except Exception as e:
            print(f"[ERROR] Failed to fetch members: {e}")
            return []

    # Ham cap nhat thong tin member (tuong tu file mau) ---------------------------------------------------------------------
    def update_member(self, db):
        try:
            # Kiem tra ton tai member
            if not self.member_id:
                print("[ERROR] member_id is required for update.")
                return

            current = db.fetch_one("SELECT * FROM members WHERE member_id=%s", (self.member_id,))
            if not current:
                print(f"[ERROR] Member ID '{self.member_id}' not found.")
                return

            # Lấy giá trị mới hoặc giữ nguyên nếu không truyền
            new_name = chuan_hoa_ho_ten(self.name or current.get('name'))
            new_birthday_raw = self.birthday or current.get('birthday')
            new_email = self.email or current.get('email')
            new_phone_raw = self.phoneNumber or current.get('phoneNumber')

            # Kiểm tra birthday
            try:
                if isinstance(new_birthday_raw, str):
                    dob = datetime.strptime(new_birthday_raw, "%Y-%m-%d")
                elif isinstance(new_birthday_raw, datetime):
                    dob = new_birthday_raw
                else:
                    print("[ERROR] Invalid birthday format. Use 'YYYY-MM-DD'.")
                    return
                if dob >= datetime.now():
                    print("[ERROR] Birthday must be in the past.")
                    return
            except Exception:
                print("[ERROR] Invalid birthday format. Use 'YYYY-MM-DD'.")
                return

            # Kiểm tra email
            if not kiem_tra_email_hop_le(new_email):
                print(f"[ERROR] Invalid email '{new_email}'.")
                return

            # Nếu email thay đổi thì kiểm tra trùng
            if new_email != current.get('email'):
                e_exists = db.fetch_one("SELECT * FROM members WHERE email=%s", (new_email,))
                if e_exists:
                    print(f"[ERROR] Email '{new_email}' already in use.")
                    return

            # Kiểm tra số điện thoại
            sdt_info = kiem_tra_so_dien_thoai(new_phone_raw)
            if not sdt_info.get('valid'):
                print(f"[ERROR] Invalid phone number: {sdt_info.get('reason')}")
                return

            # Thực hiện update
            db.execute_query("""
                UPDATE members
                SET name=%s, birthday=%s, email=%s, phoneNumber=%s
                WHERE member_id=%s
            """, (
                new_name,
                dob.strftime("%Y-%m-%d %H:%M:%S"),
                new_email,
                sdt_info.get('sdt_chuan_hoa'),
                self.member_id
            ))

            print(f"[SUCCESS] Updated member '{new_name}' successfully!")
        except Exception as e:
            print(f"[ERROR] Failed to update member: {e}")

    # Ham xoa member theo member_id ---------------------------------------------------------------------------------------
    @staticmethod
    def delete_member(db, member_id):
        try:
            exists = db.fetch_one("SELECT * FROM members WHERE member_id=%s", (member_id,))
            if not exists:
                print(f"[ERROR] Member ID '{member_id}' not found.")
                return
            db.execute_query("DELETE FROM members WHERE member_id=%s", (member_id,))
            print(f"[SUCCESS] Deleted member '{member_id}' successfully!")
        except Exception as e:
            print(f"[ERROR] Failed to delete member: {e}")
