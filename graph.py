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

soupNodes = []
edges = []
bbcNodes = []

#Adding all page elements to node list
for child in soup.descendants:
    if(child.name is not None):
        soupNodes.append(child)

for child in soup2.descendants:
    if(child.name is not None):
        bbcNodes.append(child)
#Adding nodes to Graph
G.add_nodes_from(soupNodes)
H.add_nodes_from(bbcNodes)

print(G.number_of_nodes()) #15 is the correct number!
print(H.number_of_nodes()) #1344

#Attempting to create edges
edges = []
#For all the nodes create list of children
for n in list(G.nodes):
        children = n.contents
        #Cycle through node list again not accounting for current node currently
        for m in list(G.nodes):
                #cyclce through child list and check if any of the children of the current node are equal to any other node. If so append to edges list
                for x in children:
                        if(m == x):
                                edges.append([n,m])

#print("Printing Edges")
#for x in edges:
       # print('/////////////////////////')
        #print(x)
        #print('#########################')

G.add_edges_from(edges)
print(G.number_of_edges())

#drawing graph fingers crossed
plt.subplot(111)
nx.draw(G)
plt.show()
#Things to do next:
#create edge rules. Edges between parents and children
#G.add_edges_from([(1,2)],[(1,3)]) Example for adding numerical edges. Edges can be added between nodes
#Nodes in the graph still work as bs4 tag objects. Iterate through g.nodes and create an edge if any of the other nodes a direct child
#.parent attribute shows a tags parents. .contents shows a list of a tags direct children