import tkinter as tk
from tkinter import ttk
from tkinter.constants import *

class ListItem(ttk.Frame):
    def __init__(self, mainframe, name, distance, time, rating):
        ttk.Frame.__init__(self, mainframe)
        self.name        = tk.StringVar(self, value=name)
        self.distance    = tk.StringVar(self, value=distance)
        self.time        = tk.StringVar(self, value=time)
        self.rating      = tk.StringVar(self, value=rating)
        # self.photo = photo
        self.initUI()

    def initUI(self):
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=("Consolas", 12, "bold"))
        self.style.configure("subTitle.TLabel", font=("Consolas", 10, "bold"))
        self.style.configure("Detail.TLabel", font=("Consolas", 10, "normal"))

        self.name_label      = ttk.Label(self, textvariable=self.name,       style="Title.TLabel", background='lightblue')
        self.distance_label  = ttk.Label(self, textvariable=self.distance,   style="Detail.TLabel", background='lightblue')
        self.time_label      = ttk.Label(self, textvariable=self.time,       style="Detail.TLabel", background='lightblue')
        self.rating_label    = ttk.Label(self, textvariable=self.rating,     style="Detail.TLabel", background='lightblue')

        self.name_label      .configure(style="Title.TLabel")
        self.distance_label  .configure(style="Detail.TLabel")
        self.time_label      .configure(style="Detail.TLabel")
        self.rating_label    .configure(style="Detail.TLabel")

        self.name_label      .grid(column=0, row=0, columnspan=2, sticky=W)
        self.distance_label  .grid(column=1, row=1, columnspan=2, sticky=W)
        self.time_label      .grid(column=1, row=2, columnspan=2, sticky=W)
        self.rating_label    .grid(column=1, row=3, columnspan=2, sticky=W)