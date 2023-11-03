from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from typing import List, Dict

class SurveySet(ttk.Frame):
    # creates a questionaire in tabular form, with given score names and subtitles
    def __init__(self, container, score_names: List[int], subtitles: List[str], *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        # instance members
        self.score_labels: [ttk.Label] = []
        self.radio_sets: List[RadioSet] = []
        self.answers: Dict[str, IntVar] = {}

        # set default value of answers, and initialize self.answers
        default_value = (len(score_names) - 1) // 2
        for subtitle in subtitles:
            self.answers[subtitle] = IntVar(self, value=default_value)

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
    def __init__(self, container, pos: (int, int), title: str, radio_count: int, variable: IntVar, *args, **kwargs):
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

# TODO: scrolling via mouse wheel
# TODO: auto hiding scrollbar when not needed
# TODO: set maximum size of the window to not exceed the screen size 
#       (max size is only updated when the content is changed)
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # <Configure> event
        # triggered whenever its size, position, or border width changes, and sometimes when it has changed position in the stacking order.
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsw")
        self.scrollbar.grid(row=0, column=1, sticky="ens")
    
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

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
    for key, value in survey.answers.items():
        print(key, value.get(), sep=": ")


def displaySearchResult(data):
    # hide question label
    question_label.grid_remove()
    survey.grid_remove()

    # prevents displaying large window bigger than minsize
    width = map_placeholder.width()
    window.geometry(f"{width}x{width}")
    # this will re-enable auto-resizing by systems when widgets are restored 
    window.geometry("") 

    # restore searched result UI layout
    mainframe.configure(padding=5)
    map.grid()
    listframe.grid()
    mainframe.rowconfigure(1, weight=1)
    
    buttomBar.grid()
    mainframe.rowconfigure(2, weight=0)
    
    # change some layout configuration of runButton
    runButton.grid(sticky=S)
    mainframe.rowconfigure(3, weight=0)

    # set the window's size to fit the initial content
    (width, height) = currentWindowSize()
    window.minsize(width, height)
    window.maxsize(int(width * 1.5), height * 2)


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

    listframe = ScrollableFrame(mainframe)
    listframe.grid(column=0, row=1, sticky=(N, W, E, S))
    mainframe.rowconfigure(1, weight=1)

    # give some placeholder item to the list
    for i in range(10):
        listitem = ListItem(listframe.scrollable_frame, "name", "distance", "time", 5)
        listitem.grid(column=0, row=i, sticky=[W, N])
        listframe.scrollable_frame.rowconfigure(i, weight=0)

    buttomBar = ttk.Separator(mainframe, orient='horizontal')
    buttomBar.grid(column=0, row=2, sticky=[E, W])
    mainframe.rowconfigure(2, weight=4)

    map.grid_remove()
    listframe.grid_remove()
    buttomBar.grid_remove()

    question_text = "각 음식 종류별 선호도를 알려주세요."
    question_label = ttk.Label(mainframe)
    question_label.configure(text=question_text)
    question_label.grid(column=0, row=0, sticky=[W, N])

    score_kinds = ["싫어함", "별로", "그럭저럭", "좋아함", "땡김"]
    food_kinds = ["중식", "일식", "한식", "디저트"]
    survey = SurveySet(mainframe, score_names=score_kinds, subtitles=food_kinds)
    survey.grid(column=0, row=1, sticky=(N, W, E, S), pady=(10, 30))

    runButton = ttk.Button(mainframe)
    runButton.config(text="Run")
    runButton.config(command=mainButtonPressed)
    
    runButton.grid(column=0, row=3, sticky=[N, E, S, W])
    mainframe.rowconfigure(3, weight=2)

    # set the window's size to fit the initial content
    (width, height) = currentWindowSize()
    window.minsize(width, height)

    window.mainloop()
