import tkinter as tk
from tkinter import ttk, simpledialog

class LoadingDialog(simpledialog.Dialog):
    def __init__(self, parent, data: list, *args, **kwargs):
        self.data = data
        self.default_text = "주변의 맛집을 검색하고 있어요"
        super().__init__(parent, *args, **kwargs)

    def body(self, master, ):
        self.text = tk.StringVar(self, value=self.default_text)
        self.label = ttk.Label(master, textvariable=self.text, foreground='dimgray', background='#F8F5E2', font=("NanumGothic", 12, "bold"))
        self.label.grid(padx=10, pady=10)
        master.configure(background='#F8F5E2', highlightthickness=0)

        self.resizable(False, False)
        self.geometry("300x200")
        
        self.configure(background='#F8F5E2')
        
        self.refresh()

    def refresh(self):
        if self.text.get().count(".") < 3:
            self.text.set(self.text.get() + ".")
        else:
            self.text.set(self.default_text)

        if len(self.data) > 0:
            self.destroy()

        self.after(500, self.refresh)

    # remove default button
    def buttonbox(self):
        pass