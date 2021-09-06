import requests
from bs4 import BeautifulSoup

url = 'https://ruz.hse.ru/ruz/main' # url страницы
#headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4630.2 Safari/537.36"}
r = requests.get(url)
r.encoding = 'utf-8'

with open('html/test.html', 'w') as file:
    file.write(r.text)
