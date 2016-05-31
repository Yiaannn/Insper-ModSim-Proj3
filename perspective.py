# -*- coding: utf-8 -*-
"""
Created on Mon May 30 11:10:58 2016

@author: Alexandre Young
"""
from cardinal import Cardinal

WINDOW_HEIGHT= 800
WINDOW_WIDTH= 600

class Perspective():
    
    def __init__(self):
        
        self.lock= None
        self.position= Cardinal(0, 0, 0)
        self.scale= 3*(10**9) #em quilômetros por pixel
        
    def window(self, celestial_body):
        x= (WINDOW_WIDTH//2) + (celestial_body.position.x - self.position.x)/self.scale
        y= (WINDOW_HEIGHT//2) - (celestial_body.position.y - self.position.y)/self.scale
        
        return x, y
    
    def perceived_size(self, celestial_body):
        pass