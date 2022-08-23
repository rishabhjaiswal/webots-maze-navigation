import itertools
from math import ceil, floor
from re import S
import sys
from this import d
from tkinter import Y
from traceback import print_tb
import numpy as np
import  math
from matplotlib import pyplot as plt
import numpy as np
import networkx as nx

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
            a['translation']=parse_translate(i)
        if 'rotation' in i:
            a['rotation']=parse_translate(i)
        if 'size' in i:
            a['size']=parse_translate(i)
    return a

def parse_translate(line):
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
    return walls


# main
walls = extractDataFromVRML('empty')
for i in walls:
    print(i)

grid = np.zeros([20, 20], dtype=float)

for i in walls:
    if i['size'][1] == 0.05: #horizontal lines
        
        if i['translation'][1] >= 0: #positve y
            print('#positve y')
            print('lower', math.ceil((i['translation'][1]-0.125)/0.5))
            lower = math.ceil((i['translation'][1]-0.125)/0.5)
            print('upper', math.ceil((i['translation'][1]+0.125)/0.5))
            upper = math.ceil((i['translation'][1]+0.125)/0.5)
            if upper == lower: #only one cell has wall passing through
                print('upper', upper)
                right_x = ceil((i['translation'][0]+i['size'][0]/2)/0.5)
                left_x = floor(((i['translation'][0]-i['size'][0]/2)/0.5))

                y_index_left = 10+left_x
                y_index_right = 10+right_x
                x_index = 10 - upper
                for i in range(y_index_left, y_index_right+1):
                    grid[x_index][i] = 1
                # print(grid)
            else:#two cell has wall passing through
                right_x = ceil((i['translation'][0]+i['size'][0]/2)/0.5)
                left_x = floor(((i['translation'][0]-i['size'][0]/2)/0.5))

                y_index_left = 10+left_x
                y_index_right = 10+right_x
                x_index_upper = 10 - upper
                x_index_lower = 10 - lower
                for i in range(y_index_left, y_index_right+1):
                    grid[x_index_lower][i] = 1
                    grid[x_index_upper][i] = 1
                # print(grid)
            
        else: #negative y
            print('negative y')
            print('lower', math.ceil((i['translation'][1]-0.125)/0.5))
            lower = math.ceil((i['translation'][1]-0.125)/0.5)
            print('upper', math.ceil((i['translation'][1]+0.125)/0.5))
            upper = math.ceil((i['translation'][1]+0.125)/0.5)
            if upper == lower: #only one cell has wall passing through
                print('upper', upper)
                right_x = ceil((i['translation'][0]+i['size'][0]/2)/0.5)
                left_x = floor(((i['translation'][0]-i['size'][0]/2)/0.5))

                y_index_left = 10+left_x
                y_index_right = 9+right_x
                x_index = 10 - upper
                for i in range(y_index_left, y_index_right+1):
                    grid[x_index][i] = 1
                # print(grid)
            else:#two cell has wall passing through
                right_x = ceil((i['translation'][0]+i['size'][0]/2)/0.5)
                left_x = floor(((i['translation'][0]-i['size'][0]/2)/0.5))

                y_index_left = 10+left_x
                y_index_right = 9+right_x
                x_index_upper = 10 - upper
                x_index_lower = 10 - lower
                for i in range(y_index_left, y_index_right+1):
                    grid[x_index_lower][i] = 1
                    grid[x_index_upper][i] = 1
                # print(grid)
    else: #vertical line

        if i['translation'][0] >= 0: #positve x

            left = math.ceil((i['translation'][0]-0.125)/0.5)
            right = math.ceil((i['translation'][0]+0.125)/0.5)
            print('#positve x', i, left, right)
            if right == left: #only one cell has wall passing through
                print('right', right)
                print((i['translation'][1]+i['size'][1]/2))
                up_y = ceil((i['translation'][1]+i['size'][1]/2)/0.5)
                print((i['translation'][1]-i['size'][1]/2))
                down_y = floor(((i['translation'][1]-i['size'][1]/2)/0.5))
                print('up_y', up_y)
                print('down_y', down_y)
                x_index_up = 10-up_y
                x_index_down = 9-down_y
                print('x_index_up', x_index_up)
                print('x_index_down', x_index_down)
                y_index = 9 + right
                for i in range(x_index_up, x_index_down+1):
                    grid[i][y_index] = 1
                # print(grid)
            else:#two cell has wall passing through
            
                print('right', right)
                print((i['translation'][1]+i['size'][1]/2))
                up_y = ceil((i['translation'][1]+i['size'][1]/2)/0.5)
                print((i['translation'][1]-i['size'][1]/2))
                down_y = floor(((i['translation'][1]-i['size'][1]/2)/0.5))
                print('up_y', up_y)
                print('down_y', down_y)
                x_index_up = 10-up_y
                x_index_down = 9-down_y
                print('x_index_up', x_index_up)
                print('x_index_down', x_index_down)
                y_index_right = 9 + right
                y_index_left = 9 + left
                for i in range(x_index_up, x_index_down+1):
                    grid[i][y_index_right] = 1
                    grid[i][y_index_left] = 1
                # print(grid)
        
        else: #negative x
            left = math.ceil((i['translation'][0]-0.125)/0.5)
            right = math.ceil((i['translation'][0]+0.125)/0.5)
            print('#positve x', i, left, right)
            if right == left: #only one cell has wall passing through
                print('right', right)
                print((i['translation'][1]+i['size'][1]/2))
                up_y = ceil((i['translation'][1]+i['size'][1]/2)/0.5)
                print((i['translation'][1]-i['size'][1]/2))
                down_y = floor(((i['translation'][1]-i['size'][1]/2)/0.5))
                print('up_y', up_y)
                print('down_y', down_y)
                x_index_up = 10-up_y
                x_index_down = 9-down_y
                print('x_index_up', x_index_up)
                print('x_index_down', x_index_down)
                y_index = 9 + right
                for i in range(x_index_up, x_index_down+1):
                    grid[i][y_index] = 1
                # print(grid)
            else:#two cell has wall passing through
            
                print('right', right)
                print((i['translation'][1]+i['size'][1]/2))
                up_y = ceil((i['translation'][1]+i['size'][1]/2)/0.5)
                print((i['translation'][1]-i['size'][1]/2))
                down_y = floor(((i['translation'][1]-i['size'][1]/2)/0.5))
                print('up_y', up_y)
                print('down_y', down_y)
                x_index_up = 10-up_y
                x_index_down = 9-down_y
                print('x_index_up', x_index_up)
                print('x_index_down', x_index_down)
                y_index_right = 9 + right
                y_index_left = 9 + left
                for i in range(x_index_up, x_index_down+1):
                    grid[i][y_index_right] = 1
                    grid[i][y_index_left] = 1
                # print(grid)


# print(grid)

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
        width = 4,
        node_size=400)

plt.show()