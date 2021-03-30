from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException

from urllib.request import urlopen
import json
import time
import os
import argparse

parser = argparse.ArgumentParser(description='Crawling')
parser.add_argument('--list', type=str, help='food list txt files')
parser.add_argument('--item', type=str, default='', help='food one item name')
parser.add_argument('--name', type=str, default='new_data', help='Image Folder Name')

opt = parser.parse_args()

def get_food_list():
    if opt.list:
        with open(opt.list, 'r', encoding='UTF8') as f:
            lines = f.read().splitlines()
            food_list_en = [name.strip() for name in lines[0].split(',')]
            food_list_kr = [name.strip() for name in lines[1].split(',')]

    else:
        item_en_kr = opt.item.split(',')
        food_list_en = [item_en_kr[0].strip()]
        food_list_kr = [item_en_kr[1].strip()]

    return food_list_en, food_list_kr

def check_dir(filename):
    original = filename
    file_order = 1
    
    while True:
        if os.path.isdir(filename):
            new_name = original + str(file_order)
            filename = new_name
            file_order += 1
        else:
            os.makedirs(filename)
            break

def crawling():
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(desired_capabilities=caps,options=options)
    base_url = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query='
    
    food_list_en, food_list_kr = get_food_list()
    print('아래의 음식 사진을 수집합니다.')
    print(food_list_kr)

    check_dir(opt.name)

    image_total = 0
    for food_en, food_kr in zip(food_list_en, food_list_kr):
        print('-----------------------', food_kr + '  시작------------------')
        driver.get(base_url + food_kr)

        delay = 10
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'main_pack')))
            print("페이지 로딩 완료")
        except TimeoutException:
            print("페이지 로딩 실패")
            break

        list_len_for_scroll = 0
        while True:
            driver.find_element_by_tag_name('html').send_keys(Keys.END)
            time.sleep(0.7)
            driver.find_element_by_class_name('photo_tile')
            url_list_for_scroll = driver.find_elements_by_class_name('_image')
            
            
            if len(url_list_for_scroll) == list_len_for_scroll:
                driver.find_element_by_tag_name('html').send_keys(Keys.HOME)
                y = 1000
                for timer in range(0,50):
                    driver.execute_script("window.scrollTo(0, "+str(y)+")")
                    y += 1000  
                    time.sleep(0.1)
                break
            list_len_for_scroll = len(url_list_for_scroll)

        driver_log = driver.get_log('performance')
        image_url_list = []
        for i, log in enumerate(driver_log):
            if 'request' in json.loads(log['message'])['message']['params']:
                url = json.loads(log['message'])['message']['params']['request']['url']
                if 'https://search.pstatic.net/common/' in url:
                    image_url_list.append(url)

        count = 1
        os.makedirs('new_data\\' + food_en, exist_ok=True)
        for image_url in set(image_url_list):
            with urlopen(image_url) as f:
                with open('{}\{}\{}'.format('new_data', food_en, food_en) + str(count) + '.jpg', 'wb') as file_name:
                    img = f.read()
                    file_name.write(img)
            count += 1

        print(food_kr + ' 사진 개수 : {}개'.format(len(image_url_list)))
        print('-----------------------', food_kr + '  종료------------------')
        image_total += len(image_url_list)

    print('크롤링 끝')
    print('수집된 이미지의 총 개수는 {}개입니다.'.format(image_total))

if __name__ == '__main__':
    crawling()