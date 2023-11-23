import tkinter as tk
from tkinter import ttk

class AutoHidingScrollbar(ttk.Scrollbar):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.container = container

    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.grid_remove()
            self.container.canvas.unbind_all("<MouseWheel>")
        else:
            self.grid()
            self.container.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        ttk.Scrollbar.set(self, low, high)

    def _on_mousewheel(self, event):
        scroll_speed = 20
        self.container.canvas.yview_scroll(-1 * int(event.delta/120) * scroll_speed, "units")


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.scrollbar = AutoHidingScrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = self._setScrollableFrame()

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.configure(yscrollincrement='1') # prevent dynamic scroll speed based on content size
        self.canvas.configure(background='#F8F5E2')
        self.canvas.configure(highlightthickness=0)

        self.canvas.grid(row=0, column=0, sticky="nswe")
        self.scrollbar.grid(row=0, column=1, sticky="ens")
    
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def _setScrollableFrame(self) -> ttk.Frame:
        scrollable_frame = ttk.Frame(self.canvas)
        # <Configure> event
        # triggered whenever its size, position, or border width changes, and sometimes when it has changed position in the stacking order.
        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        style = ttk.Style()
        style.configure('Scroll.TFrame', background='#F8F5E2')
        scrollable_frame.configure(style='Scroll.TFrame')

        return scrollable_frame
        
    def clear(self):
        self.canvas.delete("all")
        self.scrollable_frame = self._setScrollableFrame()