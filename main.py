import threading

from tkinter import ttk, Tk
from tkinter.constants import *
from PIL import ImageTk, Image

from surveyWidget import SurveySet
from loadingDialog import LoadingDialog
from scrollableWidget import ScrollableFrame
from restaurantItemWidget import ListItem
from LinearModel import RecommendationModel
from LinearModel import Extract_Numbers
from mapList import restaurant_list

import pandas as pd

from ttkthemes import ThemedTk

def DataInit(DF, Meat_pre, Noodle_pre, Rice_pre, FastFood_pre):
    Meat = ['닭발', '곱창,막창,양', '돼지고기구이', '스테이크,립', '정육식당', '육류,고기요리', '돈가스', '고기뷔페', '양식', '족발,보쌈', '소고기구이', '닭갈비', '치킨,닭강정', '만두', '닭요리',
            '육류,고기', '돈까스,우동', '해물,생선', '곱창,막창', '조개']
    Noodle = ['중식당', '국수', '아시아음식', '우동,소바', '샤브샤브', '돈까스,우동', '이탈리안', '중식', '베트남음식', '분식', '양식']
    Rice = ['죽', '한식', '보리밥', '국밥', '김밥', '감자탕', '한정식', '백반,가정식', '곰탕,설렁탕', '초밥,롤', '주먹밥']
    FastFood = ['햄버거', '베이커리', '피자', '카페', '카페,디저트', '디저트카페', '샌드위치', '분식', '패스트푸드']

    preference_dict = {
        'Meat': Meat,
        'Noodle': Noodle,
        'Rice': Rice,
        'FastFood': FastFood
    }

    DF['선호도'] = 3
    for category, preferences in preference_dict.items():
        DF.loc[DF['카테고리'].isin(preferences), '선호도'] = {
            'Meat': Meat_pre,
            'Noodle': Noodle_pre,
            'Rice': Rice_pre,
            'FastFood': FastFood_pre
        }[category]

    return DF

# TODO: convert to cancelable background task
def ML(survey, data: list):
    ''' 추가한 부분 '''
    
    # 합칠 때, UI에서 선호도 가져오면 됩니다.
    Meat_pre = survey.answers['고기&구이'].get()
    Noodle_pre = survey.answers['면'].get()
    Rice_pre = survey.answers['백반&죽'].get()
    FastFood_pre = survey.answers['패스트푸드'].get()

    TrainDF = pd.read_csv('train_data.csv', encoding = 'cp949')
    TrainDF = DataInit(TrainDF, Meat_pre, Noodle_pre, Rice_pre, FastFood_pre)

    # 사용자의 음식 선호도에 맞게 TrianData를 학습시키기 위해서 추가하는 공식
    TrainDF['추천율'] = 0
    TrainDF['추천율'] = TrainDF['별점'].values * TrainDF['선호도'] + (TrainDF['별점 리뷰수'].values * 0.01) + (TrainDF['블로그 리뷰수'].values * 0.01)

    X = TrainDF[['별점', '선호도', '별점 리뷰수', '블로그 리뷰수']].values
    y = TrainDF['추천율'].values

    # 모델 생성
    model = RecommendationModel()
    model.train(X, y, epochs = 100)

    placesDF = restaurant_list()

    while(placesDF.empty):
        print("다시 리스트 가져오는 중..")
        placesDF = restaurant_list()


    placesDF = DataInit(placesDF, Meat_pre, Noodle_pre, Rice_pre, FastFood_pre)

    #print(placesDF)

    # '별점 리뷰수'와 '블로그 리뷰수'에서 숫자만 추출하여 업데이트
    placesDF['별점'] = placesDF['별점'].apply(Extract_Numbers)
    placesDF['별점 리뷰수'] = placesDF['별점 리뷰수'].apply(Extract_Numbers)
    placesDF['블로그 리뷰수'] = placesDF['블로그 리뷰수'].apply(Extract_Numbers)

    realX = placesDF[['별점', '선호도', '별점 리뷰수', '블로그 리뷰수']].values
    #print(placesDF)
    #print(realX)

    # 여기 X에는 실제 데이터가 들어가야합니다! (지금은 잘 나오나 원래 데이터로 돌려봤어요.)
    Predict_data = model.predict(realX)

    # 실제 데이터프레임(placesDF 말고)에서 '추천율' column을 생성한 후에 예측한 추천율을 넣어놓습니다.
    placesDF['추천율'] = 0
    placesDF['추천율'] = Predict_data

    # 추천율을 기준으로 정렬합니다. (추천율이 높은 순서대로 하기위해서 ascending = False를 사용했습니다.)
    data.append(placesDF.sort_values('추천율', ascending = False))
    ''' 끝 '''


