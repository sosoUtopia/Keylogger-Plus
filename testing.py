from tktools.tkroot import DefaultWindow
from user import User
# from key_logger import Logger
from tkinter import *
from tkinter import messagebox
from tktools.tk_functions import TkFunctions as tf
from analyzer import Analyzer
import datetime as t
from pynput.keyboard import Key, Listener
import threading
from collections import OrderedDict
from pprint import pprint
import sqlite3

conn = sqlite3.connect("userdata.db", check_same_thread=False, timeout=500)
