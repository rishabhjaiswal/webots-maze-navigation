import itertools
from math import ceil, floor
from tkinter import Y
import numpy as np
import sys
import math
from matplotlib import pyplot as plt
import numpy as np
import networkx as nx

# start_x, start_y = input("Enter starting point coordiates:").split
# print("Username is: " + start_x, start_y)

  
# taking two inputs at a time
file_name = input("Enter file name : ")
start_x, start_y = map(int, input("Enter starting point coordiates: ").split())
end_x, end_y = map(int, input("Enter starting point coordiates: ").split())

np.set_printoptions(threshold=sys.maxsize)

def skip_pass(marker, lines):
    """
    Skip until reach the line which contains the marker, then also skip
    the marker line
    """
    result = itertools.dropwhile(
        lambda line: marker not in line,  # Condition
        lines)                            # The lines
    next(result)                          # skip pass the markers
    return result

def take(marker, lines):
    """
    Take and return those lines which contains a marker
    """
    result = itertools.takewhile(
        lambda line: marker not in line,      # Condition
        lines)                            # The lines
    
    return result

def parse_walls(lines):
    """
    Parse one block of 'Walls'
    """
    point_lines = take('}', lines)
    a={}
    for i in point_lines:
        if 'translation' in i:
            a['translation']=parse_values(i)
        if 'rotation' in i:
            a['rotation']=parse_values(i)
        if 'size' in i:
            a['size']=parse_values(i)

        # if 'floorSize' in i:
        #     a['floorSize']=parse_values(i)
        # else:
        #     a['floorSize'] = [1, 1]
        # if 'floorTileSize' in i:
        #     a['floorTileSize']=parse_values(i)
        # else:
        #     a['floorTileSize'] = [0.5, 0.5]
    return a

def parse_arena_info(lines):
    """
    Parse one block of 'Walls'
    """
    point_lines = take('}', lines)
    a={}
    for i in point_lines:
        if 'floorSize' in i:
            a['floorSize']=parse_values(i)
            
        
    a['floorTileSize'] = [0.5, 0.5]
    return a



    
def parse_values(line):
    """
    Given a line such as: "translate 5 6 7", return [5.0, 6.0, 7.0]
    """
    translate = [float(x) for x in line.split()[1:]]
    return translate

def extractDataFromVRML(root):
    walls = []
    with open(root + '.wbt') as infile:
        for line in infile:
            if 'Wall' in line:
                a_set = parse_walls(lines=infile)
                walls.append(a_set)
            if 'RectangleArena' in line:
                
                arena_prop = parse_arena_info(lines=infile)
    return walls, arena_prop


# main
walls, arena_info = extractDataFromVRML(file_name)
for i in walls:
    print('i', i)

grid_size = [int(arena_info['floorSize'][0]/arena_info['floorTileSize'][0]), int(arena_info['floorSize'][1]/arena_info['floorTileSize'][1])]

