from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #selenium에서 사용할 모듈 import

import requests
from bs4 import BeautifulSoup
import csv

import subprocess as sp # 쉘 명령어를 실행하기 위한 모듈
import re # 정규표현식 사용
import json

import pandas as pd

def restaurant_list():
    
    # 정확도 조절 - 높은 값으로 설정할수록 속도가 빨라지나 정확도가 떨어짐
    accuracy = 1
    commd = 'add-type -assemblyname system.device; '\
            '$loc = new-object system.device.location.geocoordinatewatcher;'\
            '$loc.start(); '\
            'while(($loc.status -ne "Ready") -and ($loc.permission -ne "Denied")) '\
            '{start-sleep -milliseconds 100}; '\
            '$acc = %d; '\
            'while($loc.position.location.horizontalaccuracy -gt $acc) '\
            '{start-sleep -milliseconds 100; $acc = [math]::Round($acc*1.5)}; '\
            '$loc.position.location.latitude; '\
            '$loc.position.location.longitude; '\
            '$loc.position.location.horizontalaccuracy; '\
            '$loc.stop()' %(accuracy)

    pshellcomm = ['powershell', commd]

    # 쉘 명령어 실행 및 결과값 저장
    p = sp.Popen(pshellcomm, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.STDOUT, text=True)
    (out, err) = p.communicate()

    # 전체 출력 문자열에서 개행문자를 기준으로 분리 
    out = re.split('\n', out)

    lat = float(out[0])
    long = float(out[1])
    radius = int(out[2])

    # print(lat, long, radius)

    def lat_lon_to_addr(lon ,lat):
        url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={longitude}&y={latitude}'.format(longitude=lon,latitude=lat)
        headers = {"Authorization": "KakaoAK " + "82e74383a81e76a453aed30fac79cef2"}
        result = json.loads(str(requests.get(url, headers=headers).text))
        match_first = result['documents'][0]['address_name']
        return str(match_first)

    myAddress = lat_lon_to_addr(long,lat)
    
    options = Options()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())

    url = f'https://map.kakao.com/?q={myAddress}+맛집'
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    
    #식당 정보 얻어오는 코드
    restaurant = driver.find_elements(By.CLASS_NAME, 'link_name')
    star = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[4]/span[1]/em')
    address = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[5]/div[2]/p[1]')
    time = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[5]/div[3]/p/a')
    type = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[3]/span')
    starReview = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[4]/span[1]/a')
    blogReview = driver.find_elements(By.XPATH, '//*[@id="info.search.place.list"]/li/div[4]/a/em')


    # 데이터를 담을 리스트 초기화
    placesDF = {
        '이름': [],
        '별점': [],
        '주소': [],
        '영업시간': [],
        '카테고리': [],
        '별점 리뷰수': [],
        '블로그 리뷰수': [],
    }

    # 식당 정보를 리스트에 추가
    for i in range(len(restaurant)):
        placesDF['이름'].append(restaurant[i].text)
        placesDF['별점'].append(star[i].text)
        placesDF['주소'].append(address[i].text)
        placesDF['영업시간'].append(time[i].text)
        placesDF['카테고리'].append(type[i].text)
        placesDF['별점 리뷰수'].append(starReview[i].text)
        placesDF['블로그 리뷰수'].append(blogReview[i].text)

    # DataFrame 생성
    placesDF = pd.DataFrame(placesDF)

    driver.quit()

    return placesDF