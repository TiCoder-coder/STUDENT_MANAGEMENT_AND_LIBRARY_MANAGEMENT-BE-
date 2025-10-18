import mysql.connector
from decouple import config


class Database:
    def __init__(self):
        self.info = {
            "user": config("DB_USER", default="root"),
            "password": config("DB_PASSWORD", default=""),
            "host": config("DB_HOST", default="localhost"),
            "database": config("DB_NAME", default="course_registration"),
        }
        self.conn = None

    # KET NOI DATABASE
    def connect(self):
        try:
            if self.conn is None or not self.conn.is_connected():
                self.conn = mysql.connector.connect(**self.info)
        except mysql.connector.Error as e:
            print(f"[DB ERROR] Connection failed: {e}")
            self.conn = None

    # THUC THI CAC LENH
    def execute_query(self, sql, params=None):
        try:
            self.connect()
            if self.conn is None:
                raise Exception("Database not connected.")

            with self.conn.cursor() as cur:
                cur.execute(sql, params or ())
                self.conn.commit()
        except mysql.connector.Error as e:
            print(f"[DB ERROR] SQL execution failed: {e}")
        except Exception as e:
            print(f"️[DB ERROR] General error: {e}")

    # SELECT NHIEU DONG
    def fetch_all(self, sql, params=None):
        try:
            self.connect()
            if self.conn is None:
                raise Exception("Database not connected.")

            cur = self.conn.cursor(dictionary=True)
            cur.execute(sql, params or ())
            rows = cur.fetchall()
            cur.close()
            return rows or []
        except mysql.connector.Error as e:
            print(f"[DB ERROR] SQL fetch_all failed: {e}")
            return []
        except Exception as e:
            print(f"[DB ERROR] General error in fetch_all: {e}")
            return []

    # SELECT 1 DONG
    def fetch_one(self, sql, params=None):
        try:
            self.connect()
            if self.conn is None:
                raise Exception("Database not connected.")

            cur = self.conn.cursor(dictionary=True)
            cur.execute(sql, params or ())
            row = cur.fetchone()
            cur.close()
            return row
        except mysql.connector.Error as e:
            print(f"[DB ERROR] SQL fetch_one failed: {e}")
            return None
        except Exception as e:
            print(f"️[DB ERROR] General error in fetch_one: {e}")
            return None

    # HUY KET NOI
    def __del__(self):
        try:
            if self.conn and self.conn.is_connected():
                self.conn.close()
                print("🔌 Database connection closed.")
        except:
            pass
