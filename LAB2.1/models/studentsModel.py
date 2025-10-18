import re
from datetime import datetime


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
    
    # Chia chuoi ra va sau do viet hoa cac chu cai dau roi gop lai
    words = ho_ten_raw.split()
    return " ".join([word.capitalize() for word in words])

# HAM DUNG DE KIEM TRA EMAIL CO HOP LE KHONG-----------------------------------------------------------------------------
def kiem_tra_email_hop_le(email: str) -> bool:
    
    # Mot email hop le phai co duoi @gmail.com va cac ki tu phia truoc
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return bool(re.match(pattern, email))

# HAM DUNG DE KIEM TRA SO DIEN THOAI CO HOP LE KHONG--------------------------------------------------------------------
def kiem_tra_so_dien_thoai(sdt: str) -> dict:
    sdt_sach = re.sub(r'\D', '', sdt)
    if sdt_sach.startswith('84'):
        sdt_sach = '0' + sdt_sach[2:]

    # So dien thoai hop le phai bat dau bang so 0 va co len = 10
    if not sdt_sach.startswith('0') or len(sdt_sach) != 10:
        return {'valid': False, 'reason': 'Số điện thoại phải có 10 số và bắt đầu bằng 0.'}

    dau_so = sdt_sach[:3]
    for ten_mang, cac_dau_so in NHA_MANG_DI_DONG.items():
        if dau_so in cac_dau_so:
            return {'valid': True, 'sdt_chuan_hoa': sdt_sach, 'nha_mang': ten_mang}

    # Neu so dau la 02 ti la may ban
    if dau_so.startswith('02'):
        return {'valid': True, 'sdt_chuan_hoa': sdt_sach, 'nha_mang': 'Máy bàn'}

    return {'valid': False, 'reason': f'Đầu số "{dau_so}" không hợp lệ.'}


# CLASS STUDENT: DUNG DE TAO RA CAC STUDENT ------------------------------------------------------------------------------
class Student:
    
    # Ham dung de khoi tao cac thuoc tinh cho student
    def __init__(self, studentId, fullName, birthday, email, phoneNumber, address):
        self.studentId = studentId
        self.fullName = chuan_hoa_ho_ten(fullName)
        self.birthday = birthday
        self.email = email
        self.phoneNumber = phoneNumber
        self.address = address

    # Ham dung de them mot sinh vien moi vao -----------------------------------------------------------------------------
    def add_student(self, db):
        try:
            
            # Kiem tra xem student do da ton tai hay chua --- Neu co -> False
            exists = db.fetch_one("SELECT * FROM students WHERE studentId=%s", (self.studentId,))
            if exists:
                print(f"[ERROR] Student ID '{self.studentId}' already exists.")
                return

            # kiem tra birthday --- Khong duoc lon hon ngay hien tai
            dob_obj = datetime.strptime(self.birthday, "%Y-%m-%d")
            if dob_obj >= datetime.now():
                print("[ERROR] Birthday must be in the past.")
                return

            # Kiem tra email hop le khong
            if not kiem_tra_email_hop_le(self.email):
                print(f"[ERROR] Invalid email '{self.email}'. Must be a valid Gmail.")
                return

            # Kiem tra so dien thoai co dung khong
            sdt_info = kiem_tra_so_dien_thoai(self.phoneNumber)
            if not sdt_info['valid']:
                print(f"[ERROR] Invalid phone number '{self.phoneNumber}': {sdt_info['ly_do']}")
                return

            # Neu cac thong tin dung het thi thuc hien them vao
            db.execute_query("""
                INSERT INTO students (studentId, fullName, birthday, email, phoneNumber, address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                self.studentId, self.fullName, self.birthday,
                self.email, sdt_info['sdt_chuan_hoa'], self.address
            ))

            print(f"[SUCCESS] Added student '{self.fullName}' successfully! ({sdt_info['nha_mang']})")
        # Bat loi khi them mot sinh vien moi
        except Exception as e:
            print(f"[ERROR] Failed to add student: {e}")

    
    # Ham dung de tim kiem mot sinh vien theo studentId ------------------------------------------------------------------
    @staticmethod
    def search_student(db, studentId):
        try:
            # Tra ve thong tin cua sinh vien can tim kiem
            return db.fetch_all("SELECT * FROM students WHERE studentId=%s", (studentId,))
        
        # Bat loi tim kiem
        except Exception as e:
            print(f"[ERROR] Failed to search student: {e}")
            return []

    # Ham dung de lay thong tin cua tat ca cac sinh vien -----------------------------------------------------------------
    @staticmethod
    def get_all_students(db):
        try:
            
            # Lay tat ca cac thong tin
            return db.fetch_all("SELECT * FROM students")
        
        # Bat loi khi lay thong tin
        except Exception as e:
            print(f"[ERROR] Failed to fetch students: {e}")
            return []
        
    # Ham dung de cap nhap thong tin cho student--------------------------------------------------------------------------
    # Ham update khong bat buoc phai update tat ca ma chi update nhung cai mong muon (optional)
    def update_student(self, db):
        try:
            
            # Kiem tra xem sinh vien can cap nhap co ton tai khong
            current_data = db.fetch_one("SELECT * FROM students WHERE studentId=%s", (self.studentId,))
            if not current_data:
                print(f"[ERROR] Student ID '{self.studentId}' not found.")
                return
            
            # Xu li va kiem tra cac thuoc tinh truoc khi update
            new_fullName = chuan_hoa_ho_ten(self.fullName or current_data['fullName'])
            new_birthday = self.birthday or current_data['birthday']
            new_email = self.email or current_data['email']
            new_phone = self.phoneNumber or current_data['phoneNumber']
            new_address = self.address or current_data['address']

            if not kiem_tra_email_hop_le(new_email):
                print(f"[ERROR] Invalid email '{new_email}'.")
                return

            sdt_info = kiem_tra_so_dien_thoai(new_phone)
            if not sdt_info['valid']:
                print(f"[ERROR] Invalid phone: {sdt_info['ly_do']}")
                return
            
            # Neu khong co loi gi thi thuc hien update
            db.execute_query("""
                UPDATE students
                SET fullName=%s, birthday=%s, email=%s, phoneNumber=%s, address=%s
                WHERE studentId=%s
            """, (new_fullName, new_birthday, new_email, sdt_info['sdt_chuan_hoa'], new_address, self.studentId))
            print(f"[SUCCESS] Updated student '{new_fullName}' successfully!")

        except Exception as e:
            print(f"[ERROR] Failed to update student: {e}")

    # Ham dung de xoa thong tin cua mot sinh vien ------------------------------------------------------------------------
    @staticmethod
    def delete_student(db, studentId):
        try:
            
            # Kiem tra xem sinh vien muon xoa co ton tai hay khong --- Neu ton tai thi xoa
            exists = db.fetch_one("SELECT * FROM students WHERE studentId=%s", (studentId,))
            if not exists:
                print(f"[ERROR] Student ID '{studentId}' not found.")
                return
            db.execute_query("DELETE FROM students WHERE studentId=%s", (studentId,))
            print(f"[SUCCESS] Deleted student '{studentId}' successfully!")
            
        # Bat loi xoa
        except Exception as e:
            print(f"[ERROR] Failed to delete student: {e}")

    
