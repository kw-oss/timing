import tkinter as tk
from tkinter import ttk, simpledialog
from typing import List

class LoadingDialog(simpledialog.Dialog):
    def __init__(self, parent, task_canceled: List[bool], *args, **kwargs):
        self.task_canceled = task_canceled
        super().__init__(parent, *args, **kwargs)

    def body(self, master):
        self.text = tk.StringVar(self, value="Loading...")
        self.label = ttk.Label(master, textvariable=self.text)
        self.label.grid(padx=10, pady=10)

        self.resizable(False, False)
        self.geometry("130x50")
        
        self.refresh()
        
        # temporary - auto destroy after 3 seconds
        self.after(3000, self.destroy)

    def refresh(self):
        if self.text.get().count(".") < 3:
            self.text.set(self.text.get() + ".")
        else:
            self.text.set("Loading")

        self.after(500, self.refresh)

    # remove default button
    def buttonbox(self):
        pass

    def cancel(self):
        # TODO: cancel main button task
        
        self.task_canceled[0] = True

        super().cancel()