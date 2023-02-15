import sqlite3
import pandas as pd
# import sqlalchemy

CREATE_USER = "INSERT INTO users (username, password) VALUES (?, ?);"
GET_ONE_USER = "SELECT username FROM users where username=?;"
GET_USERNAME_PASSWORD_COMBO = "SELECT username, password FROM users WHERE username=? AND password=?;"
GET_ID_BY_NAME = "SELECT user_id FROM users WHERE username=?;"
STORE_START_ENTRY = "INSERT INTO entries (start_date, start_time, FK_entries_user_id) VALUES (?, ?, ?);"
STORE_END_ENTRY = "UPDATE entries SET end_date=?, end_time=? WHERE entry_id=?;"
STORE_LOG = "INSERT INTO logs (FK_logs_entry_id, FK_logs_user_id, logged_date, logged_time, status, status_type, term) VALUES (?, ?, ?, ?, ?, ?, ?);"
GET_ENTRY_ID_BY_DATE_TIME_AND_USER_ID = "SELECT entry_id FROM entries where start_date=? AND start_time=? AND FK_entries_user_id=?;"
GET_ALL_ENTRY_ID_BY_USER_ID = "SELECT entry_id, start_date, end_date, start_time, end_time FROM entries WHERE FK_entries_user_id=?;"
GET_LOGS_BY_ENTRY_ID  = "SELECT * FROM logs WHERE FK_logs_entry_id=?;"

class TableConnection():
    def __init__(self, __user_id=None, username=None, password=None):
        self.__username = username
        self.__user_id = __user_id
        self.__password = password
        self.logged_in = False
        self.__conn = sqlite3.connect("userdata.db", check_same_thread=False)
        self.__cur = self.__conn.cursor()
        self.__entry_id = None

        self.__cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """);

        self.__cur.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_date DATE NOT NULL,
            end_date DATE,
            start_time TIME NOT NULL,
            end_time TIME,
            FK_entries_user_id INTEGER,
            FOREIGN KEY (FK_entries_user_id) REFERENCES users(user_id)
        )
        """);

        self.__cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            FK_logs_entry_id INTEGER NOT NULL,
            FK_logs_user_id INTEGER NOT NULL,
            logged_date DATE NOT NULL,
            logged_time TIME NOT NULL,
            status VARCHAR(10) NOT NULL,
            status_type VARCHAR(20) NOT NULL,
            term VARCHAR(200) NOT NULL,
            FOREIGN KEY (FK_logs_entry_id) REFERENCES entries(entry_id)
            FOREIGN KEY (FK_logs_user_id) REFERENCES users(user_id)
        )
        """)

    def __del__(self):
        self.__conn.commit()
        self.__conn.close()

    def create_user(self, username, password):
        if not self.if_user_exists(username,):
            self.__cur.execute(CREATE_USER, (username, password,))
            self.__conn.commit()
        else:
            print("User already exists!")

    def if_user_exists(self, username):
        self.__cur.execute(GET_ONE_USER, (username,))
        if self.__cur.fetchone():
            return True
        return False

    def is_valid_login(self, username, password,):
        if not self.if_user_exists(username):
            print("User does not exist!")
            return False

        self.__cur.execute(GET_USERNAME_PASSWORD_COMBO, (username, password,))
        if self.__cur.fetchone():
            return True
        else:
            print("Incorrect combinations! " + username + " " + password)
            return False

    def access_to_table(self,user_id, username, password):
        self.__user_id = user_id
        self.__username = username
        self.__password = password  
        self.logged_in = True

    def insert_start_entry(self, date, start_time, user_id):
        print("query")

        if not user_id:
            user_id = self.__user_id

        self.__cur.execute(STORE_START_ENTRY, (str(date), str(start_time), user_id,))
        self.__entry_id = self.get_entry_id_by_date_time_and_user_id(str(date), str(start_time), user_id,)
        self.__conn.commit()

    def get_current_entry_id(self):
        return self.__entry_id
    
    def insert_end_entry(self, end_date, end_time):
        self.__cur.execute(STORE_END_ENTRY, (str(end_date), str(end_time), self.__entry_id))
        self.__conn.commit()
    
    def disconnect_db(self):
        self.__conn.commit()
        self.__conn.close()

    def log(self, date, time, status_type, term):
        self.__cur.execute(STORE_LOG, (self.__entry_id, self.__user_id, str(date), str(time), "Active", str(status_type), str(term),))
        self.__conn.commit()

    def log_idle_status(self, date, time):
        self.__cur.execute(STORE_LOG, (self.__entry_id, self.__user_id, str(date), str(time), "Idle", "Idle", "Idle",))
        self.__conn.commit()

    def viewPastSessions(self):
        pass

    def viewGeneralData(self):
        pass

    def getIdByObj(self):
        pass

    def get_id_by_name(self, username, password=None):

        if not username:
            username = self.__username
        if not password:
            password = self.__password

        self.__cur.execute(GET_ID_BY_NAME, (username,))
        user_id = self.__cur.fetchone()[0]
        return user_id

    def get_entry_id_by_date_time_and_user_id(self, date, time, user_id):

        if not user_id:
            user_id = self.__user_id

        self.__cur.execute(GET_ENTRY_ID_BY_DATE_TIME_AND_USER_ID, (str(date), str(time), user_id,))
        entry_id = self.__cur.fetchone()[0]
        return entry_id

    def get_all_entries(self):
        self.__cur.execute(GET_ALL_ENTRY_ID_BY_USER_ID, (self.__user_id,))
        entries = self.__cur.fetchall()
        return entries

    def get_logs_by_entry_id(self, entry_id):
        entry_id = str(entry_id)
        self.__cur.execute(GET_LOGS_BY_ENTRY_ID, (entry_id,))
        return self.__cur.fetchall()

class User():
    def __init__(self, user_id=None, username=None, password=None, logged_in=None):
        self.__username = username
        self.__user_id = user_id
        self.__password = password
        self.logged_in = logged_in
        self.table = TableConnection(self.__user_id, self.__username, self.__password)

    def set_id(self, username, password):
        self.__user_id = self.table.get_id_by_name(username)

    def get_id(self):
        return self.__user_id

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def login(self, username, password):
        try:
            self.set_id(username, password)
            self.__username = username
            self.__password = password
            if not self.logged_in:
                self.logged_in = True
                print("id " + str(self.__user_id))
                self.table.access_to_table(self.__user_id, self.__username, self.__password)
        except ValueError:
            print("username and password both need to be type string")

    def register(self, username, password):
        try:
            if self.table.if_user_exists(username):
                print("Username already exists, create another username")
            else:
                self.table.create_user(username, password)
                self.login(username, password)
        except ValueError:
            print("username and password both need to be type string")