def mainButtonPressed():
    # put some search result to `data`
    data = []

    bg_thread = threading.Thread(target=ML, args=(survey, data))
    bg_thread.start()

    dialog = LoadingDialog(window, data, title="Loading")

    # TODO: cancel background task
    if len(data) == 0:
        return

    displaySearchResult(data[0])

def displaySearchResult(data):
    # hide question label
    question_label.grid_remove()
    survey.grid_remove()

    # prevents displaying large window bigger than minsize
    width = map_placeholder.width()
    window.geometry(f"{width}x{width}")
    # this will re-enable auto-resizing by systems when widgets are restored 
    window.geometry("")

    # give some placeholder item to the list
    #item_count = 5
    for i, (name, address, time, rate) in enumerate(zip(data['이름'], data['주소'], data['영업시간'], data['별점'])):

        # ★☆ 별점 표시
        if(rate >= 5):
            rate = '별점 : ' + str(rate) + ' ★★★★★'
        elif(rate >= 4):
            rate = '별점 : ' + str(rate) + ' ★★★★☆'
        elif(rate >= 3):
            rate = '별점 : ' + str(rate) + ' ★★★☆☆'
        elif(rate >= 2):
            rate = '별점 : ' + str(rate) + ' ★★☆☆☆'
        elif(rate >= 1):
            rate = '별점 : ' + str(rate) + ' ★☆☆☆☆'
        elif(rate >= 0):
            rate = '별점 : ' + str(rate) + ' ☆☆☆☆☆'

        if(len(address) == 0):
            address = '주소 : 정보가 없습니다.'
        else:
            address = '주소 : ' + address

        if(len(time) == 0):
            time = '영업시간 : 정보가 없습니다.'
        else:
            time = '영업시간 : ' + time

        listitem = ListItem(listframe.scrollable_frame, name, address, time, rate)
        listitem.grid(column=0, row=i, sticky=[W, N])
        listframe.scrollable_frame.rowconfigure(i, weight=0)

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
    window =ThemedTk(theme = 'arc')
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

    # 배경색 바꾸는 Style + 적용
    style = ttk.Style()
    style.configure('TFrame', background='lightblue')
    mainframe.configure(style='TFrame')

    # placeholder image for map area
    map_placeholder = ImageTk.PhotoImage(Image.open('image_placeholder.png'))
    map = ttk.Label(mainframe, image=map_placeholder)
    map.grid(column=0, row=0, sticky=N)
    mainframe.rowconfigure(0, weight=0)
    map.configure(background='lightblue')

    listframe = ScrollableFrame(mainframe)
    listframe.grid(column=0, row=1, sticky=(N, W, E, S))
    mainframe.rowconfigure(1, weight=1)

    # # give some placeholder item to the list
    # item_count = 5
    # for i in range(item_count):
    #     listitem = ListItem(listframe.scrollable_frame, "name", "distance", "time", 5)
    #     listitem.grid(column=0, row=i, sticky=[W, N])
    #     listframe.scrollable_frame.rowconfigure(i, weight=0)

    buttomBar = ttk.Separator(mainframe, orient='horizontal')
    buttomBar.grid(column=0, row=2, sticky=[E, W])
    mainframe.rowconfigure(2, weight=4)

    map.grid_remove()
    listframe.grid_remove()
    buttomBar.grid_remove()

    question_text = "어떤 음식을 선호하시나요?"
    question_label = ttk.Label(mainframe)
    question_label.configure(text=question_text)
    question_label.grid(column=0, row=0, sticky=[W, N])

    question_label.configure(background='lightblue', foreground='black', font=("Malgun Gothic", 12, "normal"))

    score_kinds = ["싫어함", "별로", "그럭저럭", "좋아함", "땡김"]
    food_kinds = ["고기&구이", "면", "백반&죽", "패스트푸드"]
    survey = SurveySet(mainframe, score_names=score_kinds, subtitles=food_kinds)
    survey.grid(column=0, row=1, sticky=(N, W, E, S), pady=(20, 30))

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
