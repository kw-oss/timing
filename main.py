from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

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
        
def mainButtonPressed():
    # put some search result to `data`
    data = None
    displaySearchResult(data)
    print(preference)


def displaySearchResult(data):
    # hide question label
    questionLabel.grid_remove()
    foodCategoryCheckButtons.grid_remove()

    # prevents displaying large window bigger than minsize
    width = map_placeholder.width()
    window.geometry(f"{width}x{width}")
    # this will re-enable auto-resizing by systems when widgets are restored 
    window.geometry("") 

    # restore searched result UI layout
    mainframe.configure(padding=5)
    map.grid()
    item.grid()
    mainframe.rowconfigure(1, weight=1)
    buttomBar.grid()
    
    # change some layout configuration of runButton
    runButton.grid(sticky=S)
    mainframe.rowconfigure(3, weight=0)

    # set the window's size to fit the initial content
    (width, height) = currentWindowSize()
    window.minsize(width, height)
    window.maxsize(int(width * 1.5), height * 2)


def checkButtonList(master, names: set) -> ttk.Frame:
    frame = ttk.Frame(master)

    i = 0
    for name in names:
        name = str(name)
        check = ttk.Checkbutton(frame, text=name)
        
        # 'lambda n=name:' 구문: 현재 name 값을 n값으로 '즉시' 캡쳐
        # 즉시 캡쳐하지 않을 경우 lambda 표현식은 해당 변수를 '호출 시점'에 참조하므로 의도가 달라짐.
        check.configure(command=lambda n=name: listPushOrPop(n))
        check.state(['!alternate'])
        check.grid(column=0, row=i, sticky=W, pady=1)
        i += 1


    def listPushOrPop(name: str):
        if name in names:
            names.remove(name)
        else:
            names.add(name)


    names.clear()
    return frame


def currentWindowSize() -> (int, int):
    window.update()
    width = window.winfo_width()
    height = window.winfo_height()
    return (width, height)


if __name__ == '__main__':
    window = Tk()
    window.title("Result")

    # sticky == alignment(stick or fill)
    # column/rowconfigure(column/row_index, weight, minsize, pad(=padding))
    # weight == 0 means fixed, weight > 0 means expandable, each weight is a ratio with other widget's weight
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    mainframe = ttk.Frame(window, padding=50)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) # fill its parent    
    mainframe.columnconfigure(0, weight=1) # setting inner grid

    # placeholder image for map area
    map_placeholder = ImageTk.PhotoImage(Image.open('image_placeholder.png'))
    map = ttk.Label(mainframe, image=map_placeholder)
    map.grid(column=0, row=0, sticky=N)
    mainframe.rowconfigure(0, weight=0)

    questionLabel = ttk.Label(mainframe)
    questionLabel.configure(text="지금 어떤 종류의 음식을 원하시나요?")
    questionLabel.grid(column=0, row=0, sticky=[W, N])

    preference = {"중식", "일식", "한식", "간식", "휴식"}
    foodCategoryCheckButtons = checkButtonList(mainframe, preference)
    foodCategoryCheckButtons.grid(column=0, row=1, sticky=[W, N], pady=(10, 30))

    # give some placeholder item to the list
    item = ListItem(mainframe, "name", "distance", "time", 5)
    item.grid(column=0, row=1, sticky=[W, N])
    mainframe.rowconfigure(1, weight=0)

    map.grid_remove()
    item.grid_remove()

    buttomBar = ttk.Separator(mainframe, orient='horizontal')
    buttomBar.grid(column=0, row=2, sticky=[E, W])
    buttomBar.grid_remove()

    runButton = ttk.Button(mainframe)
    runButton.config(text="Run")
    runButton.config(command=mainButtonPressed)
    
    runButton.grid(column=0, row=3, sticky=[N, E, S, W])
    mainframe.rowconfigure(2, weight=0)
    mainframe.rowconfigure(3, weight=1)

    # TODO: define list's scrollbar, and present the list with scrollbar(replace item to list)
    # reference: 
    # https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
    # https://blog.teclado.com/tkinter-scrollable-frames/

    # set the window's size to fit the initial content
    (width, height) = currentWindowSize()
    window.minsize(width, height)

    window.mainloop()
