from selenium import webdriver
import time
import pymysql

conn = pymysql.connect(host='vi-eco.cecgsm74tces.ap-northeast-2.rds.amazonaws.com', user='admin', password='1q2w3e4r', db='vi_eco', charset='utf8')


url='https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%A0%84%EA%B8%B0%EC%B0%A8'

chromedriver = 'D:/coding_test/chromedriver_win32/chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headlss chrome 옵션 적용
options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR')    # 언어 설정
driver = webdriver.Chrome(chromedriver, options=options)

driver.get(url)

allCarElement = driver.find_elements_by_css_selector("#_cs_car > div.info_sec > div.car_list > ul._list > li")

#print(allCarElement)
carnum=1
try:
    with conn.cursor() as curs:
        for item in allCarElement:
            CarName = item.find_element_by_tag_name("strong").text
            if (CarName != ''):
                print(CarName)
                ahref = item.find_element_by_tag_name("a").get_attribute("href")
                print(ahref)
                imgUrl = item.find_element_by_tag_name("img").get_attribute("src")
                print(imgUrl)
                CarPrice = item.find_element_by_class_name('car_price').text
                print(CarPrice)
                CarMileage = item.find_element_by_class_name('car_mileage').text
                print(CarMileage)
                sql = 'insert into car_information values(%s, %s, %s, %s, %s, %s)'
                curs.execute(sql, (carnum, CarName, '전기차', CarMileage, ahref, imgUrl))
            conn.commit()
            carnum+=1

        time.sleep(1)

        nextBtn = driver.find_element_by_css_selector("#_cs_car > div.info_sec > div._page.pg_nate > a._next._ready.nxt.on")
        pagenum=0
        isExistNextPage = nextBtn.is_enabled()

        while (pagenum<12):
            print("다음 페이지 존재함=======================================>")
            nextBtn.click()
            print(nextBtn)
            time.sleep(1)
            allCarElement = driver.find_elements_by_css_selector("#_cs_car > div.info_sec > div.car_list > ul._list > li")

            for item in allCarElement:
                CarName = item.find_element_by_tag_name("strong").text
                if (CarName != ''):
                    print(CarName)
                    ahref = item.find_element_by_tag_name("a").get_attribute("href")
                    print(ahref)
                    imgUrl = item.find_element_by_tag_name("img").get_attribute("src")
                    print(imgUrl)
                    CarPrice = item.find_element_by_class_name('car_price').text
                    print(CarPrice)
                    CarMileage = item.find_element_by_class_name('car_mileage').text
                    print(CarMileage)
                    sql = 'insert into car_information values(%s, %s, %s, %s, %s, %s)'
                    curs.execute(sql, (carnum, CarName, '전기차', CarMileage, ahref, imgUrl))
                conn.commit()
                carnum+=1

            isExistNextPage = nextBtn.is_enabled()
            print(isExistNextPage)
            pagenum+=1
finally:
    conn.close()