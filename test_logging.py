from key_logger import *
from user import User
import datetime as t

username = ""
password = ""
user = User()
entry_id = None
timestamp = t.datetime.now()

def ask_for_login():
    global username 
    username = str(input("Username: "))
    global password
    password = str(input("Password: "))
    if user.table.is_valid_login(username, password):
        global entry_id
        user.login(username, password)
        start_date = t.datetime.now().date()
        start_time = t.datetime.now().time()
        user_id = user.get_id()
        user.table.insert_start_entry(start_date, start_time, user_id)

        # user.table.disconnect_db()
    else:
        print("Not Valid!")
        ask_for_login()
        return
    
ask_for_login()
Logger(user).start_log()
user.table.insert_end_entry(t.datetime.now().date(), t.datetime.now().time().replace())
# user.table.disconnect_db();
