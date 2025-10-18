import re
import bcrypt
from datetime import datetime

# DANH SÁCH CÁC NHÀ MẠNG PHỔ BIẾN DÙNG ĐỂ KIỂM TRA SỐ ĐIỆN THOẠI CÓ HỢP LỆ KHÔNG ----------------------------------------
NHA_MANG_DI_DONG = {
    'Viettel': ('096', '097', '098', '086', '032', '033', '034', '035', '036', '037', '038', '039'),
    'MobiFone': ('090', '093', '089', '070', '079', '077', '076', '078'),
    'VinaPhone': ('091', '094', '088', '083', '084', '085', '081', '082'),
    'Vietnamobile': ('092', '056', '058'),
    'Gmobile': ('099', '059'),
    'I-Telecom': ('087',),
    'Wintel': ('055',)
}

# HÀM CHUẨN HÓA HỌ TÊN ĐỂ VIẾT HOA ĐÚNG CHỮ CÁI ĐẦU ---------------------------------------------------------------------
def chuan_hoa_ho_ten(ho_ten_raw: str) -> str:
    words = ho_ten_raw.strip().split()
    return " ".join([word.capitalize() for word in words])

# HÀM KIỂM TRA EMAIL CÓ ĐÚNG ĐỊNH DẠNG VÀ PHẢI LÀ GMAIL -----------------------------------------------------------------
def kiem_tra_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    return re.match(pattern, email) is not None

# HÀM KIỂM TRA SỐ ĐIỆN THOẠI HỢP LỆ VÀ XÁC ĐỊNH NHÀ MẠNG ----------------------------------------------------------------
def kiem_tra_so_dien_thoai(sdt: str) -> dict:
    sdt_sach = re.sub(r'\D', '', sdt)

    if sdt_sach.startswith('84'):
        sdt_sach = '0' + sdt_sach[2:]

    if not sdt_sach.startswith('0') or len(sdt_sach) != 10:
        return {'valid': False, 'ly_do': 'SĐT phải có 10 số và bắt đầu bằng 0.'}

    dau_so = sdt_sach[:3]
    for ten_mang, cac_dau_so in NHA_MANG_DI_DONG.items():
        if dau_so in cac_dau_so:
            return {'valid': True, 'nha_mang': ten_mang, 'sdt_chuan_hoa': sdt_sach}

    if dau_so.startswith('02'):
        return {'valid': True, 'nha_mang': 'Máy bàn', 'sdt_chuan_hoa': sdt_sach}

    return {'valid': False, 'ly_do': f'Đầu số {dau_so} không tồn tại.'}

# CLASS MANAGER: DÙNG ĐỂ QUẢN LÝ CÁC THÔNG TIN CỦA MANAGER TRONG HỆ THỐNG ---------------------------------------------
class Manager:
    
    # Hàm khởi tạo các thuộc tính cho manager --------------------------------------------------------------------------
    def __init__(self, manager_id, full_name, email, username, password, phoneNumber, created_at=None):
        self.manager_id = manager_id
        self.full_name = chuan_hoa_ho_ten(full_name)
        self.email = email
        self.username = username
        self.password = password
        self.phoneNumber = phoneNumber
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # HÀM DÙNG ĐỂ KIỂM TRA TÍNH HỢP LỆ TRƯỚC KHI THÊM MỘT MANAGER -------------------------------------------------------
    def validate(self, db):
        # Kiểm tra ID đã tồn tại hay chưa
        existing_id = db.fetch_one("SELECT manager_id FROM managers WHERE manager_id=%s", (self.manager_id,))
        if existing_id:
            raise ValueError(f"Manager ID '{self.manager_id}' đã tồn tại trong hệ thống.")

        # Kiểm tra username có bị trùng hay không
        existing_username = db.fetch_one("SELECT username FROM managers WHERE username=%s", (self.username,))
        if existing_username:
            raise ValueError(f"Username '{self.username}' đã tồn tại, vui lòng chọn tên khác.")

        # Kiểm tra email có bị trùng hoặc sai định dạng không
        existing_email = db.fetch_one("SELECT email FROM managers WHERE email=%s", (self.email,))
        if existing_email:
            raise ValueError(f"Email '{self.email}' đã tồn tại trong hệ thống.")
        if not kiem_tra_email(self.email):
            raise ValueError("Email không hợp lệ. Phải có dạng hợp lệ và kết thúc bằng @gmail.com.")

        # Kiểm tra số điện thoại hợp lệ
        kq_sdt = kiem_tra_so_dien_thoai(self.phoneNumber)
        if not kq_sdt["valid"]:
            raise ValueError(f"Số điện thoại không hợp lệ: {kq_sdt.get('ly_do', 'Không xác định.')}")

    # HÀM THÊM MỘT MANAGER MỚI VÀO DATABASE ---------------------------------------------------------------------------
    def add_manager(self, db):
        try:
            # Kiểm tra hợp lệ trước khi thêm
            self.validate(db)

            # Hash password trước khi lưu vào database
            hashed_pw = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            sql = """
                INSERT INTO managers (manager_id, full_name, email, username, password, phoneNumber, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(sql, (
                self.manager_id, self.full_name, self.email, self.username,
                hashed_pw, self.phoneNumber, self.created_at
            ))
            print(f"[SUCCESS] Manager '{self.full_name}' đã được thêm thành công!")
        except Exception as e:
            raise Exception(f"[ERROR] Không thể thêm Manager: {e}")

    # HÀM TÌM KIẾM MANAGER THEO ID -------------------------------------------------------------------------------------
    @staticmethod
    def search_manager(db, manager_id):
        try:
            sql = "SELECT * FROM managers WHERE manager_id=%s"
            return db.fetch_one(sql, (manager_id,))
        except Exception as e:
            raise Exception(f"[ERROR] Khi tìm kiếm Manager: {e}")

    # HÀM LẤY TOÀN BỘ DANH SÁCH MANAGER -------------------------------------------------------------------------------
    @staticmethod
    def get_all_managers(db):
        try:
            sql = "SELECT * FROM managers ORDER BY created_at DESC"
            return db.fetch_all(sql)
        except Exception as e:
            raise Exception(f"[ERROR] Khi lấy danh sách Manager: {e}")

    # HÀM CẬP NHẬT THÔNG TIN CHO MANAGER -------------------------------------------------------------------------------
    def update_manager(self, db):
        try:
            # Nếu password được nhập mới → hash lại
            hashed_pw = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            sql = """
                UPDATE managers
                SET full_name=%s, email=%s, username=%s, password=%s, phoneNumber=%s
                WHERE manager_id=%s
            """
            db.execute_query(sql, (
                self.full_name, self.email, self.username, hashed_pw, self.phoneNumber, self.manager_id
            ))
            print(f"[SUCCESS] Manager '{self.manager_id}' cập nhật thành công.")
        except Exception as e:
            raise Exception(f"[ERROR] Khi cập nhật Manager: {e}")

    # HÀM XÓA MỘT MANAGER KHỎI DATABASE --------------------------------------------------------------------------------
    @staticmethod
    def delete_manager(db, manager_id):
        try:
            check = db.fetch_one("SELECT * FROM managers WHERE manager_id=%s", (manager_id,))
            if not check:
                raise ValueError(f"Manager ID '{manager_id}' không tồn tại.")
            db.execute_query("DELETE FROM managers WHERE manager_id=%s", (manager_id,))
            print(f"[SUCCESS] Manager có ID '{manager_id}' đã được xóa thành công.")
        except Exception as e:
            raise Exception(f"[ERROR] Khi xóa Manager: {e}")
