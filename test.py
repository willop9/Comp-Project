from bs4 import BeautifulSoup
import urllib.request
import numpy as np

url = "https://www.theguardian.com/uk"
domain = url.split('.',2)
ad_words = ['ad', 'advert', 'advertisement', 'advertising', 'advertorial', 'banner','billboard','banner-ad','banner-advertisement','googleads']
test_string = 'banner advertisement'
count = 0
for n in ad_words:
    if n in test_string:
        count += 1
        print('This should print: ' + str(count))
print(domain)
site = urllib.request.urlopen("file:./docs/page.html")

soup = BeautifulSoup(site, 'lxml')
print("#######################")
array = soup.find_all(src=True)
print(array)
print("########################")
for n in array:
    src = n['src']
    print(src)
    print('////////////////////////')
    print(n)

a = np.array([1,2,3,4,5])
print("Printing array")
print(a)