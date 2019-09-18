# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:20:52 2019

@author: Kari Ness
"""
import map
import temp


map_obj = map.Map_Obj(task=1)

map_string = map_obj.get_maps()[1]
map_int = map_obj.get_maps()[0]

#print(map_int)
map_obj.show_map(map=None)



def main():
    map_int = (map_obj.get_maps()[0])
    #print(type(map_int[0][0]))
    start_pos = tuple(map_obj.get_start_pos())
    goal_pos = tuple(map_obj.get_goal_pos())
    
    map_int =[list(x) for x in map_int]
    
    print(map_string)
    
    path1 = temp.astar(map_int, start_pos, goal_pos)
    print(path1)
    
main()