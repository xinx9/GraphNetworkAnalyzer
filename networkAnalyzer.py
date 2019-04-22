
import networkx as nx
import  matplotlib.pyplot as plt
import sys
f = open(sys.argv[1],"r")
x = f.read()
y = x.split()
# even numbers = node
# odd number = edge connections

if(len(sys.argv) != 2):
    print("Usage: python roadmap.py <road file>")
    sys.exit(1)

filename = sys.argv[1].split(".")[0]
filename += ".png"
G = nx.Graph()
i = 0
while(i != len(y)): #good luck
    if( i % 2 == 0):
        G.add_node(y[i])
    else:
        G.add_edge(y[i-1], y[i])
    i+=1
#Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
pos = nx.spring_layout(G, k=10)
options = { 'width':.09, 'font_size':2,'node_size':2, 'with_labels':False} 
nx.draw_networkx(G, pos, alpha=.7, **options)
plt.savefig(filename, dpi=1250, bbox_inches='tight', format="PNG")