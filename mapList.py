from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

def time_wait(num, code):
        try:
            wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
        except:
            print(code, '태그를 찾지 못하였습니다.')
            driver.quit()
        return wait

driver = webdriver.Chrome()
driver.set_window_size(1024, 1000)

# 네이버 지도 접속
driver.get('https://map.naver.com/v5/search')
    
time_wait(3, 'div.input_box > input.input_search')

search_box = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
search_box.send_keys('노원구 월계동 피자')
search_box.send_keys(Keys.ENTER)  # 엔터버튼 누르기

sleep(10)