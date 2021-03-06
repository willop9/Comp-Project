import urllib.request
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import csv
test_url = "https://www.test.com"
url = "https://www.bristolpost.co.uk/"
G = nx.Graph(base_uri = url)
H = nx.DiGraph()

site = urllib.request.urlopen("file:./pages/bristolPost.html")#file:./docs/page.html  file:guardian.html

soup = BeautifulSoup(site, 'lxml')

HTMLNodes = []
httpNodes = []
htmlToHtmlEdges = []
htmlToHttpEdges = []
htmlToHttpIframe = []
bbcNodes = []

is_first_node_loaded = False
#Adding all page elements to node list
for child in soup.descendants:
    if(child.name is not None):
                G.add_node(child, type='HTML', domain=G.graph['base_uri'], ad=0)
                HTMLNodes.append(child)
                if(is_first_node_loaded):
                        G.add_edge(child, child.parent, type='htmlhtml')
                        htmlToHtmlEdges.append([child,child.parent])
                is_first_node_loaded = True

#adding tag attributes for different types of nodes
for n in soup.find_all('img'):
        G.nodes[n]['type']='HTML img'
for n in soup.find_all('style'):
        G.nodes[n]['type']='HTML style'
for n in soup.find_all('iframe'):
        G.nodes[n]['type']='HTML iframe'
for n in soup.find_all('div'):
        G.nodes[n]['type']='HTML div'
print(G.number_of_nodes()) #15 is the correct number! I am now getting 16 for some reason
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
        print(src)
        G.nodes[n]['domain'] = src
        G.add_node(src, type='HTTP source',domain=src, ad=0)
        httpNodes.append(src)
        htmlToHttpEdges.append([n,src])
        G.add_edge(n,src, type='htmlhttpsrc')

for n in soup.find_all(href=True):
        href = n['href']
        G.nodes[n]['domain'] = href
        G.add_node(href, type='HTTP href',domain=href, ad=0)
        httpNodes.append(href)
        htmlToHttpEdges.append([n,href])
        G.add_edge(n,href, type='htmlhttphref')
#Changing http iframes with src attribute
for n in soup.find_all('iframe'):
        try:
                src = n['src']
                G.nodes[src]['type'] = 'HTTP iframe'
                G.add_edge(n.parent,src, type='htmlhttpiframe')
                htmlToHttpIframe.append([n.parent,src])
        except:
                print('Could not add http node as iframe element does not have src attribute')
                G.nodes[n]['type'] = 'HTML iframe'

print(G.number_of_nodes())
nx.write_gexf(G,'./Graphs/bristolPost.gexf')
#Feature extraction
index = 0
a = np.zeros(shape=(G.number_of_nodes(), 9))
print(a)
#convert graph to a directed view
ad_words = ['ad', 'advert', 'advertisement', 'advertising', 'advertorial', 'banner','billboard','banner-ad','banner-advertisement','googleads', 'product', 'sponsor']
diG = G.to_directed()
#katz = nx.katz_centrality(G, alpha=0.1, beta=1.0, max_iter=10) Takes too long
#closeness = nx.closeness_centrality(G)
#eccentricity = nx.eccentricity(G)
clustering = nx.clustering(G)
print('clustering complete')
mdc=nx.average_neighbor_degree(G) #mean degree connectivity
print('mean degree connectivity complete')
graph_domain_split = G.graph['base_uri'].split('.',2)[1]
for n in list(G.nodes):
        row = []
        ad_count = 0
        #Find in degree
        row.append(diG.in_degree(n))
        #out degree
        row.append(diG.out_degree(n))
        #Descendants
        row.append(diG.in_degree(n) + diG.out_degree(n))
        #Katz Centrality
        #row.append(katz[n]) Takes too long on actual graphs even with reduced iteration number
        #closeness centrality
        #row.append(closeness[n])
        #mean degree connectivity
        row.append(mdc[n])
        #eccentricity
        #row.append(eccentricity[n])
        #Clustering
        row.append(clustering[n])
        #domain party
        if G.nodes[n]['domain'] == G.graph['base_uri']: #if the domain of the node is the same as the html doc then the value is 1.
                row.append(1)
        else:
                row.append(0)
        #sub domain
        #Check if the domain attribute of the node is a sub domain of the base uri attribute of the graph.
        node_dom = G.nodes[n]['domain']
        split = node_dom.split('.',2)[0]
        if split in {'http://www', 'https://www', 'www'}:
                split_node_dom = node_dom.split('.',2)[1]
        else:
                split_node_dom = node_dom.split('.',1)[0]
        if(split_node_dom == graph_domain_split):
                row.append(1)
        else:
                row.append(0)
        #node category
        node_type = G.nodes[n]['type']
        if node_type == 'HTML':
                row.append(0)
        elif node_type == 'HTML img':
                row.append(1)
        elif node_type == 'HTML style':
                row.append(2)
        elif node_type == 'HTML iframe':
                row.append(3)
        elif node_type == 'HTML div':
                row.append(4)
        elif node_type == 'HTTP source':
                row.append(5)
        elif node_type == 'HTTP iframe':
                row.append(6)
        elif node_type == 'HTTP href':
                row.append(7)

        #ad keywords
        try:    #Checking in the attributes  
                tag = n.attrs
                node_attributes = tag.values()
                for x in ad_words:
                        for y in node_attributes:
                                if x in y:
                                        for x in y:
                                                ad_count += 1
                #Check the text of a node as well if it exists
                if n.string is not None:
                        for x in ad_words:
                                if x in n.string:
                                        ad_count +=1
                row.append(ad_count)
        except: #try statement only fails when the node is a string as in HTTP node
                for x in ad_words:
                        if x in n:
                                ad_count += 1
                row.append(ad_count)
        print(row)   
        a[index][:] = row
        index += 1
        #print(a)
np.savetxt("./Features/brispost.csv", a, delimiter=",")
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