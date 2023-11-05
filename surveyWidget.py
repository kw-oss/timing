import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from typing import List, Dict

class SurveySet(ttk.Frame):
    # creates a questionaire in tabular form, with given score names and subtitles
    def __init__(self, container, score_names: List[int], subtitles: List[str], *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        # instance members
        self.score_labels: [ttk.Label] = []
        self.radio_sets: List[RadioSet] = []
        self.answers: Dict[str, tk.IntVar] = {}

        # set default value of answers, and initialize self.answers
        default_value = (len(score_names) - 1) // 2
        for subtitle in subtitles:
            self.answers[subtitle] = tk.IntVar(self, value=default_value)

        # set score_label row
        for i, score_name in enumerate(score_names):
            # workaround for radio button's misalignment to center
            score_name += " "

            new_label = ttk.Label(self, text=score_name)
            new_label.grid(column=i+1, row=0)
            
            self.score_labels.append(new_label)

        # set radio_set rows
        for i, subtitle in enumerate(subtitles):
            new_radioset = RadioSet(self, pos=(0, i+1), title=subtitle, radio_count=len(score_names), variable=self.answers[subtitle])

            self.radio_sets.append(new_radioset)

        # set column weight
        self.columnconfigure(0, weight=0)
        for i in range(len(score_names)):
            # uniform: share common width between columns that has same key str
            self.columnconfigure(i+1, weight=2, uniform="radio set")

        # set row weight
        for i in range(len(subtitles)):
            self.rowconfigure(i+1, weight=2)

class RadioSet:
    # create and attach a label and number of radio button to container, start at given position
    def __init__(self, container, pos: (int, int), title: str, radio_count: int, variable: tk.IntVar, *args, **kwargs):
        # instance members
        self.radio: List[ttk.Radiobutton] = []
        self.label: ttk.Label
        self.variable = variable
        
        (col, row) = pos
        
        # set title label
        self.label = ttk.Label(container, text=title)
        self.label.grid(column=col, row=row, sticky=E, padx=(0, 10))

        # set radio buttons
        for i in range(radio_count):
            col += 1
        
            new_radio = ttk.Radiobutton(container, text="", value=i, variable=self.variable)
            new_radio.grid(column=col, row=row)
            
            self.radio.append(new_radio)