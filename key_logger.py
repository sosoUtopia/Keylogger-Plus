from pynput.keyboard import Key, Listener
from user import *
from counter import *
import threading
import datetime as t
import string

username = ""
password = ""
user = User()
entry_id = None
timestamp = t.datetime.now()
log_every_second = None

class Counter():
    def __init__(self, user):
        self.counter = threading.Thread(target=self.run)
        self.idle_status = "Idle"
        self.curr_datetime_list = []
        self.db_datetime_list = []
        self.curr_datetime = t.datetime.now()
        self.curr_date = str(t.datetime.now().date())
        self.curr_time = str(t.datetime.now().time())
        # self.counter.start()

    def start_counter(self):
        self.counter.start()

    def run(self):
        global timestamp 
        global log_every_second
        log_every_second = threading.Timer(1.0, self.run)
        log_every_second.start()
        self.curr_datetime = t.datetime.now()
        self.curr_date = str(t.datetime.now().date())
        self.curr_time = str(t.datetime.now().time())
        self.curr_datetime_list = [self.curr_date, self.curr_time]
        self.db_datetime_list.append(self.curr_datetime_list)
        if (self.curr_datetime - timestamp).total_seconds() >= 5:
            timestamp = t.datetime.now()
            for row in self.db_datetime_list:
                user.table.log_idle_status(row[0], row[1])
                print(
                    str(user.table.get_current_entry_id()) 
                    + " " + str(user.get_id()) + ' ' +row[0] 
                    + ' ' + row[1] 
                    + ' ' + self.idle_status 
                    + ' ' + self.idle_status 
                    + ' ' + self.idle_status
                    )
            self.db_datetime_list.clear()
            self.curr_datetime_list.clear()
            
