import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
driver = webdriver.Firefox()
url='https://www.theguardian.com/uk'
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
name = 'guardian'
#soup.prettify()
with open(name + '.html', "w") as file:
    file.write(str(soup))