# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 18:19:59 2019

@author: Kari Ness
"""
#change to int representation
#check order of coordinates
#check the updates of the cost
#må hente inn nodene fra nodes

import map
import math as m


class Node():
    """A node class for A* Pathfinding"""

    #initialiserer noden
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.children = []

        self.g = float('inf') #the cost of getting from the root to node s
        self.h = None #the estimated distance from s to a goal state
        
        
        self.cost = 0 
        

    def __eq__(self, other):
        """finds if the nodes are equal"""
        return self.position == other.position
    
    def __str__(self):
        return "x: " + str(self.position) + ", y: " + str(self.position) + ", cost: " + str(self.cost)
    
    def f(self):

    	"""Method for getting f(node), which is the total cost (cost so far + estimated cost to goal)
    	:return: g(node) + h(node)"""
    	return self.g + self.h
    
def a_star(map_string, start, end, nodes):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    # Create start and end node
    print(nodes)
    print(type(nodes))
    for node in nodes:
        print(node)
    end_node = Node(None,tuple(end))
    print(end_node)
    start_node = Node(None,tuple(start))
    end_node.h = 0
    start_node.g = 0
    start_node.h = euclidian_distance(start_node, end_node)
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
            return False  
        
        # Get the current node
        current_node = open_list.pop()
        #print(current_node)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return True


        
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (map_shape(map_string)[1] - 1) or node_position[0] < 0 or node_position[1] > (map_shape(map_string)[0] - 1) or node_position[1] < 0:
                continue
                #map_shape(map_string)[1] returns the number of columns, x
                #map_shape(map_string)[0] returns the number of columns, y

            # Make sure walkable terrain
            if map_string[node_position[1]][node_position[0]] == -1:
                continue

#            # Create new node
#            for node in nodes:
#                print(101)
#                if node_position == node.position:
#                    new_node = node
#            if new_node == None:
                new_node = Node(current_node, node_position)

            new_node = Node(current_node, node_position)
            
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
    child.h = euclidian_distance(child, end_node)       
            
def generate_map(task):
    map_obj = map.Map_Obj(task=1)
    #in string format
    return map_obj.get_maps()[1]

def map_shape(map_string):
    """shape will return a tuple (m, n), where m is the number of rows, and n is the number 
    of columns."""
    return map_string.shape

#initializing the nodes
def create_nodes(map_string):
    
    #finds the number of rows and columns in my map of nodes
    rows = map_shape(map_string)[0]
    columns = map_shape(map_string)[1]
    
    #initializing the nodes list
    nodes = []
    start_node = []
    end_node = []

    for x_cord in range(columns):
        for y_cord in range(rows):
            node_position = [y_cord, x_cord]
            node = map_string[y_cord][x_cord]
            node.strip()
            map_string[y_cord][x_cord] = node #strip takes away redundant space
            print(node_position)
            if node == '#': #found wall-node
                wall_node = Node(node_position)
                wall_node.cost = float('inf')
                nodes.append(wall_node)
                
            elif node == 'A':  # Found start-node
                start_node = Node(node_position)
                nodes.append(start_node)
            
            elif node == 'B':  # Found goal-node
                goal_node = Node(node_position)
                nodes.append(goal_node)
                
            else: #found regular node
                search_node = Node(node_position)
                search_node.cost = 1
                nodes.append(search_node)
    return map_string, nodes, end_node, start_node

##initializing the nodes
#def create_nodes(map_int):
#    
#    #finds the number of rows and columns in my map of nodes
#    rows = map_shape(map_int)[0]
#    columns = map_shape(map_int)[1]
#    
#    #initializing the nodes list
#    nodes = []
#    start_node = []
#    end_node = []
#
#    for x_cord in range(columns):
#        for y_cord in range(rows):
#            node_position = [y_cord, x_cord]
#            node = map_int[y_cord][x_cord]
#            node.strip()
#            map_int[y_cord][x_cord] = node #strip takes away redundant space
#            
#            
#            if node == -1: #found wall-node
#                wall_node = Node(node_position)
#                wall_node.cost = float('inf')
#                nodes.append(wall_node)
#                
#            else: #found regular node
#                search_node = Node(node_position)
#                search_node.cost = 1
#    return map_int, nodes, end_node, start_node

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
        path.append(current.position)
        current = current.parent
        return path[::-1] # Return reversed path

def main():
    
    #creates the map
    map_obj = map.Map_Obj(task=1)
    map_string = generate_map(1)
    #map_int = map_obj.get_maps()[0]
    
    #updates map_string to not contain any space and updates the cost of the nodes
    #nodes-list has all the nodes in the  map
    map_string, nodes, end_node, start_node = create_nodes(map_string)
    print(nodes[1])
    start = map_obj.get_start_pos()
    end = map_obj.get_goal_pos()
    
    #script
    if a_star(map_string, start, end, nodes):
        path = get_path(end_node)
        print(path)        
    else:
        print("There's no path between the given nodes")
        
    
main()
    