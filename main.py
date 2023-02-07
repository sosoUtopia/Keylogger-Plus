from window import App
from key_logger import Logger
from user import User
import datetime as t

user = User()
app = App(user)
app.start_window()

# print("Recording is in process")
# user.login("Alvin", "testingpassword123")
# start_date = t.datetime.now().date()
# start_time = t.datetime.now().time()
# user_id = user.get_id()
# user.table.insert_start_entry(start_date, start_time, user_id)
# Logger(user).start_log()
# user.table.insert_end_entry(t.datetime.now().date(), t.datetime.now().time().replace())
# user.table.disconnect_db()

app.mainloop()