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
    url = 'https://search.naver.com/search.naver?query=날씨'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    
    #위치
    #위치 주소에 대한 html값을 찾아서 Address에 넣음
    #myAddress = soup.find('div', {'class': 'title_area _area_panel'}).find('h2', {'class': 'title'}).text
    
    myAddress = soup.find('div', {'class': 'title_area _area_panel'}).find('h2', {'class': 'title'}).text
    
    url = f'https://map.kakao.com/?q={myAddress}+치킨'
    driver = webdriver.Chrome()
    driver.get(url)
    
    restaurant = driver.find_elements(By.CLASS_NAME, 'link_name')
    star = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[4]/span[1]/em')
    address = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[5]/div[2]/p[1]')
    time = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[5]/div[3]/p/a')
    #print(star[1].text)
    #search_box.send_keys("노원구 광운로 피자")
    #search_box.send_keys(Keys.ENTER)
    
    size = len(restaurant)
    
    f = open('naver_map.csv', 'w', newline='')
    writer = csv.writer(f)
    #List = []
    for i in range(size):
        
        writer.writerow([restaurant[i].text, star[i].text, address[i].text, time[i].text])
        #List.append([restaurant[i].text, star[i].text])
        
    
    f.close()
    
restaurant_list()