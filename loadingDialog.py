import tkinter as tk
from tkinter import ttk, simpledialog

class LoadingDialog(simpledialog.Dialog):
    def __init__(self, parent, data: list, *args, **kwargs):
        self.data = data
        super().__init__(parent, *args, **kwargs)

    def body(self, master, ):
        self.text = tk.StringVar(self, value="주변의 맛집을 검색하고 있어요")
        self.label = ttk.Label(master, textvariable=self.text, foreground='black')
        self.label.grid(padx=10, pady=10)

        self.resizable(False, False)
        self.geometry("300x200")
        
        self.refresh()

    def refresh(self):
        if self.text.get().count(".") < 3:
            self.text.set(self.text.get() + ".")
        else:
            self.text.set("주변의 맛집을 검색하고 있어요")

        if len(self.data) > 0:
            self.destroy()

        self.after(500, self.refresh)

    # remove default button
    def buttonbox(self):
        pass