from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from styleframe import StyleFrame
import datetime


class exercise():
    def __init__(self):
        self.date = ""
        self.day = ""
        self.time = ""
        self.number = ""
        self.location = ""
        self.subject = ""
        self.type = ""
        self.format = ""
        self.group = ""
        self.teacher = ""

    def __str__(self):
        return f'{self.location}\n{self.time} {self.type}\n{self.subject}'


people_file = open('people.txt', 'r')
people_text = people_file.read()
people = ['Литвинов Марк Николаевич'] + sorted(people_text.split('\n\n'))
weekly_keys = ['Имя', 'пн1', 'пн2', 'пн3', 'пн4', 'пн5', 'пн6', 'пн7', 'вт1', 'вт2', 'вт3', 'вт4', 'вт5', 'вт6', 'вт7',
               'ср1',
               'ср2', 'ср3', 'ср4', 'ср5', 'ср6', 'ср7', 'чт1', 'чт2', 'чт3',
               'чт4', 'чт5', 'чт6', 'чт7', 'пт1', 'пт2', 'пт3', 'пт4', 'пт5', 'пт6', 'пт7', 'сб1', 'сб2', 'сб3', 'сб4',
               'сб5', 'сб6', 'сб7', 'вс1', 'вс2', 'вс3', 'вс4', 'вс5', 'вс6', 'вс7']

PATH = '/Users/marklitvinov/Documents/GitHub/hse_timetable/chromedriver'
option = webdriver.ChromeOptions()
option.add_argument("-incognito")

driver = webdriver.Chrome(PATH, options=option)
driver.get('https://ruz.hse.ru/ruz/main')
arr = []  # weekly timetable
sleep(3)

for person in people:

    week = []
    xbutt = driver.find_elements_by_xpath("//button[@class='btn btn-outline-danger mt-3 clear-filter']")[0].click()
    driver.find_element(By.XPATH, '//button[text()=" Студент "]').click()
    personname = driver.find_elements_by_id("autocomplete-student")[0]
    personname.send_keys(person)
    sleep(1)
    personname.send_keys(Keys.ENTER)
    sleep(1)
    driver.find_element(By.XPATH, '//button[text()=" Список "]').click()
    sleep(2)

    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')

    lessons = soup.find_all('div', class_='media day ng-star-inserted')

    # lets add every пара to weekly timetable of the student

    for i in range(len(lessons)):

        soup = BeautifulSoup(str(lessons[i]), 'lxml')
        ex = exercise()
        try:
            ex.date = soup.find_all('div', class_='day')[0].get_text() + " " + \
                      soup.find_all('div', class_='month')[0].get_text()  # the day_month
            ex.day = soup.find_all('div', class_='week')[0].get_text()  # day of the week
            ex.type = soup.find_all('div', class_='text-muted kind ng-star-inserted')[0].get_text()
        except IndexError:
            try:
                ex.date = week[-1].date  # the day_month
                ex.day = week[-1].day  # day of the week
            except IndexError:
                continue
        try:
            ex.time = soup.find_all('div', class_='time')[0].get_text()  # time
            ex.number = soup.find_all('small')[0].get_text()
            ex.location = soup.find_all('span', class_='auditorium')[0].get_text() + " " + \
                          soup.find_all('span', class_='mr-2 text-muted ng-star-inserted')[0].get_text()
            ex.subject = soup.find_all('span', class_='ng-star-inserted')[0].get_text()
            ex.group = soup.find_all('div', class_='group ng-star-inserted')[0].get_text()
            ex.teacher = soup.find_all('div', class_='lecturer')[0].get_text()
        except IndexError:
            pass

        week.append(ex)

    # lets add every ex from weekly timetable to week_dict

    week_dict = dict(zip(weekly_keys, [''] * len(weekly_keys)))

    for elem in week:
        week_dict[elem.day + elem.number[0]] = str(elem)
    week_dict['Имя'] = person

    arr.append(week_dict)

df = pd.DataFrame(arr)

my_date = datetime.date.today()
year, week_num, day_of_week = my_date.isocalendar()

excel_writer = StyleFrame.ExcelWriter(f'results/{week_num}.xlsx')
sf = StyleFrame(df)
sf.set_column_width(columns=weekly_keys, width=45)

sf.to_excel(
    excel_writer=excel_writer,
    header=f'Week №{week_num}',
    sheet_name='Timetable'
)
excel_writer.save()

df = pd.DataFrame(arr)

my_date = datetime.date.today()
year, week_num, day_of_week = my_date.isocalendar()

excel_writer = StyleFrame.ExcelWriter(f'results/{week_num}.xlsx')
sf = StyleFrame(df)
sf.set_column_width(columns=weekly_keys, width=45)

sf.to_excel(
    excel_writer=excel_writer,
    header=f'Week №{week_num}',
    sheet_name='Timetable'
)
excel_writer.save()

sleep(3)
driver.close()
