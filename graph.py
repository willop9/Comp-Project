import urllib.request
from bs4 import BeautifulSoup
import networkx as nx

G = nx.Graph()
site = urllib.request.urlopen("file:./docs/page.html")
soup = BeautifulSoup(site, 'lxml')

for child in soup.descendants:
    if(child.name is not None):
        print(child)