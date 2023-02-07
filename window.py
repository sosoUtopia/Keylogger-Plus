from tktools.tkroot import DefaultWindow
from user import User
from key_logger import Logger
from tkinter import *
from tkinter import messagebox
from tktools.tk_functions import TkFunctions as tf
from analyzer import Analzyer
import datetime as t
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
    
class SessionPage(Frame):
    def __init__(self, parent, controller, controller_user : User):
        Frame.__init__(self, parent)
        self.user = controller_user
        self.session_page(controller)

    def session_page(self, controller):
        login_button = tf.make_center_button(self, "Start Record", command=lambda:self.start_record(controller))
        login_button.pack()

    def start_record(self, controller):
        date = t.datetime.now().date()
        time = t.datetime.now().time()
        user_id = self.user.get_id()
        self.user.table.insert_start_entry(str(date), str(time), user_id,)
        logger = Logger(self.user)
        logger.start_log()

class RegistrationPage(Frame):
    def __init__(self, parent, controller, controller_user : User):
        Frame.__init__(self, parent)
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

    def register_and_login_after_verify(self, name, pwd, controller, controller_user : User):
        if controller_user.table.if_user_exists(name):
            messagebox.showerror("Failed", "Username already taken!")
        else:
            controller_user.register(name, pwd)
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
        for F in (LoginPage, RegistrationPage, SessionPage):
            frame = F(root_window, self, self.user)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def start_window(self):
        self.show_frame(LoginPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

# App().mainloop()