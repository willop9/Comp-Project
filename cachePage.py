import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
driver = webdriver.Firefox()
url='https://www.bristol-sport.co.uk/'
driver.get(url)
time.sleep(10)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
name = 'bristolsport'
soup.prettify()
with open('./pages/'+ name + '.html', "w", encoding="utf-8") as file:
    file.write(str(soup))