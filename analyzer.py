from user import User
import pandas as pd
import numpy as np
import pandas as pd
import sqlite3
from collections import OrderedDict
from pprint import pprint
import matplotlib.pyplot as plt
import itertools
from textblob import TextBlob
import datetime 

class Analyzer:
    def __init__(self, user: User):
        self.__user = user

    def get_words_per_minutes(self, entry_id):
        print(entry_id)
        print(self.__user.get_id())
        query = self.__user.table.get_logs_by_entry_id(entry_id)
        print("QUERY HERE")
        pprint(query)
        print(len(query))
        logs_dict = OrderedDict()
        for logs in query:
            # print("heloo")
            try: 
                print(str(logs[0]) + " " +str(logs[1]) + " " +str(logs[2]) + " " +str(logs[3]) )
                logs_dict[logs[0]] = {
                    "FK_logs_entry_id": logs[1],
                    "FK_logs_user_id": logs[2],
                    "logged_date": logs[3],
                    "logged_time": logs[4],
                    "status": logs[5],
                    "status_type": logs[6],
                    "term": logs[7],
                }
            except TypeError:
                pass

        avg_dict = {}
        time_frame = {}
        avg : float
        prev_log = False
        avg_list = []
        for entry_id, value in logs_dict.items():
            details = logs_dict[entry_id]
            curr_date = " ".join([details["logged_date"], details["logged_time"]])
            if details["status"] == "Idle":
                avg_list = []
                avg_dict[curr_date] = 0
            else:
                if details["status_type"] == "Word":
                    print("getting")
                    word = details["term"]
                    if avg_list:
                        avg_list.append(word)
                        time_frame["end"] = curr_date
                        start_time = datetime.datetime.strptime(
                            time_frame["start"], 
                            "%Y-%m-%d %H:%M:%S"
                            )
                        end_time = datetime.datetime.strptime(
                            time_frame["end"], 
                            "%Y-%m-%d %H:%M:%S")
                        time_index = end_time - start_time
                        speed_index = np.divide(np.average(len(avg_list)), time_index.total_seconds)
                        avg_dict[curr_date] = speed_index
                    else:
                        avg_list.append(word)
                        time_frame["start"] = curr_date
                        speed_index = np.average(len(avg_list)) 
                        avg_dict[curr_date] = speed_index
                    
        pprint(avg_dict)
        plt.plot(list(avg_dict.keys()),list(avg_dict.values()))
        plt.show();
   
        # print("LOGS HERE")
        # print(len(logs_dict))
        # pprint(logs_dict)

    def get_sentiments(self, entry_id):
        print(entry_id)
        print(self.__user.get_id())
        query = self.__user.table.get_logs_by_entry_id(entry_id)
        print("QUERY HERE")
        pprint(query)
        print(len(query))
        logs_dict = OrderedDict()
        for logs in query:
            # print("heloo")
            try: 
                print(str(logs[0]) + " " +str(logs[1]) + " " +str(logs[2]) + " " +str(logs[3]) )
                logs_dict[logs[0]] = {
                    "FK_logs_entry_id": logs[1],
                    "FK_logs_user_id": logs[2],
                    "logged_date": logs[3],
                    "logged_time": logs[4],
                    "status": logs[5],
                    "status_type": logs[6],
                    "term": logs[7],
                }
            except TypeError:
                pass
        nullifiable_keys = {
            'Key.shift', 'Key.shift_l', 'Key.shift_r',
            'Key.space'
        }
        sentiment_dict = {}
        sentiment_str = str;
        
        for entry_id, value in logs_dict.items():
            details = logs_dict[entry_id]
            curr_date = " ".join([details["logged_date"], details["logged_time"]])
            status_type = details["status_type"]
            if status_type == "word" or status_type == "special":
                sentiment_str += details["term"] + " "
            elif status_type == "command":
                if details['term'] not in nullifiable_keys:
                    if len(sentiment_str) > 0:
                        sentiment_str += details['term']
                        sentiment : float
                        sentiment = TextBlob.polarity(sentiment_str)
                        sentiment_dict[curr_date] = sentiment
                        sentiment_str = ""
            elif status_type == "Idle":
                curr_date = " ".join(details["logged_date"], details["logged_time"])
                if len(sentiment_str) > 0:
                    sentiment : float
                    sentiment = TextBlob.polarity(sentiment_str)
                    sentiment_dict[curr_date] = sentiment
                    sentiment_str = ""
                else:
                    sentiment_dict[curr_date] = 0

        print(sentiment_dict)