from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #selenium에서 사용할 모듈 import

import time
import requests
from bs4 import BeautifulSoup
import re
import csv

import tkinter as tk
import pandas as pd
import numpy as np

def get_RestaurantList():
    
    # 위치가져오는건데 함수 return값으로? 받는걸로 고쳐야할듯
    url = 'https://search.naver.com/search.naver?query=날씨'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    
    # 위치
    #위치 주소에 대한 html값을 찾아서 Address에 넣음
    Address = soup.find('div', {'class': 'title_area _area_panel'}).find('h2', {'class': 'title'}).text
    '''
    url = f'https://map.naver.com/v5/search/{Address}+맛집'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    
    frame = soup.find('iframe', id="searchIframe")
    frame_url = frame["src"]
    
    '''
    
    url = f"https://pcmap.place.naver.com/restaurant/list?query={Address}+맛집"
    iframe = requests.get(url)
    #iframe = requests.get("https://pcmap.place.naver.com/restaurant/list?query=%EB%B6%84%EB%8B%B9%EA%B5%AC%20%EC%A0%95%EC%9E%90%EB%8F%99+%EB%A7%9B%EC%A7%91")
    iframe_soup = BeautifulSoup(iframe.content.decode('utf-8', 'replace'), 'html.parser')
    
    Restaurant = iframe_soup.find_all('span', {'class': 'place_bluelink TYaxT'})
    #Address_restaurant = soup.find_all('span', {'class': 'Pb4bU'})


    #RestaurantType = soup.find_all('span', {'class': 'KCMnt'})
    #RestaurantOpen = soup.find_all('span', {'class': 'h69bs KvAhC utj_r'})
    #RestaurantReview = soup.find_all('span', {'class': 'place_blind'})

    # for i in Restaurant:
    #     text_widget.insert(i.text + "\n")


    # 아마 Restaurant가 List가 아닌듯함,, 그래서 바꾸는 과정?
    List = []
    for i in Restaurant:
        List.append(i.text)
        
    f = open('naver_map.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(List)
    f.close()
    
    # 라벨 2에 출력
    #label_2.config(text=f"음식점 리스트\n\n{List[0]}\n{List[1]}\n{List[2]}\n{List[3]}\n{List[4]}\n{List[5]}\n{List[6]}\n{List[7]}\n{List[8]}\n{List[9]}", font = ("Helvetica", 20))
    
get_RestaurantList()