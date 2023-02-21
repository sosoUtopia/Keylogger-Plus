from tktools.tkroot import DefaultWindow
from user import User
from key_logger import Logger
from tkinter import *
from tkinter import messagebox
from tktools.tk_functions import TkFunctions as tf
from analyzer import Analyzer
import datetime as t
from pynput.keyboard import Key, Listener
import threading
from collections import OrderedDict
from pprint import pprint
# from key_logger import *

class LoginPage(Frame):
    def __init__(self, parent, controller, controller_user : User):
        Frame.__init__(self, parent)
        self.user = controller_user
        self.main_menu(controller)

    def main_menu(self, controller):
        print("menu")
        username_label = tf.make_center_label(self, "Username")
        username_label.pack()

        username = StringVar()
        user_entry_box = tf.make_center_entry(self, username, 20)
        user_entry_box.focus()
        user_entry_box.pack()

        pwd_label = tf.make_center_label(self, "Password")
        pwd_label.pack()

        pwd = StringVar()
        pwd_entry_box = tf.make_center_entry(self, pwd, 20, "*")
        pwd_entry_box.pack()
    
        login_button = tf.make_center_button(self, "Login", command=lambda:self.login_after_verified(username.get(), pwd.get(), controller))
        login_button.pack()

        registration_text = "New user? Click here to register"
        registration_page = tf.make_center_button(self, registration_text, command=lambda:controller.show_frame(RegistrationPage))
        registration_page.pack()

    def login_after_verified(self, name, pwd, controller):
        if self.user.table.is_valid_login(name, pwd):
            self.user.login(name, pwd)
            controller.show_frame(SessionPage)
        else:
            print(name, pwd)
            messagebox.showerror("Failed", "Incorrect Login-Passowrd combination!")

class EntriesPage(Frame):
    def __init__(self, parent, controller, controller_user : User):
        Frame.__init__(self, parent)
        self.user = controller_user
        self.analyzer = Analyzer(self.user)
        login_button = tf.make_center_button(self, "entries", command=lambda:self.show_all_entries(controller))
        login_button.pack()
    
    def show_all_entries(self, controller):
        print(self.user.get_id())
        entries = self.user.table.get_all_entries()
        entries_dict = OrderedDict()
        entries_set = set()
        for entry in entries:
            try: 
                entries_dict[entry[0]] = {
                    "start day" : entry[1],
                    "end day" : entry[2],
                    "start time": entry[3],
                    "end time": entry[4],
                }
            except TypeError:
                continue
        pprint(entries_dict)

        entry_label = tf.make_center_label(self, "Choose entry")
        entry_label.pack()

        entry = IntVar()
        entry = tf.make_center_entry(self, 20)
        entry.pack()
    
        login_button = tf.make_center_button(self, "Words Per Minute", command=lambda:self.get_words_per_minute(entry.get(), controller))
        login_button.pack()
        pass

    def get_words_per_minute(self, entry, controller):
        print("hello")
        print(entry)
        self.analyze_entry(entry)
        self.analyzer.get_words_per_minutes()
        pass

class SessionPage(Frame):
    def __init__(self, parent, controller, controller_user : User):
        Frame.__init__(self, parent)
        self.user = controller_user
        self.session_page(controller)

    def session_page(self, controller):
        login_button = tf.make_center_button(self, "Start Record", command=lambda:self.start_record(controller))
        login_button.pack()

        login_button = tf.make_center_button(self, "Show All Entries", command=lambda:controller.show_frame(EntriesPage))
        login_button.pack()

    def start_record(self, controller):
        date = t.datetime.now().date()
        time = t.datetime.now().time()
        user_id = self.user.get_id()
        # self.user.table.insert_start_entry(str(date), str(time), user_id,)
        # logger = Logger(self.user)
        # logger.start_log()
        # logger.counter.counter.start()
        # with Listener(on_press=logger.on_press, on_release=logger.on_release, suppress = False) as listener:
        #     listener.start()


class RegistrationPage(Frame):
    def __init__(self, parent, controller, controller_user : User):
        Frame.__init__(self, parent)
        self.user = controller_user
        self.registration_page(controller)

    def registration_page(self, controller):
        new_username = StringVar()
        new_user_label = tf.make_center_label(self, "Create your username")
        user_entry_box = tf.make_center_entry(self, new_username, 20)
        new_user_label.pack()
        user_entry_box.focus()
        user_entry_box.pack()

        new_password = StringVar()
        newpwd_label = tf.make_center_label(self, "Create your password")
        pwd_entry_box = tf.make_center_entry(self, new_password, 20, "*")
        newpwd_label.pack()
        pwd_entry_box.pack()

        registration_text = "Register"
        registration_page = tf.make_center_button(self, registration_text, lambda:self.register_and_login_after_verify(new_username.get(), new_password.get(), controller))
        registration_page.pack()

    def register_and_login_after_verify(self, name, pwd, controller):
        if self.user.table.if_user_exists(name):
            messagebox.showerror("Failed", "Username already taken!")
        else:
            self.user.register(name, pwd)
            controller.show_frame(SessionPage)

class App(Tk):
    def __init__(self, u: User, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.user = u
        self.title("KeyLogger-Plus")
        ws = self.winfo_screenwidth() 
        hs = self.winfo_screenheight() 
        w = 500
        h = 500
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.resizable(0,0)
        root_window = Frame(self)
        root_window.pack()

        self.frames = {}
        for F in (LoginPage, RegistrationPage, SessionPage, EntriesPage):
            frame = F(root_window, self, self.user)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def start_window(self):
        self.show_frame(LoginPage)
        self.mainloop()

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


user = User()
app = App(user)
app.start_window()
