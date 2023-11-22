import tkinter as tk
from tkinter import ttk
from tkinter.constants import *

class ListItem(ttk.Frame):
    def __init__(self, mainframe, name, distance, time, rating, review_text):
        ttk.Frame.__init__(self, mainframe)
        self.name        = tk.StringVar(self, value=name)
        self.distance    = tk.StringVar(self, value=distance)
        self.time        = tk.StringVar(self, value=time)
        self.rating      = tk.StringVar(self, value=rating) 
        self.review_text = tk.StringVar(self, value=review_text)
        # self.photo = photo
        self.initUI()

    def initUI(self):
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=("Malgun Gothic", 12, "bold"))
        self.style.configure("subTitle.TLabel", font=("Malgun Gothic", 10, "bold"))
        self.style.configure("Detail.TLabel", font=("Malgun Gothic", 10, "normal"))

        self.name_label      = ttk.Label(self, textvariable=self.name,        style="Title.TLabel",  background='peachpuff', foreground='black')
        self.distance_label  = ttk.Label(self, textvariable=self.distance,    style="Detail.TLabel", background='peachpuff', foreground='black')
        self.time_label      = ttk.Label(self, textvariable=self.time,        style="Detail.TLabel", background='peachpuff', foreground='black')
        self.rating_label    = ttk.Label(self, textvariable=self.rating,      style="Detail.TLabel", background='peachpuff', foreground='black')
        self.review_label    = ttk.Label(self, textvariable=self.review_text, style="Detail.TLabel", background='peachpuff', foreground='black')

        self.name_label      .configure(style="Title.TLabel")
        self.distance_label  .configure(style="Detail.TLabel")
        self.time_label      .configure(style="Detail.TLabel")
        self.rating_label    .configure(style="Detail.TLabel")
        self.review_label    .configure(style="Detail.TLabel")

        self.name_label      .grid(column=0, row=0, sticky=W)
        self.distance_label  .grid(column=0, row=1, sticky=W)
        self.time_label      .grid(column=0, row=2, sticky=W)
        self.rating_label    .grid(column=0, row=3, sticky=W)
        self.review_label    .grid(column=0, row=4, sticky=W)