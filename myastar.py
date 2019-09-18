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

		self.cost = 0
		self.g = float('inf')  # g(s)
		self.h = None  # h(s)
        #the float('inf') is an unbound upper value. this means that the value can only be positive
        #the reason why this is important is because walls in the map are negative numbers, and we 
        #can't add negative numbers to our path

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

def a_star():
    """returns a boolean on whether or not a path was found between node A and B"""
    
    #visited nodes
    closed_nodes = []
    #generated nodes, not visited
    open_nodes = [start]
    
    #true as long as there still exists possible paths
    while True:
        
        #are there any generated nodes in which we haven't visited yet?
        if open_nodes == []:
            return False
        
        #moves the node with the least cost drom the open_nodes list to the closed nodes list
        current_node = open.nodes.pop(0)
        closed_nodes.append(current_node)
        
        #check if this is the goal node
        if current_node.get_solution():
            return True
        
def generate_children(current_node):
    """generates the children of the node, and adds them to the children list of the node"""   
    
	for node in all_nodes:
		if node.cost < float('inf'):
        # Checks if node is not a wall. The comparison will always be true as long as the number is not infinity or not a number
			if (current_node.x == node.x) and (current_node.y == node.y - 1 or current_node.y == node.y + 1):
				current_node.children.append(node)
			elif (current_node.y == node.y) and (current_node.x == node.x - 1 or current_node.x == node.x + 1):
				current_node.children.append(node)     
    

def main():
    node1 = SearchNode(0,0)
    print(node1.get_solution())

main()