class Logger():
    def __init__(self, user):
        global timestamp
        timestamp = t.datetime.now()
        self.current_key = ""
        self.date = t.datetime.now().date()
        self.time = t.datetime.now().time()
        self.active_status = "Active"
        self.keys = []
        self.append_string = ""
        self.command_keys = {
            "Key.alt", "Key.alt_l", "Key.alt_r", "Key.alt_gr", "Key.backspace", 
            "Key.caps_lock", "Key.cmd", "Key.cmd_l", "Key.cmd_r", "Key.ctrl", 
            "Key.ctrl_l", "Key.ctrl_r", "Key.delete", "Key.down", "Key.end",
            "Key.enter", "Key.esc", "Key.f1", "Key.f2", "Key.F3", 
            "Key.f4", "Key.f5", "Key.f6", "Key.f7", "Key.f8", "Key.f9", "Key.f10", 
            "Key.f11", "Key.f12", "Key.f13", "Key.f14", "Key.f15", "Key.f17", 
            "Key.f18", "Key.f20", "Key.home", "Key.left", "Key.page_down", "Key.page_up", 
            "Key.right", "Key.shift", "Key.shift_l", "Key.shift_r", "Key.space", 
            "Key.tab", "Key.up", "Key.media_volume_mute", "Key.media_volume_down", 
            "Key.media_volumn_up", "Key.media_prev", "Key.media_next", "Key.insert", 
            "Key.menu", "Key.num_lock", "Key.pause", "Key.print_screen", "Key.scroll_lock"
        }

        self.insert_to_db = {
            "command" : self.flush_command_keys,
            "number" : self.flush_numerics,
            "alphabet" : self.flush_word,
            "punctuation": self.insert_single_punc,
            "special": self.flush_special
        }

        self.counter = Counter(user)
        # with Listener(on_press=self.on_press, on_release=self.on_release, supress=True) as listener:
        #     listener.join()
    def record(self):
        # self.counter.start_counter()
        listener = Listener(on_press=self.on_press, on_release=self.on_release, supress=False)
        listener.join()


    def start_log(self):
        # self.thread = threading.Thread(target=self.record)
        # self.thread.start()
        self.counter.start_counter()
        with Listener(on_press=self.on_press, on_release=self.on_release, supress=False) as listener:
            listener.start()

    def on_press(self, key):
        global timestamp
        timestamp = t.datetime.now()

        if self.counter.curr_datetime_list: 
            self.counter.curr_datetime_list.clear()
        if self.counter.db_datetime_list:
            self.counter.db_datetime_list.clear()
 
        self.current_key = str(key).replace("'", '')
        if self.current_key == '""':
            self.current_key = "'"
        self.keys.append(self.current_key)
        
        type = self.curr_type()

        if type == "command":
            if self.has_precedence_of_different_type() and self.prev_key() == "'" and len(self.keys) >= 3:
                self.flush_word()
            elif self.has_precedence_of_different_type():
                self.insert_to_db[self.prev_type()]()
        elif type == "alphabet":
            if self.has_precedence_of_different_type():
                if self.prev_key() == "'":
                    pass
                else:
                    self.insert_to_db[self.prev_type()]()
        elif type == "number":
            if self.has_precedence_of_different_type():
                if len(self.keys) >= 1 and self.prev_type() != "number":
                    if self.prev_type() == "punctuation":
                        self.flush_word()
                    else:
                        self.insert_to_db[self.prev_type()]()
        elif type == "punctuation":
            if self.has_precedence_of_different_type():
                if self.prev_type() == "alphabet" and self.current_key == "'":
                    pass
                else:
                    self.insert_to_db[self.prev_type()]()
            elif self.current_key != "'":
                self.insert_single_punc()
            elif self.current_key == "'" and self.prev_key() == "'" and len(self.keys) == 2:
                self.flush_punc()
        elif type == "special":
            self.flush_special()

    def curr_type(self) -> str:
        if self.current_key in self.command_keys:
            return "command"
        elif self.current_key.isalpha():
            return "alphabet"
        elif self.current_key.isnumeric():
            return "number"
        elif self.current_key in string.punctuation:
            return "punctuation"
        else:
            return "special"

    def type(self, key):
        if key in self.command_keys:
            return "command"
        elif key.isalpha():
            return "alphabet"
        elif key.isnumeric():
            return "number"
        elif key in string.punctuation:
            return "punctuation"
        else:
            return "special"

    def prev_type(self) -> str:
        this_key : str = self.keys[len(self.keys) - 2]
        if this_key in self.command_keys:
            return "command"
        elif this_key.isalpha():
            return "alphabet"
        elif this_key.isnumeric():
            return "number"
        elif this_key in string.punctuation:
            return "punctuation"
        else:
            return "special"

    def prev_key(self):
        if len(self.keys) > 1:
            return self.keys[len(self.keys) - 2]

    def insert_term_to_db(self, status_type):
        self.date = t.datetime.now().date()
        self.time = t.datetime.now().time()
        user.table.log(self.date, self.time, status_type, self.append_string)
        print(" ".join(
            ["log id", 
            str(user.table.get_current_entry_id()), 
            str(user.get_id()), 
            str(self.date), 
            str(self.time), 
            self.active_status, 
            status_type, 
            self.append_string]))
        self.append_string = ""

    def flush_command_keys(self) -> None:
        while len(self.keys) > 0:
            self.append_string += self.keys.pop(0) + " "
        self.append_string.rstrip()
        print(self.append_string)
        self.insert_term_to_db("Command")
    
    def insert_special(self) -> None:
        while len(self.keys) > 0:
            self.append_string += self.keys.pop(0)
        self.insert_term_to_db("Special")

    def insert_single_punc(self) -> None:
        if len(self.keys) > 0:
            self.append_string += self.keys.pop(0)
            self.insert_term_to_db("Punctuation")

    def flush_special(self) -> None:
        while len(self.keys) > 0:
            self.append_string += self.keys.pop(0)
            self.insert_term_to_db("Punctuations or Special")

    def flush_punc(self) -> None:
        while len(self.keys) > 0:
            self.append_string += self.keys.pop(0)
            self.insert_term_to_db("Punctuation")

    def flush_word(self) -> None:
        while len(self.keys) > 1:
            self.append_string += self.keys.pop(0)
        self.insert_term_to_db("Word")

    def flush_numerics(self) -> None:
        while len(self.keys) > 1:
            self.append_string += self.keys.pop(0)
        self.insert_term_to_db("Numeric")

    def has_precedence_of_different_type(self) -> bool:
        if len(self.keys) > 1: 
            if self.curr_type() != self.prev_type():
                return True
        else: 
            return False

    def on_release(self, key):
        global log_every_second
        if str(key) == "Key.esc":
            self.insert_to_db[self.curr_type()]()
            log_every_second.cancel()
            return False

    def log(self):
        pass

# def ask_for_login():
#     global username 
#     username = str(input("Username: "))
#     global password
#     password = str(input("Password: "))
#     if user.table.is_valid_login(username, password):
#         global entry_id
#         user.login(username, password)
#         start_date = t.datetime.now().date()
#         start_time = t.datetime.now().time()
#         user_id = user.get_id()
#         user.table.insert_start_entry(start_date, start_time, user_id)
#     else:
#         print("Not Valid!")
#         ask_for_login()
#         return

# ask_for_login()
# print("Recording is in process")
# Logger(user).start_log()
# user.table.insert_end_entry(t.datetime.now().date(), t.datetime.now().time().replace())
# user.table.disconnect_db()