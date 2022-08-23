from matplotlib import pyplot as plt
import numpy as np
import networkx as nx

# lines to 2d array
with open('myfile.txt') as f:
    a = np.array([list(map(int,i.split())) for i in f.readlines()])

# define grid graph according to the shape of a
G = nx.grid_2d_graph(*a.shape)


# remove those nodes where the corresponding value is != 0
for val,node in zip(a.ravel(), sorted(G.nodes())):
    if val!=0:
        G.remove_node(node)

plt.figure(figsize=(9,9))
# coordinate rotation
pos = {(x,y):(y,-x) for x,y in G.nodes()}
nx.draw(G, pos=pos, 
        node_color='grey',
        width = 4,
        node_size=400)

plt.show()

