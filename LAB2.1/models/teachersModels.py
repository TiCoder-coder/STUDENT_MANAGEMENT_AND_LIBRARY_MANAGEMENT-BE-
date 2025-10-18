import re
from datetime import datetime
import bcrypt                                                                  # Khai bao thu vien dung de hash mat khau 
# TAO MOT DANH SACH CAC NHA MANG DUNG DE KIEM TRA SO DIEN THOAI CO HOP LE KHONG --- CO XU LI SO BAN VA SO MAY------------
NHA_MANG_DI_DONG = {
    'Viettel': ('096', '097', '098', '086', '032', '033', '034', '035', '036', '037', '038', '039'),
    'MobiFone': ('090', '093', '089', '070', '079', '077', '076', '078'),
    'VinaPhone': ('091', '094', '088', '083', '084', '085', '081', '082'),
    'Vietnamobile': ('092', '056', '058'),
    'Gmobile': ('099', '059'),
    'I-Telecom': ('087',),
    'Wintel': ('055',)
}


# HAM DUNG DE CHUAN CHUOI HO VA TEN CHO DUNG-----------------------------------------------------------------------------
def chuan_hoa_ho_ten(ho_ten_raw: str) -> str:
    words = ho_ten_raw.split()
    return " ".join([word.capitalize() for word in words])


# HAM DUNG DE KIEM TRA SO DIEN THOAI CO HOP LE KHONG--------------------------------------------------------------------
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


# HAM DUNG DE KIEM TRA EMAIL CO HOP LE KHONG-----------------------------------------------------------------------------
def kiem_tra_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    return re.match(pattern, email) is not None


# CLASS TEACHER: DUNG DE TAO RA CAC TEACHER ------------------------------------------------------------------------------
class Teacher:
    
    # Ham dung de khoi tao cac thuoc tinh cho teacher --------------------------------------------------------------------
    def __init__(self, teacherId, fullName, birthday, email, phoneNumber, address, userName, password):
        self.teacherId = teacherId
        self.fullName = chuan_hoa_ho_ten(fullName)
        self.birthday = birthday
        self.email = email
        self.phoneNumber = phoneNumber
        self.address = address
        self.userName = userName
        self.password = password

    
    # Viet mot ham dung de kiem tra tat ca cac thong tin truoc khi thuc hien -------------------------------------------- 
    def validate(self, db):
        # Kiem tra teacherId da ton tai chua --- Neu ton tai -> False
        existing = db.fetch_one("SELECT teacherId FROM teachers WHERE teacherId=%s", (self.teacherId,))
        if existing:
            raise ValueError(f"Teacher ID '{self.teacherId}' đã tồn tại trong hệ thống.")

        # Kiem tra userName co trung khong --- Neu trung -> False
        existing_username = db.fetch_one("SELECT userName FROM teachers WHERE userName=%s", (self.userName,))
        if existing_username:
            raise ValueError(f"UserName  '{self.userName}' already exists, please choose another name.")

        # Kiem tra ngay sinh co hop le khong
        if isinstance(self.birthday, str):
            try:
                self.birthday = datetime.strptime(self.birthday, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Date of birth is not in YYYY-MM-DD format.")
        # Kiem tra ngay sinh --- Ngay sinh phai nho hon ngay hien tai
        if self.birthday >= datetime.now():
            raise ValueError("Date of birth must be less than current date.")

        # Kiem tra email co hop le khong
        if not kiem_tra_email(self.email):
            raise ValueError("Invalid email. Email must be valid and end with @gmail.com.")

        # Check phone number
        kq_sdt = kiem_tra_so_dien_thoai(self.phoneNumber)
        if not kq_sdt["valid"]:
            raise ValueError(f"Invalid phone number: {kq_sdt.get('ly_do', 'Not determined.')}")

    # Ham dung de them mot teacher moi --------------------------------------------------------------------------------- 
    def add_teacher(self, db):
        try:
            # Goi ham validate dinh nghia o tren de kiem tra tinh hop le --- Neu hop le thi them moi
            self.validate(db)
            
            # Hash mat khau truoc khi luu 
            hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            hashed_password = hashed_password.decode('utf-8')
            
            sql = """
                INSERT INTO teachers (teacherId, fullName, birthday, email, phoneNumber, address, userName, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(sql, (
                self.teacherId, self.fullName, self.birthday, self.email,
                self.phoneNumber, self.address, self.userName, hashed_password
            ))
            print(f"Add teachers '{self.fullName}' successfully.")
            
        # Bat loi them khong duoc 
        except Exception as e:
            raise Exception(f"Error adding teacher: {e}")


    # Ham dung de tim kiem thong tin cua teacher theo teacherId --------------------------------------------------------
    @staticmethod
    def search_teacher(db, teacherId):
        try:
            sql = "SELECT * FROM teachers WHERE teacherId=%s"
            return db.fetch_one(sql, (teacherId,))
        except Exception as e:
            raise Exception(f"Error when searching for teacher: {e}")

    # Ham dung de lay tat ca cac thong tin cua teacher -----------------------------------------------------------------
    @staticmethod
    def get_all_teachers(db):
        try:
            sql = "SELECT * FROM teachers ORDER BY fullName ASC"
            return db.fetch_all(sql)
        except Exception as e:
            raise Exception(f"Error when getting teacher list: {e}")
        
    # Ham dung de cap nhap thong tin cho teacher--------------------------------------------------------------------------
    # Ham update khong bat buoc phai update tat ca ma chi update nhung cai mong muon (optional)
    def update_teacher(self, db):
        try:
            sql = """
                UPDATE teachers
                SET fullName=%s, birthday=%s, email=%s, phoneNumber=%s, address=%s, userName=%s, password=%s
                WHERE teacherId=%s
            """
            db.execute_query(sql, (
                self.fullName, self.birthday, self.email, self.phoneNumber,
                self.address, self.userName, self.password, self.teacherId
            ))
            print(f"Teacher updates '{self.teacherId}' successfully.")
        except Exception as e:
            raise Exception(f"Error updating teacher: {e}")

    # Ham dung de xoa thong tin cua mot teacher ------------------------------------------------------------------------
    @staticmethod
    def delete_teacher(db, teacherId):
        try:
            db.execute_query("DELETE FROM teachers WHERE teacherId=%s", (teacherId,))
            print(f"Delete teacher has id {teacherId} successfully")
        except Exception as e:
            raise Exception(f"Error when deleting teacher: {e}")

    