grid = np.zeros(grid_size, dtype=float)
for i in walls:

    if i['size'][1] == 0.05: #horizontal lines
        if i['translation'][1] >= 0: #positve y
            lower = math.ceil((i['translation'][1]-(i['size'][1])/2)/arena_info['floorTileSize'][1])
            upper = math.ceil((i['translation'][1]+(i['size'][1])/2)/arena_info['floorTileSize'][1])
            if upper == lower: #only one cell has wall passing through
                right_x = ceil((i['translation'][0]+i['size'][0]/2)/arena_info['floorTileSize'][0])
                left_x = floor(((i['translation'][0]-i['size'][0]/2)/arena_info['floorTileSize'][0]))
                
                y_index_left = int(arena_info['floorSize'][0])+left_x
                y_index_right = int(arena_info['floorSize'][0])+right_x
                x_index = int(arena_info['floorSize'][1]) - upper
                
                for i in range(y_index_left, y_index_right):
                    grid[x_index][i] = 1
            else:#two cell has wall passing through

                right_x = ceil((i['translation'][0]+i['size'][0]/2)/arena_info['floorTileSize'][0])
                left_x = floor(((i['translation'][0]-i['size'][0]/2)/arena_info['floorTileSize'][0]))
                
                y_index_left = int(arena_info['floorSize'][0])+left_x
                y_index_right = int(arena_info['floorSize'][0])+right_x
                x_index_upper = int(arena_info['floorSize'][1]) - upper
                x_index_lower = int(arena_info['floorSize'][1]) - lower 
                for i in range(y_index_left, y_index_right):
                    grid[x_index_lower][i] = 1
                    grid[x_index_upper][i] = 1
            
        else: #negative y
            lower = math.ceil((i['translation'][1]-(i['size'][1]/2))/arena_info['floorTileSize'][1])
            upper = math.ceil((i['translation'][1]+(i['size'][1]/2))/arena_info['floorTileSize'][1])
            
            
           
            if upper == lower: #only one cell has wall passing through
                right_x = ceil((i['translation'][0]+i['size'][0]/2)/arena_info['floorTileSize'][0])
                left_x = floor(((i['translation'][0]-i['size'][0]/2)/arena_info['floorTileSize'][0]))

                y_index_left = int(arena_info['floorSize'][0]+left_x)
                y_index_right = int(arena_info['floorSize'][0]+right_x)
                x_index = int(arena_info['floorSize'][1]) - upper 
                for i in range(y_index_left, y_index_right):
                    grid[x_index][i] = 1
            else:#two cell has wall passing through
                right_x = ceil((i['translation'][0]+i['size'][0]/2)/arena_info['floorTileSize'][0])
                left_x = floor(((i['translation'][0]-i['size'][0]/2)/arena_info['floorTileSize'][0]))

                y_index_left = int(arena_info['floorSize'][0]+left_x)
                y_index_right = int(arena_info['floorSize'][0]+right_x)
                x_index_upper = int(arena_info['floorSize'][1] - upper)
                x_index_lower = int(arena_info['floorSize'][1] - lower) 
                for i in range(y_index_left, y_index_right):
                    grid[x_index_lower][i] = 1
                    grid[x_index_upper][i] = 1
    else: #vertical line

        if i['translation'][0] >= 0: #positve x

            left = math.ceil((i['translation'][0]-i['size'][0]/2)/arena_info['floorTileSize'][0])
            right = math.ceil((i['translation'][0]+i['size'][0]/2)/arena_info['floorTileSize'][0])
            if right == left: #only one cell has wall passing through
                up_y = ceil((i['translation'][1]+i['size'][1]/2)/arena_info['floorTileSize'][1])
                down_y = floor(((i['translation'][1]-i['size'][1]/2)/arena_info['floorTileSize'][1]))
                x_index_up = int(arena_info['floorSize'][1]-up_y)
                x_index_down = int(arena_info['floorSize'][1]-down_y)
                y_index = int(arena_info['floorSize'][1] - 1 + right)
                for i in range(x_index_up, x_index_down):
                    grid[i][y_index] = 1
            else:#two cell has wall passing through
            
                up_y = ceil((i['translation'][1]+i['size'][1]/2)/arena_info['floorTileSize'][1])
                down_y = floor(((i['translation'][1]-i['size'][1]/2)/arena_info['floorTileSize'][1]))
                x_index_up = int(arena_info['floorSize'][1]-up_y)
                x_index_down = int(arena_info['floorSize'][1]-down_y)
                y_index_right = int(arena_info['floorSize'][1] - 1 + right)
                y_index_left = int(arena_info['floorSize'][1] - 1 + left)
                for i in range(x_index_up, x_index_down):
                    grid[i][y_index_right] = 1
                    grid[i][y_index_left] = 1
        
        else: #negative x
            left = math.ceil((i['translation'][0]-0.025)/arena_info['floorTileSize'][0])
            right = math.ceil((i['translation'][0]+0.025)/arena_info['floorTileSize'][0])
            if right == left: #only one cell has wall passing through
                up_y = ceil((i['translation'][1]+i['size'][1]/2)/arena_info['floorTileSize'][1])
                down_y = floor(((i['translation'][1]-i['size'][1]/2)/arena_info['floorTileSize'][1]))
                x_index_up = int(arena_info['floorSize'][1]-up_y)
                x_index_down = int(arena_info['floorSize'][1]-down_y)
                y_index = int(arena_info['floorSize'][1] - 1 + right)
                for i in range(x_index_up, x_index_down):
                    grid[i][y_index] = 1
            else:#two cell has wall passing through
                up_y = ceil((i['translation'][1]+i['size'][1]/2)/arena_info['floorTileSize'][1])
                down_y = floor(((i['translation'][1]-i['size'][1]/2)/arena_info['floorTileSize'][1]))
                x_index_up = int(arena_info['floorSize'][1]-up_y)
                x_index_down = int(arena_info['floorSize'][1]-down_y)
                y_index_right = int(arena_info['floorSize'][1] - 1 + right)
                y_index_left = int(arena_info['floorSize'][1] - 1 + left)
                
                for i in range(x_index_up, x_index_down):
                    grid[i][y_index_right] = 1
                    grid[i][y_index_left] = 1


print(grid)

# define grid graph according to the shape of a
G = nx.grid_2d_graph(*grid.shape)


# remove those nodes where the corresponding value is != 0
for val,node in zip(grid.ravel(), sorted(G.nodes())):
    if val!=0:
        G.remove_node(node)
    

plt.figure(figsize=(9,9))
# coordinate rotation
pos = {(x,y):(y,-x) for x,y in G.nodes()}
nx.draw(G, pos=pos, 
        node_color='grey', 
        with_labels = True,
        width = 4,
        node_size=400)

# figManager = plt.get_current_fig_manager()
# figManager.resize(*figManager.window.maxsize())

plt.show()


def dist(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

nx.set_edge_attributes(G, {e: e[1][0] * 2 for e in G.edges()}, 1)
path = nx.astar_path(G, (start_x, start_y), (end_x, end_y), heuristic=dist, weight=1)
length = nx.astar_path_length(G, (start_x, start_y), (end_x, end_y), heuristic=dist, weight=1)
print('Path:', path)
print('path length A* : ', length)



pos = {(x,y):(y,-x) for x,y in G.nodes()}
nx.draw(G, pos, with_labels = True, node_color = ["blue" if n in path else "red" for n in G.nodes()]
)
edge_labels = nx.get_edge_attributes(G, 1)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()

path_dijkstra = nx.shortest_path_length(G, source=(start_x, start_y), target=(end_x, end_y), method='dijkstra', weight=1)
print('path length dijkstra : ', path_dijkstra)

path_bellman_ford = nx.shortest_path_length(G, source=(start_x, start_y), target=(end_x, end_y), method='bellman-ford', weight=1)
print('path length bellman-ford : ', path_bellman_ford)