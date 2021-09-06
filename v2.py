from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class exercise():
    def __init__(self, date, day, time, number, location, subject, type, format, group, lecture):
        self.date = ""
        self.day = ""
        self.time = ""
        self.number = ""
        self.location = ""
        self.subject = ""
        self.type = ""
        self.format = ""
        self.group = ""
        self.lecture = ""


PATH = '/Users/marklitvinov/Documents/GitHub/hse_timetable/chromedriver'
option = webdriver.ChromeOptions()
option.add_argument("-incognito")

driver = webdriver.Chrome(PATH, options=option)

#while True:

driver.get('https://ruz.hse.ru/ruz/main')
sleep(1)
driver.find_element(By.XPATH, '//button[text()=" Студент "]').click()
driver.find_elements_by_id("autocomplete-student")[0].click()
personname = driver.find_elements_by_id("autocomplete-student")[0]
personname.send_keys('Кокова Полина Дмитриевна')
sleep(1)
personname.send_keys(Keys.ENTER)
sleep(3)

source = driver.page_source
soup = BeautifulSoup(source, 'lxml')

lessons = soup.find_all('div', class_='media-body')
#print(lessons[0]
for lesson in lessons:
    tmp = BeautifulSoup(lesson, 'lxml')
    

sleep(10)

#driver.close()
