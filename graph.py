import urllib.request
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

url = "https://www.theguardian.com/uk"
G = nx.Graph(base_uri = url)
H = nx.DiGraph()

site = urllib.request.urlopen("file:./docs/page.html")#file:./docs/page.html  file:guardian.html
bbc = urllib.request.urlopen("https://www.bbc.co.uk")

soup = BeautifulSoup(site, 'lxml')
soup2 = BeautifulSoup(bbc, 'lxml')

HTMLNodes = []
httpNodes = []
htmlToHtmlEdges = []
htmlToHttpEdges = []
htmlToHttpIframe = []
bbcNodes = []
#Adding all page elements to node list
for child in soup.descendants:
    if(child.name is not None):
        G.add_node(child, type='HTML', tag='misc', ad=0)
        HTMLNodes.append(child)
        if(child.parent is not None):
                G.add_edge(child, child.parent)
                htmlToHtmlEdges.append([child,child.parent])
#adding tag attributes for different types of nodes
for n in soup.find_all('img'):
        G.nodes[n]['tag']='img'
for n in soup.find_all('style'):
        G.nodes[n]['tag']='style'
for n in soup.find_all('iframe'):
        G.nodes[n]['tag']='iframe'
for n in soup.find_all('div'):
        G.nodes[n]['tag']='div'


print(G.number_of_nodes()) #15 is the correct number!
print(H.number_of_nodes()) #1344

#Attempting to create edges
#For all the nodes create list of children
#for n in list(G.nodes):
 #       children = n.contents
        #Cycle through node list again
  #      for m in list(G.nodes):
                #cyclce through child list and check if any of the children of the current node are equal to any other node. If so append to edges list
   #             for x in children:
    #                    if(m == x):
     #                           htmlToHtmlEdges.append([n,m])
      #                          G.add_edge(n,m)

print(G.number_of_edges())
#Adding HTTP layer
for n in soup.find_all(src=True):
        src = n['src']
        print(n)
        G.add_node(src, type='HTTP source', ad=0)
        httpNodes.append(src)
        htmlToHttpEdges.append([n,src])
        G.add_edge(n,src)
#Changing iframes with src attribute
for n in soup.find_all('iframe'):
        try:
                src = n['src']
                G.nodes[src]['type'] = 'HTTP iframe'
                G.add_edge(n.parent,src)
                htmlToHttpIframe.append([n.parent,src])
        except:
                print('Could not add http node as iframe element does not have src attribute')

print(G.number_of_nodes())
#Feature extraction
index = 0
a = np.zeros(shape=(G.number_of_nodes(), 11))
print(a)
for n in list(G.nodes):
        row = []
        #convert graph to a directed view
        diG = G.to_directed()
        #Find in degree
        row.append(diG.in_degree(n))
        #out degree
        row.append(diG.out_degree(n))
        #Descendants
        row.append(diG.in_degree(n) + diG.out_degree(n))
        print(row)

#drawing graph fingers crossed
pos = nx.spring_layout(G)
plt.subplot(111)
nx.draw_networkx_nodes(G,pos,
                       nodelist=HTMLNodes,
                       node_color='r',
                       node_size=150,
                       alpha=1)
nx.draw_networkx_edges(G,pos,
                       edgelist=htmlToHtmlEdges,
                       width=3,alpha=0.8,edge_color='black')
nx.draw_networkx_nodes(G,pos,
                       nodelist=httpNodes,
                       node_color='b',
                       node_size=150,
                       alpha=1)
nx.draw_networkx_edges(G,pos,
                      edgelist=htmlToHttpEdges,
                      width=3,alpha=0.8,edge_color='green')
nx.draw_networkx_edges(G,pos,
                       edgelist=htmlToHttpIframe,
                       width=3,alpha=0.8,edge_color='blue')

plt.axis('off')     
plt.show()
#Things to do next:
#label nodes for the guardian as ad or non ad
#What is the best way to do this