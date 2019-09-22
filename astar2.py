# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 14:30:13 2019

@author: Kari Ness
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 18:19:59 2019

@author: Kari Ness
"""
#change to int representation
#check order of coordinates
#check the updates of the cost
#må hente inn nodene fra nodes

#clear all close all
import os
clear = lambda: os.system('cls')  # On Windows System
clear()

import map
import math as m
from PIL import Image


class Node():
    """A node class for A* Pathfinding"""

    #initialiserer noden
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.children = []

        self.g = float('inf') #the cost of getting from the root to node s
        self.h = None #the estimated distance from s to a goal state
        
        self.cost = 1 
        

    def __eq__(self, other):
        """finds if the nodes are equal"""
        return self.position == other.position
    
    def __str__(self):
        return "x: " + str(self.position[1]) + ", y: " + str(self.position[0]) + ", cost: " + str(self.cost)
    
    def f(self):

    	"""Method for getting f(node), which is the total cost (cost so far + estimated cost to goal)
    	:return: g(node) + h(node)"""
    	return self.g + self.h
    
def a_star(map_int, start, end, nodes):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    # Create start and end node
    end_node = Node(None,tuple(end))
    end_node.h = 0
    end_node.cost = 1    
    
    start_node = Node(None,tuple(start))
    start_node.g = 0
    start_node.h = euclidian_distance(start_node, end_node)
    start_node.cost = 0
            

    # Initialize both open and closed list
    #visited nodes
    open_list = []
    #generated nodes, not visited
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    
    # Loop until you find the end
    #while len(open_list) > 0:
    while True:
        #failure occurs if there are no more nodes in the open_list
        if not open_list:
            return False, None  
        
        # Get the current node
        current_node = open_list.pop()
        closed_list.append(current_node)
        
        # Found the goal
        if current_node == end_node:
            return True, current_node
        
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position 
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            
            #check that the node_position is within the range
            if node_position[0] > (map_shape(map_int)[0] - 1) or node_position[0] < 0 or node_position[1] > (map_shape(map_int)[1] - 1) or node_position[1] < 0:
                continue
                #map_shape(map_string)[1] returns the number of columns, x
                #map_shape(map_string)[0] returns the number of columns, y

            # Make sure walkable terrain (not a wall, value = -1)
            if map_int[node_position[0]][node_position[1]] == -1:
                continue

            new_node = Node(current_node, node_position)
            
            for node in nodes:
                if node_position == node.position:
                    new_node.cost = node.cost
                    new_node.g = node.g
                    new_node.h = node.h
                    continue

            # Append
            current_node.children.append(new_node)

        # Loop through children
        for child in current_node.children:
            
            if child not in open_list and child not in closed_list:
                #the child is not in the closed list, and has and if it is in the open_list,
                #it has a lower g-value
                #updates information about the relationship between parent and child
                attach_and_eval(child, current_node, end_node)
                #adds the child to the open list
                open_list.append(child)
                #sorts the open_list so that the node with the lowest estimated cost is in pos=0
                open_list.sort(key=lambda x: x.f())  

            elif current_node.g + child.cost < child.g:  #true if there exists a cheaper path to s
                attach_and_eval(child, current_node, end_node)
                if child in closed_list:
                    propagate_path_improvements(child)

def attach_and_eval(child, parent, end_node):
    """updates information in relationship between child and parent"""
    child.parent = parent
    
     # Create the g and h values
    child.g = parent.g + child.cost
    child.h = manhattan_distance(child, end_node)       
            
def map_shape(map_int):
    """shape will return a tuple (m, n), where m is the number of rows, and n is the number 
    of columns."""
    return map_int.shape

#initializing the nodes with int file
def create_nodes(map_obj):
    
    map_int = map_obj.get_maps()[0]
    start = tuple(map_obj.get_start_pos())
    end = tuple(map_obj.get_goal_pos())

    
    
    #finds the number of rows and columns in my map of nodes
    rows = map_shape(map_int)[0]
    columns = map_shape(map_int)[1]
    
    #initializing the nodes list
    nodes = []
    start_node = []
    end_node = []

    for x_cord in range(columns):
        for y_cord in range(rows):
            node_position = [y_cord, x_cord]
            node = map_int[y_cord][x_cord]
            map_int[y_cord][x_cord] = node #strip takes away redundant space
            
            
            if node == -1: #found wall-node
                wall_node = Node(node_position)
                wall_node.position = tuple(node_position)
                wall_node.cost = float('inf')
                nodes.append(wall_node)
                
            elif node == 2:
                stair_node = Node(node_position)
                stair_node.position = tuple(node_position)
                wall_node.cost = 2
                nodes.append(stair_node)
                
            elif node == 3:
                packed_stair_node = Node(node_position)
                packed_stair_node.position = tuple(node_position)
                packed_stair_node.cost = 3
                nodes.append(packed_stair_node)
                
            elif node == 4:
                packed_room_node = Node(node_position)
                packed_room_node.position = tuple(node_position)
                packed_room_node.cost = 4
                nodes.append(packed_room_node)
                
            else: #found regular node
                search_node = Node(node_position)
                search_node.position = tuple(node_position)
                search_node.cost = 1
                if search_node.position == start:
                    search_node.cost = 0
                    start_node.append(search_node)
                elif search_node.position == end:
                    end_node.append(search_node)
           
    return nodes, start_node, end_node

def propagate_path_improvements(parent):
    for child in parent.children:
        if parent.g + child.cost < child.g:
            child.parent = parent
            child.g = parent.g + child.cost
            propagate_path_improvements(child)

    
def euclidian_distance(node, end):
	"""
	:param node: Node in board
	:return: Euclid distance from node to goal
	"""
	return m.sqrt(m.pow(end.position[0] - node.position[0], 2) + m.pow(end.position[1] - node.position[1], 2))

def manhattan_distance(node, end):
	"""
	:param node: Node in board
	:return: Manhattan distance from node to goal
	"""
	return abs(end.position[0] - node.position[0]) + abs(end.position[1] - node.position[1])

def get_path(end_node):
    path = []
    current = end_node

    #creates path by saving the parents until one reach the start node
    while current is not None:
        path.append(current)
        current = current.parent
        
    return path[::-1] # Return reversed path

def update_map_path(map_obj, path):
    """adds the path to the map_obj. returns the string version of the map, with the path marked as ' Y '"""
    map_string = map_obj.get_maps()[1]
    start = tuple(map_obj.get_start_pos())
    end = tuple(map_obj.get_goal_pos())

    #finds the number of rows and columns in my map of nodes
    rows = map_shape(map_string)[0]
    columns = map_shape(map_string)[1]
    
    for x_cord in range(columns):
        for y_cord in range(rows):
            node_position = tuple([y_cord, x_cord])
            
            for item in path:
                if item.position == node_position and item.position != start and item.position != end:
                    map_string[y_cord][x_cord] = ' Y '
    return map_string

def show_map1(map_string):
    """
    A function used to draw the map as an image and show it.
    :param map: map to use
    :return: nothing."""

    # Define width and height of image
    width = map_shape(map_string)[1]
    height = map_shape(map_string)[0]
    # Define scale of the image
    scale = 20
    # Create an all-yellow image
    image = Image.new('RGB', (width * scale, height * scale), (255, 255, 0))
    # Load image
    pixels = image.load()

    # Define what colors to give to different values of the string map (undefined values will remain yellow, this is
    # how the yellow path is painted)
    colors = {' # ': (255, 0, 0), ' . ': (215, 215, 215), ' , ': (166, 166, 166), ' : ': (96, 96, 96),
              ' ; ': (36, 36, 36), ' S ': (255, 0, 255), ' G ': (0, 128, 255), ' Y ':(255,255,0)}
    
    #(255,0,0) - red
    #(215,215,215) - light grey
    #(166,166,166) - grey
    #(96,96,96) - dark grey
    #(36,36,36) - black
    #(255,0,255) - purple
    #(0,128,255) - blue
    #(255,255,0) - yellow
    
    # Go through image and set pixel color for every position
    for y in range(height):
        for x in range(width):
            if map_string[y][x] not in colors: continue
            for i in range(scale):
                for j in range(scale):
                    pixels[x * scale + i, y * scale + j] = colors[map_string[y][x]]
    # Show image
    image.show()

def main():
#    
#    #initialization - task 1 -part 1
#    map_obj = map.Map_Obj(task=1)
#    map_int = map_obj.get_maps()[0]
#
#    
#    #updates map_string to not contain any space and updates the cost of the nodes
#    #nodes-list has all the nodes in the  map
#    nodes, start_node, end_node = create_nodes(map_obj)
#    start = map_obj.get_start_pos()
#    end = map_obj.get_goal_pos()
#   
#    #script task 1 - part 1
#    if a_star(map_int, start, end, nodes)[0] == True:
#        print("Path found")
#        print("Start-node:", start)
#        print("End-node:", end)
#        
#        goal = a_star(map_int, start, end, nodes)[1]
#        path = get_path(goal)
##        for item in path:
#            #print(item)
#
#    else:
#        print("There's no path between the given nodes")
#    
#    map_1 = map.Map_Obj(task=1)
#    map_string = update_map_path(map_1,path)
#    show_map1(map_string)
#
#    #initialization - task 2 - part 1
#    map_obj2 = map.Map_Obj(task=2)
#    map_int2 = map_obj.get_maps()[0]
#
#    #updates map_string to not contain any space and updates the cost of the nodes
#    #nodes-list has all the nodes in the  map
#    nodes2, start_node2, end_node2 = create_nodes(map_obj)
#    start2 = map_obj2.get_start_pos()
#    end2 = map_obj2.get_goal_pos()
#    
#    #script task 2 - part 1
#    if a_star(map_int2, start2, end2, nodes2)[0] == True:
#        print("Path2 found")
#        print("Start-node:", start2)
#        print("End-node:", end2)
#        
#        goal2 = a_star(map_int2, start2, end2, nodes2)[1]
#        path2 = get_path(goal2)
##        for item in path:
#            #print(item)
#
#    else:
#        print("There's no path between the given nodes")
#    
#    map_2 = map.Map_Obj(task=2)
#    map_string2 = update_map_path(map_2,path2)
#    show_map1(map_string2)
#    
#    #initialization - task 3 - part 2
#    map_obj3 = map.Map_Obj(task=3)
#    map_int3 = map_obj3.get_maps()[0]
#    
#    #updates map_string to not contain any space and updates the cost of the nodes
#    #nodes-list has all the nodes in the  map
#    nodes3, start_node3, end_node3 = create_nodes(map_obj3)
#    start3 = map_obj3.get_start_pos()
#    end3 = map_obj3.get_goal_pos()
#    
#    #script task 3 - part 2
#    if a_star(map_int3, start3, end3, nodes3)[0] == True:
#        print("Path found")
#        print("Start-node:", start3)
#        print("End-node:", end3)
#        
#        goal3 = a_star(map_int3, start3, end3, nodes3)[1]
#        path3 = get_path(goal3)
##        for item in path:
#            #print(item)
#
#    else:
#        print("There's no path between the given nodes")
#    
#    map_3 = map.Map_Obj(task=3)
#    map_string3 = update_map_path(map_3,path3)
#    show_map1(map_string3)
    
    #initialization - task 4 - part 2
    map_obj4 = map.Map_Obj(task=4)
    map_int4 = map_obj4.get_maps()[0]
    
    #updates map_string to not contain any space and updates the cost of the nodes
    #nodes-list has all the nodes in the  map
    nodes4, start_node4, end_node4 = create_nodes(map_obj4)
    start4 = map_obj4.get_start_pos()
    end4 = map_obj4.get_goal_pos()
    
    #script task 1 - part 1
    if a_star(map_int4, start4, end4, nodes4)[0] == True:
        print("Path found")
        print("Start-node:", start4)
        print("End-node:", end4)
        
        goal4 = a_star(map_int4, start4, end4, nodes4)[1]
        path4 = get_path(goal4)
#        for item in path:
            #print(item)

    else:
        print("There's no path between the given nodes")
    
    map_4 = map.Map_Obj(task=4)
    map_string4 = update_map_path(map_4,path4)
    show_map1(map_string4)
    
main()