# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 19:11:50 2019

@author: Kari Ness
"""
import math
import map

class SearchNode():
	"""
	Class for node in board to be searched
	"""

	def __init__(self, x, y):
		"""
		Initializes the search node
		:param x: x-coordinate of node
		:param y: y-coordinate of node
		"""
		self.start = False
		self.solution = False
		self.type = None
		self.in_path = False

		self.x = x
		self.y = y

		self.children = []
		self.parent = None

		self.f = 0
		self.g = 0  # g(s)
		self.h = 0  # h(s)
        

	def f(self):
		"""
		Method for getting f(node), which is the total cost (cost so far + estimated cost to goal)
		:return: g(node) + h(node)
		"""
		return self.g + self.h

	def __str__(self):
		return "x: " + str(self.x) + ", y: " + str(self.y) + ", cost: " + str(self.cost)

	def get_solution(self):
		return self.solution

def a_star(map_obj, start, end):
    """returns a boolean on whether or not a path was found between node A and B"""
    
    #creates map
    map_string = generate_map(1)
    
    #visited nodes
    closed_nodes = []
    #generated nodes, not visited
    open_nodes = [start]
    
    #true as long as there still exists possible paths
    while True:
        
        #are there any generated nodes in which we haven't visited yet?
        if open_nodes == []:
            return False
        
        #moves the node with the least cost from the open_nodes list to the closed nodes list
        current_node = open_nodes.pop(0)
        closed_nodes.append(current_node)
        
        #check if this is the goal node
        if current_node.get_solution():
            return True

        #generates the children of the node, and adds them to the children list of the node
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: 
        # Adjacent nodes
        
                # Get node position
                node_position = (current_node.x + new_position[0], current_node.y + new_position[1])
        
                # Make sure within range
                if node_position[0] > (map_shape(map_string)[1] - 1) or node_position[0] < 0 or node_position[1] > (map_shape(map_string)[0] - 1) or node_position[1] < 0:
                    continue
                    #map_shape(map_string)[1] returns the number of columns, x
                    #map_shape(map_string)[0] returns the number of columns, y
                    
                    #want to send out a outofbounds fail
        
                # Make sure walkable terrain
                if map_string[node_position[0]][node_position[1]] != 0:
                    continue
        
                # Create new node
                new_node = SearchNode(node_position[0],node_position[1])
                new_node.parent = current_node
                
        
                # Append
                children.append(new_node)
                
                #iterate through all the children
                for child in children:
        
                     # Child is on the closed list
                     #have we already added the node to pur path?
                    for closed_child in closed_list:
                        if child == closed_child:
                            continue
        
                    # Create the f, g, and h values
                    child.g = current_node.g + 1
                    child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                    child.f = child.g + child.h
        
                    # Child is already in the open list
                    for open_node in open_list:
                        if child == open_node and child.g > open_node.g:
                            continue
        
                    # Add the child to the open list
                    open_list.append(child)
        
                    for child in children:
                    
                        # Child is on the closed list
                        #have we already added the node to pur path?
                        for closed_child in closed_list:
                             if child == closed_child:
                                 continue
                    
                        # Create the f, g, and h values
                        child.g = current_node.g + 1
                        child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                        child.f = child.g + child.h
                        
                        # Child is already in the open list
                        for open_node in open_list:
                            if child == open_node and child.g > open_node.g:
                                continue
                        
                        # Add the child to the open list
                        open_list.append(child)

def generate_map(task):
    map_obj = map.Map_Obj(task=1)
    #in string format
    return map_obj.get_maps()[1]

def map_shape(map_string):
    """shape will return a tuple (m, n), where m is the number of rows, and n is the number 
    of columns."""
    return map_string.shape

def main():
    map_obj = map.Map_Obj(task=1)
    map_string = generate_map(1)
    print(map_shape(map_string))
    print(type(map_string))
    start = map_obj.get_start_pos()
    end = map_obj.get_goal_pos()
    #path = a_star(map_string, start, end)
    #print(path)

main()
