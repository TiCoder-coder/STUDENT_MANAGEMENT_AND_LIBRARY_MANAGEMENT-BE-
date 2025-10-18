# enums/enums.py
from enum import Enum

# Trang thai cua cac cuon sach
class BookStatus(Enum):
    AVAILABLE = 0                                           # Trang thai co san
    BORROWED = 1                                            # Trang thai da muon
    OTHER = 2                                               # Trang thai khac

# Cac loai sach
class BookType(Enum):
    NOVEL = 'novel'                                         # Sach tieu thuyet
    TEXTBOOK = 'textbook'                                   # Sach giao khoa
    SCIENCE = 'science'                                     # Sach khoa hoc

class BookNovelType(Enum):
    ROMANTIC = 'romantic'                                   # Lang man
    THRILLING = 'thrilling'                                 # Ly ky, giat gan
    MYSTERY = 'mystery'                                     # Huyen bi
    CRIME = 'crime'                                         # Toi pham
    FANTASY = 'fantasy'                                     # Ky ao
    SCIENCE_FICTION = 'science_fiction'                     # Khoa hoc vien tuong
    HORROR = 'horror'                                       # Kinh di
    HISTORICAL = 'historical'                               # Lich su
    ADVENTURE = 'adventure'                                 # Phieu luu
    CONTEMPORARY = 'contemporary'                           # Duong dai
    COMEDY = 'comedy'                                       # Hai huoc
    DRAMA = 'drama'                                         # Kich tinh
    YOUNG_ADULT = 'young_adult'                             # Thanh thieu nien
    PARANORMAL = 'paranormal'                               # Sieu nhien
    DYSTOPIAN = 'dystopian'                                 # Phan dia hang

class TextBookType(Enum):
    MATH = 'math'                                           # Toan hoc
    LITERATURE = 'literature'                               # Ngu van
    ENGLISH = 'english'                                     # Tieng Anh
    PHYSICS = 'physics'                                     # Vat ly
    CHEMISTRY = 'chemistry'                                 # Hoa hoc
    BIOLOGY = 'biology'                                     # Sinh hoc
    HISTORY = 'history'                                     # Lich su
    GEOGRAPHY = 'geography'                                 # Dia ly
    CIVICS = 'civics'                                       # Giao duc cong dan
    TECHNOLOGY = 'technology'                               # Cong nghe
    COMPUTER_SCIENCE = 'computer_science'                   # Tin hoc
    MUSIC = 'music'                                         # Am nhac
    ART = 'art'                                             # My thuat
    PHYSICAL_EDUCATION = 'physical_education'               # The duc
    REFERENCE_BOOK = 'reference_book'                       # Sach tham khao
    TEACHER_BOOK = 'teacher_book'                           # Sach giao vien
    EXERCISE_BOOK = 'exercise_book'                         # Sach bai tap
class ScienceType(Enum):
            
    # Cong nghe Thong tin (IT) ---
    PROGRAMMING = 'programming'                             # Lap trinh (Python, Java, C++,...)
    DATA_STRUCTURES = 'data_structures'                     # Cau truc du lieu & Giai thuat
    DATABASES = 'databases'                                 # Co so du lieu (SQL, NoSQL)
    NETWORKING = 'networking'                               # Mang may tinh
    CYBER_SECURITY = 'cyber_security'                       # An toan thong tin
    WEB_DEVELOPMENT = 'web_development'                     # Phat trien Web (Frontend, Backend)
    MOBILE_DEVELOPMENT = 'mobile_development'               # Phat trien Di dong
    OPERATING_SYSTEMS = 'operating_systems'                 # He dieu hanh

    # Tri tue Nhan tao (AI) & Du lieu ---
    AI_GENERAL = 'ai_general'                               # Tong quan ve AI
    MACHINE_LEARNING = 'machine_learning'                   # Hoc may
    DEEP_LEARNING = 'deep_learning'                         # Hoc sau
    DATA_SCIENCE = 'data_science'                           # Khoa hoc du lieu
    NLP = 'nlp'                                             # Xu ly Ngon ngu Tu nhien
    COMPUTER_VISION = 'computer_vision'                     # Thi giac may tinh

    # Co khi & Ky thuat Lien quan ---
    MECHANICAL_ENGINEERING = 'mechanical_engineering'       # Co khi Che tao may
    AUTOMATION = 'automation'                               # Tu dong hoa
    ROBOTICS = 'robotics'                                   # Robotics (Lien quan ca AI va Co khi)
    CAD_CAM = 'cad_cam'                                     # Thiet ke & San xuat (CAD/CAM)
    MATERIALS_SCIENCE = 'materials_science'                 # Khoa hoc Vat lieu
    THERMODYNAMICS = 'thermodynamics'                       # Nhiet dong luc hoc
    ELECTRONICS = 'electronics'                             # Ky thuat Dien - Dien tu
class EducationLevel(Enum):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    HIGHSCHOOL = 'highschool'
    UNIVERSITY = 'university'