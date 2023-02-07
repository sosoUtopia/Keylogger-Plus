from tkinter import *

class DefaultWindow():
    def get_root(self):
        default_window = Tk()
        ws = default_window.winfo_screenwidth() 
        hs = default_window.winfo_screenheight() 
        w = 500
        h = 500
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        default_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        default_window.resizable(0,0)
        return default_window
