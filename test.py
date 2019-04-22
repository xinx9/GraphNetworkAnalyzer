import sys
import networkx as nx
import matplotlib.pyplot as plt
import random, string
import community
from community import community_louvain
from networkx.algorithms.community import *

def avgdegree(graph):
    degrees = graph.degree()
    avgdeg = 0.0
    for degree in degrees:
        avgdeg += degree[1]
    avgdeg /= len(degrees)
    return avgdeg

def highestdeg(graph):
    hdeg = sorted(graph.degree, key=lambda x: x[1], reverse=True)
    return hdeg[0][1]

def highestClosenessCentrality(graph):
    rcc = nx.closeness_centrality(graph)
    cc = list(rcc.values())
    hcc = sorted(cc, reverse=True)
    return hcc[0]

def highestBetweenessCentrality(graph):
    rbc = nx.betweenness_centrality(graph)
    bc = list(rbc.values())
    hbc = sorted(bc, reverse=True)
    return hbc[0]

def dataout(graph, name):
    fout = open(name + "_stats.txt", "w+")
    diameter = str(nx.diameter(graph))
    cc = str(nx.average_clustering(graph))
    avgdeg = str(avgdegree(graph))
    highdeg = str(highestdeg(graph))
    highcc = str(highestClosenessCentrality(graph))
    highbc = str(highestBetweenessCentrality(graph))
    clustersize = str(len(louvainModClustering(graph, name)))
    fout.write(name + "\nAverage Degree: " + avgdeg + "\nHighest Node Degree: " + highdeg + "\nHighest Closeness Centrality Node: " +  highcc  + "\nHighest Betweenness Centrality Node: " + highbc + "\nDiameter: " + diameter + "\nClustering Coefficient: " + cc + "\nLouvain Modularity Cluster Size: " + clustersize)
    fout.close()

def printNetwork(graph, name):
    options = { 'width':.09,'node_size':2, 'with_labels':False} 
    nx.draw_networkx(graph, **options)
    plt.savefig(name + "_Graph.png", dpi=800, bbox_inches='tight', format="PNG")

def degdist(graph, name):
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    plt.loglog(degree_sequence,'b-',marker='o')
    plt.title(name + " Degree rank plot")
    plt.ylabel("Degree")
    plt.xlabel("rank")
    plt.axes([0.45,0.45,0.45,0.45])
    plt.axis('off')
    filename = name + "_degree_histogram.png" 
    plt.savefig(filename)
    plt.clf()
 
def bcdist(graph, name):
    rbc = nx.betweenness_centrality(graph)
    bc = list(rbc.values())
    hbc = sorted(bc, reverse=True)
    plt.loglog(hbc,'b-',marker='o')
    plt.title(name + " Betweeness Centrality rank plot")
    plt.ylabel("Betweeness Centrality")
    plt.xlabel("rank")
    plt.axes([0.45,0.45,0.45,0.45])
    plt.axis('off')
    filename = name + "_bc_histogram.png" 
    plt.savefig(filename)
    plt.clf()

def louvainModClustering(graph, name):
    louvain = community_louvain.best_partition(graph)
    mod = community.modularity(louvain,graph)
    filename = name + "_Louvain_Modularity_cluster"
    fin = open(filename + "_louvain_modularity_data", "w+")
    for key ,value in louvain.items():
        lmdata= str(key)+ ":" + str(value)
        fin.write(lmdata + "\n")
    fin.close()
    values = [louvain.get(node) for node in graph.nodes()]
    uniqueval = list(dict.fromkeys(values))
    nx.draw_spring(graph, cmap=plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
    plt.savefig(filename)
    plt.clf()
    return uniqueval

if(len(sys.argv) != 2):
    print("Usage: python test.py <file name,er, or ba>")
    sys.exit(1)

if(sys.argv[1] == "er"):
    er = nx.erdos_renyi_graph(500, .02)
    dataout(er,"ER")
    printNetwork(er, "ER")
    degdist(er,"ER")
    bcdist(er,"ER")
elif(sys.argv[1] == "ba"):
    ba = nx.barabasi_albert_graph(500, 5)
    dataout(ba,"BA")
    printNetwork(ba, "BA")
    degdist(ba, "BA")
    bcdist(ba, "BA")
else:
    f = open(sys.argv[1],"r")
    x = f.read()
    y = x.split()
    filename = sys.argv[1].split(".")[0]
    G = nx.Graph()
    i = 0
    while(i != len(y)):
        if( i % 2 == 0):
            G.add_node(int(y[i]))
        else:
            G.add_edge(int(y[i-1]), int(y[i]))
        i+=1
    dataout(G,filename)
    printNetwork(G, filename)
    degdist(G,filename)
    bcdist(G,filename)
