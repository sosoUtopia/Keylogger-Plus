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
        self.logs_dict = OrderedDict()

    def analyze_entry(self, entry_id):
        query = self.__user.table.get_logs_by_entry_id(entry_id)
        print("QUERY HERE")
        pprint(query)
        print(len(query))
        for logs in query:
            # print("heloo")
            try: 
                print(str(logs[0]) + " " +str(logs[1]) + " " +str(logs[2]) + " " +str(logs[3]) )
                self.logs_dict[logs[0]] = {
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

    def get_words_per_minutes(self):
        avg_dict = {}
        time_frame = {}
        avg : float
        prev_log = False
        avg_list = []
        for entry_id, value in self.logs_dict.items():
            details = self.logs_dict[entry_id]
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
                        start_time = self.get_date_format(time_frame["start"])
                        end_time = self.get_date_format(time_frame["end"])
                        time_index = end_time - start_time
                        speed_index = np.divide(len(avg_list), time_index.total_seconds())
                        avg_dict[curr_date] = speed_index
                    else:
                        avg_list.append(word)
                        time_frame["start"] = curr_date
                        speed_index = np.average(len(avg_list)) 
                        avg_dict[curr_date] = speed_index
                    
        pprint(avg_dict)
        plt.xticks(rotation=50, fontsize=7)
        plt.plot(list(avg_dict.keys()),list(avg_dict.values()))
        plt.show();
    
    def get_date_format(self, time):
        time = datetime.datetime.strptime(
            time, 
            "%Y-%m-%d %H:%M:%S"
            )
        return time
   
    def get_sentiments(self, entry_id):
        nullifiable_keys = {
            'Key.shift', 'Key.shift_l', 'Key.shift_r',
            'Key.space'
        }
        sentiment_dict = {}
        current_sentiment = {}
        sentiment_str = str;
        
        for entry_id, value in self.logs_dict.items():
            word = details["term"]
            details = self.logs_dict[entry_id]
            curr_date = " ".join([details["logged_date"], details["logged_time"]])
            status_type = details["status_type"]
            if status_type == "Word" or status_type == "Special" or status_type == "Punctuation":
                if word not in nullifiable_keys:
                    current_sentiment['time'] = curr_date
                    if sentiment_str:
                        sentiment_str = " ".join([sentiment_str, word])
                        current_sentiment["phrase"] = sentiment_str
                    else:
                        sentiment_str = word
                        current_sentiment["phrase"] = sentiment_str
            # elif status_type == "command":
            elif details['term'] not in nullifiable_keys:
                phrase = current_sentiment["phrase"]
                time = current_sentiment["time"]
                if phrase:
                    sentiment : float
                    sentiment = TextBlob.polarity(phrase)
                    sentiment_dict[time]["phrase"] = phrase
                    sentiment_dict[time]["sentiment"] = sentiment
                    current_sentiment["phrase"] = None
                    current_sentiment["time"] = None
                if status_type == "Idle":
                    sentiment_dict[curr_date]["phrase"] = None
                    sentiment_dict[curr_date]["sentiment"] = 0
                
        pprint(sentiment_dict)
        plt.xticks(rotation=50, fontsize=7)
        plt.plot(list(sentiment_dict.keys()),list(sentiment_dict.values()))
        plt.show();

        print(sentiment_dict)