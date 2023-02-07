# class Counter():
#     def __init__(self, user):
#         self.counter = threading.Thread(target=self.run)
#         self.curr_datetime = t.datetime.now()
#         self.curr_date = str(t.datetime.now().date())
#         self.curr_time = str(t.datetime.now().time())
#         self.counter.start()
#         self.idle_status = "Idle"
#         self.curr_datetime_list = []
#         self.db_datetime_list = []

#     def run(self):
#         global timestamp 
#         global log_every_second
#         log_every_second = threading.Timer(1.0, self.run)
#         log_every_second.start()
#         self.curr_datetime = t.datetime.now()
#         self.curr_date = str(t.datetime.now().date())
#         self.curr_time = str(t.datetime.now().time())
#         self.curr_datetime_list = [self.curr_date, self.curr_time]
#         self.db_datetime_list.append(self.curr_datetime_list)
#         if (self.curr_datetime - timestamp).total_seconds() >= 5:
#             timestamp = t.datetime.now()
#             for row in self.db_datetime_list:
#                 print(str(user.table.entry_id) + ' ' + str(user.id) + ' ' +row[0] + ' ' +row[1] + ' ' + self.idle_status + ' ' + self.idle_status + ' ' + self.idle_status)
#                 user.table.log_idle_status(row[0], row[1])
#             self.db_datetime_list.clear()
#             self.curr_datetime_list.clear()