# -*- coding: utf-8 -*-
"""
Created on Wed May 18 17:13:14 2016

@author: Alexandre Young
"""

import pygame
import random
import color

GRAVCONST= 6.67*(10**(-11)) #em Newton*(Metro quadrado)/(quilos quadrados) 
SCALE= 3*(10**9) #em quilômetros por pixel
TIME_RESOLUTION= 3600*24*1 #intervalo de tempo, em segundos, em que cada ponto é calculado
WINDOW_HEIGHT= 800
WINDOW_WIDTH= 600

display= pygame.display
draw= pygame.draw
current_time= pygame.time.get_ticks
sleep= pygame.time.wait
canvas= pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
run= True
    
class EventHandler():
    
    def __init__(self):
        self.buffer= []
        self.quit= False
    
    def update(self):
        pygame.event.pump()
        
        self.buffer= pygame.event.get()
        ORDER= {
            pygame.QUIT: self.update_quit}
        
        for stuff in self.buffer:
            print(stuff)
            ORDER.get(stuff.type, self.update_nothing)()
    
    def update_quit(self):
        self.quit= True
        
    def update_nothing(self):
        pass
        
    
class StarDome():

    def __init__(self):
        #generate stars
        starnum= 60
        self.star= []
        
        for num in range(starnum):
            self.star.append( [(random.randint(0, WINDOW_HEIGHT-1), random.randint(0, WINDOW_WIDTH-1)), random.randint(1, 4) ])
    
    def draw(self):
        canvas.fill(color.BLACK)
        for stup in self.star:
            draw.circle(canvas, color.WHITE, stup[0], stup[1])
            
    def update(self):
        None

class Cardinal:
    
    def __init__(self, x, y, z):
        self.x= x
        self.y= y
        self.z= z
        
    def vectorize(self):
        return (self.x**2 + self.y**2 + self.z**2)**(1/2)
    
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
        
        self.tick= 0
        
    def draw(self):
        draw.circle(canvas, color.BLUE, (WINDOW_HEIGHT//2, WINDOW_WIDTH//2), int(self.radius/SCALE))
        #draw.circle(canvas, color.BLUE, (WINDOW_HEIGHT//2, WINDOW_WIDTH//2), 20)
        
    def update(self):
        self.tick+= 1
        self.tick%= 1024
    
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
        
        self.tick= 0
    
    def update(self):
        self.update_position()
        self.update_speed()
        
        self.tick+= 1
        self.tick%= 1024
    
    def update_position(self):
        
        self.position.x+= self.speed.x*TIME_RESOLUTION
        self.position.y+= self.speed.y*TIME_RESOLUTION
        self.position.z+= self.speed.z*TIME_RESOLUTION
        
    def update_speed(self):        
        
        for celestial_body in self.celestial_neighbor:
            
            relative_constant= self.position.vectorize()**3/(GRAVCONST*celestial_body.mass)
            
            self.speed.x-= ( self.position.x/relative_constant )*TIME_RESOLUTION
            self.speed.y-= ( self.position.y/relative_constant )*TIME_RESOLUTION
            self.speed.z-= ( self.position.z/relative_constant )*TIME_RESOLUTION
        
    def add_neighbor(self, celestial_body):
        
        self.celestial_neighbor.append(celestial_body)
        
    def draw(self):
        #draw pulse
        draw.circle(canvas, color.make_transparent(color.BLACK, color.WHITE, 0.5 + (self.tick%64)/128), (int(WINDOW_HEIGHT//2+self.position.x/SCALE), int(WINDOW_WIDTH//2+self.position.y/SCALE)), int(self.radius/SCALE)+int( ((self.tick%64)/2)**0.7 ))
        #draw itself
        draw.circle(canvas, color.WHITE, (int(WINDOW_HEIGHT//2+self.position.x/SCALE), int(WINDOW_WIDTH//2+self.position.y/SCALE)), int(self.radius/SCALE))
        #draw.circle(canvas, color.WHITE, (int(WINDOW_HEIGHT//2+self.position.x/SCALE), int(WINDOW_WIDTH//2+self.position.y/SCALE)), 20)
#

event= EventHandler()

center= CenterBody(1.98855*(10**30), 695700*(10**3)) #dados referentes ao Sol
#orbital= OrbitalBody(405400*(10**3), 959.583333333333333333333, 7.342* (10**22)) #dados referentes à lua
orbital= OrbitalBody(816.04*(10**9), 12.44*(10**3), 1.8986*(10**27), 69911*(10**3)) #dados referentes à jupiter
orbital.add_neighbor(center)
dome= StarDome()
#--MAIN LOOP--
while not event.quit:
    sleep( 20)
    
    event.update()
    
    #update things
    dome.update()
    center.update()
    orbital.update()
    
    #draw things
    dome.draw()
    center.draw()
    orbital.draw()
    
    display.flip()