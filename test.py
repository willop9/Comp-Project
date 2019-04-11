from bs4 import BeautifulSoup
import urllib.request
import numpy as np

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