# -*- coding: utf-8 -*-
"""
Created on Wed May 25 13:57:48 2016

@author: Alexandre Young
"""

BLACK= (0, 0, 0)
WHITE= (255, 255, 255)
BLUE= (0, 0, 255)

def make_transparent(base, color, factor):
    base= list(base)
    color= list(color)
    
    for i in range(3):
        base[i]**= 2
        color[i]**= 2
        color[i]=color[i]*(1-factor) + base[i]*factor 
        color[i]**= 1/2
    
    color= tuple(color)
    return color
    
    