from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

# TODO: Add main window with button for running restorant searching algorithm and showing the result in the list

class ListItem(ttk.Frame):
    def __init__(self, mainframe, name, distance, time, rating):
        ttk.Frame.__init__(self, mainframe)
        self.name        = StringVar(self, value=name)
        self.distance    = StringVar(self, value=distance)
        self.time        = StringVar(self, value=time)
        self.rating      = DoubleVar(self, value=rating)
        # self.photo = photo
        self.initUI()

    def initUI(self):
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=("Consolas", 12, "bold"))
        self.style.configure("Detail.TLabel", font=("Consolas", 10, "normal"))

        self.name_label      = ttk.Label(self, textvariable=self.name,       style="Title.TLabel")
        self.distance_label  = ttk.Label(self, textvariable=self.distance,   style="Detail.TLabel")
        self.time_label      = ttk.Label(self, textvariable=self.time,       style="Detail.TLabel")
        self.rating_label    = ttk.Label(self, textvariable=self.rating,     style="Detail.TLabel")
        
        self.name_label      .configure(style="Title.TLabel")
        self.distance_label  .configure(style="Detail.TLabel")
        self.time_label      .configure(style="Detail.TLabel")
        self.rating_label    .configure(style="Detail.TLabel")

        self.name_label      .grid(column=0, row=0, columnspan=2, sticky=W)
        self.distance_label  .grid(column=0, row=1, columnspan=2, sticky=W)
        self.time_label      .grid(column=0, row=2, columnspan=2, sticky=W)
        self.rating_label    .grid(column=1, row=2, sticky=W)
        

if __name__ == '__main__':
    window = Tk()
    window.title("Result")

    # placeholder image for map area
    map_placeholder = ImageTk.PhotoImage(Image.open('image_placeholder.png'))

    # sticky == alignment(stick or fill)
    # column/rowconfigure(column/row_index, weight, minsize, pad(=padding))
    # weight == 0 means fixed, weight > 0 means expandable, each weight is a ratio with other widget's weight
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    mainframe = ttk.Frame(window, padding=5)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) # positioning to its parent
    
    mainframe.columnconfigure(0, weight=1) # setting inner grid
    mainframe.rowconfigure(0, weight=0)

    map = ttk.Label(mainframe, image=map_placeholder)
    map.grid(column=0, row=0, sticky=N)

    # give some placeholder item to the list
    item = ListItem(mainframe, "name", "distance", "time", 5)
    item.grid(column=0, row=1, sticky=[W, N])
    mainframe.rowconfigure(1, weight=1)

    # TODO: define list's scrollbar, and present the list with scrollbar
    # reference: 
    # https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
    # https://blog.teclado.com/tkinter-scrollable-frames/

    # set the window's size to fit the initial content
    window.update()
    window.minsize(window.winfo_width(), window.winfo_height())

    window.mainloop()
