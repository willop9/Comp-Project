import urllib.request
from bs4 import BeautifulSoup
import networkx as nx

G = nx.Graph()
H = nx.Graph()

site = urllib.request.urlopen("file:./docs/page.html")
bbc = urllib.request.urlopen("https://www.bbc.co.uk")

soup = BeautifulSoup(site, 'lxml')
soup2 = BeautifulSoup(bbc, 'lxml')

soupNodes = []
bbcNodes = []

for child in soup.descendants:
    if(child.name is not None):
        print(child.name)
        soupNodes.append(child)

for child in soup2.descendants:
    if(child.name is not None):
        bbcNodes.append(child)

G.add_nodes_from(soupNodes)
H.add_nodes_from(bbcNodes)

print(G.number_of_nodes()) #15 is the correct number!
print(H.number_of_nodes()) #1344

nodes = list(G.nodes)
for x in nodes:
    print('//////////////////////////')
    print(x)
    print('#########################')