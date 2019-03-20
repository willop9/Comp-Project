import urllib.request
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
H = nx.Graph()

site = urllib.request.urlopen("file:./docs/page.html")
bbc = urllib.request.urlopen("https://www.bbc.co.uk")

soup = BeautifulSoup(site, 'lxml')
soup2 = BeautifulSoup(bbc, 'lxml')

HTMLNodes = []
edges = []
bbcNodes = []
#Adding all page elements to node list
for child in soup.descendants:
    if(child.name is not None):
        G.add_node(child, type='HTML')

## Commented out for speed
#for child in soup2.descendants:
    #if(child.name is not None):
        #bbcNodes.append(child)

#Adding nodes to Graph
#G.add_nodes_from(HTMLNodes)
H.add_nodes_from(bbcNodes)

print(G.number_of_nodes()) #15 is the correct number!
print(H.number_of_nodes()) #1344

#Attempting to create edges
#For all the nodes create list of children
for n in list(G.nodes):
        children = n.contents
        #Cycle through node list again
        for m in list(G.nodes):
                #cyclce through child list and check if any of the children of the current node are equal to any other node. If so append to edges list
                for x in children:
                        if(m == x):
                                edges.append([n,m])

G.add_edges_from(edges)
print(G.number_of_edges())

httpNodes = soup.find_all(src=True)
for n in httpNodes:
        src = n['src']
        print(n)
        G.add_node(src, type='HTTP')

print(G.number_of_nodes())#19?????
#drawing graph fingers crossed
plt.subplot(111)
nx.draw(G)
plt.show()
#Things to do next:
#Create an array of http nodes where a src attribute points to a url
#add nodes to the graph, represent nodes with different colours
#add edges to nodes with their corresponding html node

#Method:
#Beautifulsoup findall('src') and add that to http array