from tkinter import ttk, Tk
from tkinter.constants import *
from PIL import ImageTk, Image

from survey import SurveySet
from loadingDialog import LoadingDialog
from scrollableWidget import ScrollableFrame
from restaurantItem import ListItem

def mainButtonPressed():
    # put some search result to `data`
    data = None

    # run the search algorithm here
    # TODO: run as background task(thread non-blocking)
    for key, value in survey.answers.items():
        print(key, value.get(), sep=": ")

    task_canceled = [False]
    dialog = LoadingDialog(window, task_canceled, title="Loading")
    
    if task_canceled[0]:
        return

    displaySearchResult(data)

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
    mainframe_padding = 5
    mainframe.configure(padding=mainframe_padding)
    map.grid()
    listframe.grid()
    mainframe.rowconfigure(1, weight=1)
    
    buttomBar.grid()
    mainframe.rowconfigure(2, weight=0)
    
    # change some layout configuration of runButton
    buttomArea.columnconfigure(1, weight=0)
    mainframe.rowconfigure(3, weight=0)

    # set window's minimum size
    min_height = map.winfo_reqheight() + listitem.winfo_reqheight() + buttomBar.winfo_reqheight() + buttomArea.winfo_reqheight() + mainframe_padding * 2
    min_width = map.winfo_reqwidth() + mainframe_padding * 2
    window.minsize(min_width, min_height)


def currentWindowSize() -> (int, int):
    window.update()
    width = window.winfo_width()
    height = window.winfo_height()
    return (width, height)


if __name__ == '__main__':
    window = Tk()
    window.title("Result")

    mainframe_padding = 50

    # sticky == alignment(stick or fill)
    # column/rowconfigure(column/row_index, weight, minsize, pad(=padding))
    # weight == 0 means fixed, weight > 0 means expandable, each weight is a ratio with other widget's weight
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    mainframe = ttk.Frame(window, padding=mainframe_padding)
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
    item_count = 5
    for i in range(item_count):
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
    food_kinds = ["고기&구이", "면", "백반&죽", "패스트푸드"]
    survey = SurveySet(mainframe, score_names=score_kinds, subtitles=food_kinds)
    survey.grid(column=0, row=1, sticky=(N, W, E, S), pady=(10, 30))

    # runButton wrapper for dynamic padding
    buttomArea = ttk.Frame(mainframe)
    buttomArea.grid(column=0, row=3, sticky=[N, E, S, W])
    buttomArea.columnconfigure(0, weight=2)
    buttomArea.columnconfigure(1, weight=1) # runButton column
    buttomArea.columnconfigure(2, weight=2)
    buttomArea.rowconfigure(0, weight=1)
    buttomArea.rowconfigure(1, weight=1) # runButton row
    buttomArea.rowconfigure(2, weight=2)

    mainframe.rowconfigure(3, weight=2)

    runButton = ttk.Button(buttomArea)
    runButton.config(text="맛집 찾기")
    runButton.config(command=mainButtonPressed)
    runButton.grid(column=1, row=1, sticky=[N, E, S, W])
    
    # set the window's size to fit the initial content
    (width, height) = currentWindowSize()
    window.minsize(width, height)

    window.mainloop()
