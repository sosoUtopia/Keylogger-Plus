from tkinter import *

class TkFunctions():
    def make_center_label(parent : Frame, phrase=None):
        print("center label")
        label = Label(parent, text=phrase)
        label.config(anchor=CENTER)
        return label

    def make_center_entry(parent : Frame, term=None, width=None, show=None):
        entry_box = Entry(parent, textvariable=term, width=width, show=show)
        return entry_box

    def make_center_button(parent : Frame, phrase, command):
        button = Button(parent, text=phrase, command=command)
        button.config(anchor=CENTER)
        button.config(pady=5)
        return button