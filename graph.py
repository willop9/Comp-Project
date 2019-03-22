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
httpNodes = []
htmlToHtmlEdges = []
htmlToHttpEdges = []
bbcNodes = []
#Adding all page elements to node list
for child in soup.descendants:
    if(child.name is not None):
        G.add_node(child, type='HTML', tag='misc')
        HTMLNodes.append(child)

## Commented out for speed
#for child in soup2.descendants:
    #if(child.name is not None):
        #bbcNodes.append(child)

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
                                htmlToHtmlEdges.append([n,m])

G.add_edges_from(htmlToHtmlEdges)
print(G.number_of_edges())

for n in soup.find_all(src=True):
        src = n['src']
        print(n)
        G.add_node(src, type='HTTP')
        httpNodes.append(src)
        htmlToHttpEdges.append([n,src])

G.add_edges_from(htmlToHttpEdges)

print(G.number_of_nodes())#19?????
#drawing graph fingers crossed
pos = nx.spring_layout(G)
plt.subplot(111)
nx.draw_networkx_nodes(G,pos,
                       nodelist=HTMLNodes,
                       node_color='r',
                       node_size=500,
                   alpha=1)
nx.draw_networkx_edges(G,pos,
                       edgelist=htmlToHtmlEdges,
                       width=3,alpha=0.8,edge_color='black')
nx.draw_networkx_nodes(G,pos,
                       nodelist=httpNodes,
                       node_color='b',
                       node_size=250,
                   alpha=1)
nx.draw_networkx_edges(G,pos,
                       edgelist=htmlToHttpEdges,
                       width=3,alpha=0.8,edge_color='green')
        
plt.show()
#Things to do next:
#Create an array of http nodes where a src attribute points to a url
#add nodes to the graph, represent nodes with different colours
#add edges to nodes with their corresponding html node

#Method:
#Beautifulsoup findall('src') and add that to http array
#Code I have lost:
#Adding atributes to my nodes
#Add edges not by adding them to a list but individually as well
#Add nodes independantly and give them atrribute of misc
#find all img, style, and iframe nodes and give them attributes