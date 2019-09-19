# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 18:19:59 2019

@author: Kari Ness
"""
import map


class Node():
    """A node class for A* Pathfinding"""

    #initialiserer noden
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        """finds if the nodes are equal"""
        return self.position == other.position
    
    def __str__(self):
        """prints information about the node"""
        return "x: " + str(self.position[0]) + ", y: " + str(self.position[1]) + ", f: " + str(self.f)
    
    def f(self):

    	"""Method for getting f(node), which is the total cost (cost so far + estimated cost to goal)
    	:return: g(node) + h(node)"""
    	return self.g + self.h
    
def a_star(map_obj, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None,tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None,tuple(end))
    end_node.g = end_node.h = end_node.f = 0
    
    #creates the map
    map_string = generate_map(1)

    # Initialize both open and closed list
    
    #Genererte noder som ikke er besøkt
    open_list = []
    #besøkte noder 
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    
    # Loop until you find the end
    while len(open_list) > 0:
        print(1)
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        
        #finds out if there exists a node in open_list with a lower f-value
        #if there exist such a node, this node will be put in front in the open_list
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current node off open list, add to closed list
      # print(open_list[0].__str__())
        open_list.pop(current_index)
        closed_list.append(current_node)
        print(closed_list[0].__str__())
        print(len(open_list))
        print(len(closed_list))

        # Found the goal
        if current_node == end_node:
            print("inside the loop where we've found the end_node")
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (map_shape(map_string)[1] - 1) or node_position[0] < 0 or node_position[1] > (map_shape(map_string)[0] - 1) or node_position[1] < 0:
                continue
                #map_shape(map_string)[1] returns the number of columns, x
                #map_shape(map_string)[0] returns the number of columns, y

            # Make sure walkable terrain
            if map_string[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
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
    start = map_obj.get_start_pos()
    end = map_obj.get_goal_pos()
    path = a_star(map_string, start, end)
    #print(path)
    
main()
    