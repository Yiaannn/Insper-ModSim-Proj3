# -*- coding: utf-8 -*-
"""
Created on Wed May 18 17:13:14 2016

@author: Alexandre Young
"""

import pygame
import random

GRAVCONST= 6.67*(10**(-11)) #em Newton*(Metro quadrado)/(quilos quadrados) 
SCALE= 10**11 #em quilômetros por pixel
TIME_RESOLUTION= 1 #intervalo de tempo, em segundos, em que cada ponto é calculado
WINDOW_HEIGHT= 800
WINDOW_WIDTH= 600

display= pygame.display
draw= pygame.draw
event= pygame.event
current_time= pygame.time.get_ticks
sleep= pygame.time.wait
canvas= pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
BLACK= (0, 0, 0)
WHITE= (255, 255, 255)
BLUE= (0, 0, 255)
run= True
    
def crunch_pygame_events():
    event.pump()
    list= event.get()
    run= True
    
    for stuff in list:
        if stuff.type == pygame.QUIT:
            run= False
            
    return run
    
class StarDome():

    def __init__(self):
        #generate stars
        starnum= 60
        self.star= []
        
        for num in range(starnum):
            self.star.append( [(random.randint(0, WINDOW_HEIGHT-1), random.randint(0, WINDOW_WIDTH-1)), random.randint(1, 4) ])
    
    def draw(self):
        canvas.fill(BLACK)
        for stup in self.star:
            draw.circle(canvas, WHITE, stup[0], stup[1])
            
    def update(self):
        None

class Cardinal:
    
    def __init__(self, x, y, z):
        self.x= x
        self.y= y
        self.z= z
    
class CenterBody:
    
    def __init__(self, mass, radius):
        #Por definição, o corpo central está nos pontos (0, 0, 0) do sistema
        #Como consequência da primeira afirmação, sua velocidade em qualquer eixo
        #   sempre é zero
        #massa é dada em quilos
        
        self.position= Cardinal(0, 0, 0)
        self.speed= Cardinal(0, 0, 0)
        self.mass= mass
        self.radius= radius
        
        self.celestial_neighbor= []
        
    def draw(self):
        #draw.circle(canvas, BLUE, (WINDOW_HEIGHT//2, WINDOW_WIDTH//2), int(self.radius/SCALE))
        draw.circle(canvas, BLUE, (WINDOW_HEIGHT//2, WINDOW_WIDTH//2), 20)
        
    def update(self):
        None
    
class OrbitalBody:
    
    def __init__(self, distance, speed, mass, radius):
        #distance é dada em metros
        #speed em metros por segundo
        #mass em quilos
        
        self.position= Cardinal(distance, 0, 0)
        self.speed= Cardinal(0, speed, 0)
        self.mass= mass
        self.radius= radius
        
        self.celestial_neighbor= []
    
    def update(self):
        self.update_position()
        self.update_speed()
    
    def update_position(self):
        
        self.position.x+= self.speed.x*TIME_RESOLUTION
        self.position.y+= self.speed.y*TIME_RESOLUTION
        self.position.z+= self.speed.z*TIME_RESOLUTION
        
    def update_speed(self):        
        
        for celestial_body in self.celestial_neighbor:
            
            partial= (GRAVCONST*celestial_body.mass)
            
            if self.position.x > 0: 
                self.speed.x-= partial/(self.position.x**2)*TIME_RESOLUTION
            elif self.position.x < 0:
                self.speed.x+= partial/(self.position.x**2)*TIME_RESOLUTION
                
            if self.position.y > 0:
                self.speed.y-= partial/(self.position.y**2)*TIME_RESOLUTION
            elif self.position.y < 0:
                self.position.y+= partial/(self.position.y**2)*TIME_RESOLUTION
            #self.speed_z= partial/(self.distance_z**2)*time_lapse
                
            print ("DEBUG: "+str(partial/(self.position.y**2)*TIME_RESOLUTION))
            #print ("DEBUG: "+str(self.speed_y))
        
    def add_neighbor(self, celestial_body):
        
        self.celestial_neighbor.append(celestial_body)
        
    def draw(self):
        #draw.circle(canvas, WHITE, (int(WINDOW_HEIGHT//2+self.distance_x/SCALE), int(WINDOW_WIDTH//2+self.distance_y/SCALE)), int(self.radius/SCALE))
        draw.circle(canvas, WHITE, (int(WINDOW_HEIGHT//2+self.position.x/SCALE), int(WINDOW_WIDTH//2+self.position.y/SCALE)), 20)
        print(self.position.x)
        print(self.position.y)
        print("~~~")
#

center= CenterBody(1.98855*(10**30), 695700*(10**3)) #dados referentes ao Sol
#orbital= OrbitalBody(405400*(10**3), 959.583333333333333333333, 7.342* (10**22)) #dados referentes à lua
orbital= OrbitalBody(816.04*(10**9), 12.44*(10**3), 1.8986*(10**27), 69911*(10**3)) #dados referentes à jupiter
orbital.add_neighbor(center)
dome= StarDome()
#--MAIN LOOP--
while run:
    sleep( 100)
    
    run= crunch_pygame_events()
    
    #update things
    dome.update()
    center.update()
    orbital.update()
    
    #draw things
    dome.draw()
    center.draw()
    orbital.draw()
    
    display.flip()