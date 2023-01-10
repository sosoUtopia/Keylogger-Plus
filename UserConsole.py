from tkinter import *
from tkinter import messagebox
import datetime as t
from User import *

user = User()
class UserConsole():
    def __init__(self, root):
        root.title("Keylogger Plus")
        ws = root.winfo_screenwidth() 
        hs = root.winfo_screenheight() 
        w = 500
        h = 500
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        root.resizable(0,0)
        self.frame = root
        self.main_menu()

    def main_menu(self):
        for i in self.frame.winfo_children():
            i.destroy()
        username_label = self.make_center_label("Username")
        username_label.pack()

        username = StringVar()
        user_entry_box = self.make_center_entry(username, 20)
        user_entry_box.focus()
        user_entry_box.pack()

        pwd_label = self.make_center_label("Password")
        pwd_label.pack()

        pwd = StringVar()
        pwd_entry_box = self.make_center_entry(pwd, 20, "*")
        pwd_entry_box.pack()

        login_button = self.make_center_button("Login", lambda:self.login_after_verify_login(username.get(), pwd.get()))
        login_button.pack()

        registration_text = "New user? Click here to register"
        registration_page = self.make_center_button(registration_text, lambda:self.registration_page())
        registration_page.pack()

    def make_center_label(self, phrase=None, ):
        label = Label(self.frame, text=phrase)
        label.config(anchor=CENTER)
        return label

    def make_center_entry(self, term=None, width=None, show=None):
        entry_box = Entry(self.frame, textvariable=term, width=width, show=show)
        return entry_box

    def make_center_button(self, phrase, command):
        button = Button(self.frame, text=phrase, command=command)
        button.config(anchor=CENTER)
        button.config(pady=5)
        return button

    def login_after_verify_login(self, name, pwd):
        if user.table.isValidLogin(name, pwd):
            user.login(name, pwd)
            self.menu_after_logged_in()
        else:
            print(name, pwd)
            messagebox.showerror("Failed", "Incorrect Login-Passowrd combination!")

    def register_after_verify(self, name, pwd):
        if user.table.if_user_exists(name):
            messagebox.showerror("Failed", "Username already taken!")
        else:
            user.register(name, pwd)
            self.menu_after_logged_in()

    def menu_after_logged_in(self):
        for i in self.frame.winfo_children():
            i.destroy()

        begin_session_button = self.make_center_button("Start Session", self.beginKeylogger)
        begin_session_button.pack(pady=10)

    def beginKeylogger(self):
        start_date = t.datetime.now().date()
        start_time = t.datetime.now().time().replace(microsecond=0)
        user_id = user.id
        user.table.insert_start_entry(start_date, start_time, user_id)
        entry_id = user.table.get_entry_id_by_date_time_and_user_id(start_date, start_time, user_id)
        # while recordUser(user, entry_id) is True:
        #     pass
        # self.frame.mainloop()

        # with Listener(on_press=onPress) as listener:
        #     listener.join()

    def registration_page(self):
        for i in self.frame.winfo_children():
                i.destroy()

        new_username = StringVar()
        new_user_label = self.make_center_label("Create your username")
        user_entry_box = self.make_center_entry(new_username, 20)
        new_user_label.pack()
        user_entry_box.focus()
        user_entry_box.pack()

        new_password = StringVar()
        newpwd_label = self.make_center_label("Create your password")
        pwd_entry_box = self.make_center_entry(new_password, 20, "*")
        newpwd_label.pack()
        pwd_entry_box.pack()

        registration_text = "Register"
        registration_page = self.make_center_button(registration_text, lambda:self.register_after_verify(new_username.get(), new_password.get()))
        registration_page.pack()

        get_back_text = "Go back"
        goBackButton = self.make_center_button(get_back_text, self.main_menu)
        goBackButton.pack()

root = Tk()
UserConsole(root)
root.mainloop()