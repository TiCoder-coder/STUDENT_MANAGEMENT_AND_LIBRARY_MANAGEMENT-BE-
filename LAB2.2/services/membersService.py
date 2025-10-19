from models.membersModel import Member
from auth import require_manager  # Goi ham kiem tra quyen tu auth de kiem tra


# CLASS MEMBERSERVICE SE GOI LAI CAC HAM CUA MODEL VA THUC THI NO VA PHAN QUYEN SU DUNG ------------------------------
class MemberService:
    
    # KHOI TAO PHUONG THUC --------------------------------------------------------------------------------------------
    def __init__(self, db):
        self.db = db

    # GOI HAM THEM CAC MEMBER --- CHI CO TEACHER THUC HIEN ------------------------------------------------------------
    def add_member(self, data: dict):
        try:
            # Kiem tra quyen
            require_manager()

            # Kiem tra du lieu bat buoc
            required = ["name", "birthday", "email", "phoneNumber"]
            for f in required:
                if not data.get(f):
                    print(f"[VALIDATION] Missing field: {f}")
                    return

            # Tao doi tuong Member va goi ham add_member trong model
            member = Member(**data)
            member.add_member(self.db)
        except PermissionError as e:
            print(f"[AUTH ERROR] {e}")
        except Exception as e:
            print(f"[SERVICE ERROR] {e}")

    # GOI HAM TIM KIEM MEMBER --- CO THE SU DUNG CHO TEACHER ----------------------------------------------------------
    def search_member(self, member_id=None, name=None, email=None):
        try:
            return Member.search_member(self.db, member_id, name, email)
        except Exception as e:
            print(f"[SERVICE ERROR] {e}")
            return []

    # GOI HAM HIEN THI TAT CA CAC MEMBER --- CO THE SU DUNG CHO TEACHER -----------------------------------------------
    def get_all_members(self):
        try:
            return Member.get_all_members(self.db)
        except Exception as e:
            print(f"[SERVICE ERROR] {e}")
            return []

    # GOI HAM CAP NHAT THONG TIN MEMBER --- CHI CO TEACHER THUC HIEN --------------------------------------------------
    def update_member(self, data: dict):
        try:
            # Kiem tra quyen
            require_manager()

            if not data.get("member_id"):
                print("[VALIDATION] Missing member_id.")
                return

            member = Member(**data)
            member.update_member(self.db)
        except PermissionError as e:
            print(f"[AUTH ERROR] {e}")
        except Exception as e:
            print(f"[SERVICE ERROR] {e}")

    # GOI HAM XOA MEMBER --- CHI CO TEACHER THUC HIEN -----------------------------------------------------------------
    def delete_member(self, member_id: str):
        try:
            # Kiem tra quyen
            require_manager()
            Member.delete_member(self.db, member_id)
        except PermissionError as e:
            print(f"[AUTH ERROR] {e}")
        except Exception as e:
            print(f"[SERVICE ERROR] {e}")

    # HAM PHU LAY TAT CA (DE DUNG CHO CAC TRUONG HOP KHAC NHAU) --------------------------------------------------------
    def fetch_all(self, *args, **kwargs):
        return self.get_all_members()
