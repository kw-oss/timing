from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW
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

def restaurant_list():
    
    #csv파일에서 1행에 어떤 내용인지 기재
    f = open('kakaoMap.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(["이름", "별점", "주소", "영업시간", "카테고리", "별점 리뷰수", "블로그 리뷰수"])
    f.close()
    
    
    
    #위치
    #위치 주소에 대한 html값을 찾아서 Address에 넣음
    url = 'https://search.naver.com/search.naver?query=날씨'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    #myAddress = soup.find('div', {'class': 'title_area _area_panel'}).find('h2', {'class': 'title'}).text
    
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent = {user_agent}")
    option = options.add_argument("headless")
    options.add_argument("disable-gpu")
    
    myAddress = "노원구 광운로"
    url = f'https://map.kakao.com/?q={myAddress}+맛집'
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    
    #식당 정보 얻어오는 코드
    restaurant = driver.find_elements(By.CLASS_NAME, 'link_name')
    star = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[4]/span[1]/em')
    address = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[5]/div[2]/p[1]')
    time = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[5]/div[3]/p/a')
    type = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[3]/span')
    starReview = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[4]/span[1]/a')
    blogReview = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[4]/a/em')


    size = len(restaurant)
    print(size)
    
    #배열을 만들고 얻어온 내용을 대입
    f = open('kakaoMap.csv', 'a', newline='')
    writer = csv.writer(f)
    #foodList = []
    for i in range(size):
        
        writer.writerow([restaurant[i].text, star[i].text, address[i].text, time[i].text, type[i].text, starReview[i].text, blogReview[i].text])
        foodList.append([restaurant[i].text, star[i].text, address[i].text, time[i].text, type[i].text, starReview[i].text, blogReview[i].text])
    
    f.close()
    driver.close()

foodList = []
restaurant_list()
print(foodList[1])
