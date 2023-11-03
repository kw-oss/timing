from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW
from bs4 import BeautifulSoup
import time
from time import sleep
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 크롬 창이 안 뜨도록 옵션 설정
#options = Options()
#options.add_argument('--headless')
#options.add_argument('--window-size=1024, 1000')
#service = ChromeService()
#service.creation_flags = CREATE_NO_WINDOW
#driver = webdriver.Chrome(service=service, options=options)

# 웹드라이버 경로 설정 및 브라우저 창 크기 설정
driver = webdriver.Chrome()
driver.set_window_size(1024, 1000)

# 네이버 지도 접속
driver.get('https://map.naver.com/v5/search')

# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait

def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    driver.switch_to.frame(frame)  # frame 변경
'''
    # 페이지 다운
def page_down(num):
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.click()
    for i in range(num):
        body.send_keys(Keys.PAGE_DOWN)
'''    
# css를 찾을때 까지 10초 대기
time_wait(3, 'div.input_box > input.input_search')

# 검색 카테고리 입력
search_box = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
search_box.send_keys('노원구 피자')
'''
# 검색 실행
search_button = driver.find_element_by_css_selector("button.spm")
search_button.click()

# 데이터 로딩 대기
time.sleep(3)

# BeautifulSoup 객체 생성
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 음식점 정보 추출
place_lists = soup.select('.placelist > .PlaceItem') 

# 데이터 저장을 위한 빈 리스트 생성
data = []

# 음식점 별 정보 출력
for place in place_lists:
    place_name = place.select('.head_item > .tit_name > .link_name')[0].text  # 음식점 이름
    place_address = place.select('.info_item > .addr > p')[0].text  # 음식점 주소
    place_score = place.select('.head_item > .tit_name > .evaluate > .num')[0].text  # 음식점 별점

    data.append([place_name, place_address, place_score])  # 데이터 추가

# 데이터프레임 생성
df = pd.DataFrame(data, columns=['이름', '주소', '별점'])

# CSV 파일로 저장
df.to_csv('naver_map_places.csv', encoding='utf-8-sig', index=False)

# 드라이버 종료
#driver.quit()
'''