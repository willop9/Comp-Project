import urllib.request
import html2text
from bs4 import BeautifulSoup
url='https://www.theguardian.com/uk'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'lxml')
name = 'guardian'
#soup.prettify()
with open('./docs/' + name + '.html', "w") as file:
    file.write(str(soup))