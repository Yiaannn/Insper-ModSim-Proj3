# -*- coding: utf-8 -*-
"""
Created on Wed May 18 17:13:14 2016

@author: Alexandre Young
"""

import pygame
import random
import color
import math

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

'''
equaçoes de colisão(2D):
Vf * cos{angulo final} *(m1 + m2) = m1 * v1 + m2 * v2 * cos{angulo entre obj1 e obj2}
Vf * sin{angulo final} *(m1 + m2) = m2 * v2 *sin{angulo entre obj1 e obj2}


Algebra:
Vf  = m1 * v1 + m2 * v2 * cos{angulo entre obj1 e obj2} / (cos{angulo final} *(m1 + m2))

sin{angulo final} = m2 * v2 *sin{angulo entre obj1 e obj2} / (m1 * v1 + m2 * v2 * cos{angulo entre obj1 e obj2} / (cos{angulo final} *(m1 + m2)) *(m1 + m2)) 


'''

def colisão_2D(orbi_1,orbi_2,angulo):
    m1 = orbi_1.mass
    v1 =(orbi_1.speed.x**2 + orbi_1.speed.y**2) **(1/2)
    v1 = math.fabs(v1)
    
    m2 = orbi_2.mass
    v2 =(orbi_2.speed.x**2 + orbi_2.speed.y**2) **(1/2)
    v2 = math.fabs(v2)
    
        
    angulo_final_SemSin = m2 * v2 * math.sin(angulo)/ ((m1 * v1 + m2 * v2 * math.cos(angulo))/ (math.cos(angulo) * (m1 + m2)) *(m1 + m2)) 
    angulo_final = math.sin(angulo_final_SemSin)
    
    Vf = m1 * v1 + m2 * v2 * math.cos(angulo) / (math.cos(angulo_final) *(m1 + m2))

    return Vf,angulo_final
    
def distancia(orbi_a,orbi_b):
    dist = math.sqrt(((orbi_a.position.x - orbi_b.position.x)**2) + ((orbi_a.position.x - orbi_b.position.x) **2))
    return math.fabs(dist)
    
    
class EventHandler():
    
    def __init__(self):
        self.buffer= []
        self.quit= False
    
    def update(self):
        pygame.event.pump()
        
        self.buffer= pygame.event.get()
        ORDER= {
            pygame.MOUSEBUTTONDOWN: self.update_mouse,
            pygame.QUIT: self.update_quit}
        
        for stuff in self.buffer:
            if stuff.type in ORDER:
               ORDER[stuff.type](stuff)
    
    def update_mouse(self, stuff):
        global SCALE
        
        if stuff.button == 4:
            SCALE**=(1/1.001)
        elif stuff.button == 5:
            SCALE**=(1.001)
    
    def update_quit(self, stuff):
        self.quit= True

class CelestialCluster():
    #"KEY": (distance, speed, mass, radius)
    EARTHSYS= lambda: (
        [CelestialBody( 0, 0, 5.97237*(10**24), 6.371*(10**3))], #EARTH
        [CelestialBody(405400*(10**3) , 959.583333333333333333333, 7.342* (10**22), 1737.1*(10**3)) ]) #MOON
    
    SOLARSYS= lambda: (
        [CelestialBody(0, 0, 1.98855*(10**30), 695700*(10**3))], #SUN
        [CelestialBody(816.04*(10**9), 12.44*(10**3), 1.8986*(10**27), 69911*(10**3)) ]) #JUPITER        
    
    def __init__(self):
        #self.cluster= []
        
        self.cluster, orbital_list= CelestialCluster.EARTHSYS()
        
        for orbital in orbital_list:
            self.include(orbital)
            
    def update(self):
        for celestial_body in self.cluster:
            celestial_body.update()
        print(self.cluster[0].position.x)
            
    def draw(self):
        for celestial_body in self.cluster:
            celestial_body.draw()
        
    def include(self, celestial_body):
        for cluster_body in self.cluster:
            cluster_body.add_neighbor(celestial_body)
            celestial_body.add_neighbor(cluster_body)
        self.cluster.append(celestial_body)
    
class StarDome():

    def __init__(self):
        #generate stars
        starnum= 42000
        self.star= []
        
        for num in range(starnum):
            self.star.append( [(random.randint(0, WINDOW_HEIGHT-1), random.randint(0, WINDOW_WIDTH-1)), random.randint(3, 6) ])
    
    def draw(self):
        canvas.fill(color.WHITE)
        for stup in self.star:
            draw.circle(canvas, color.BLACK, stup[0], stup[1])
            
    def update(self):
        None

class Cardinal:
    
    def __init__(self, x, y, z):
        self.x= x
        self.y= y
        self.z= z
        
    def vectorize(self):
        return (self.x**2 + self.y**2 + self.z**2)**(1/2)
    
class CelestialBody:
    
    def __init__(self, position, speed, mass, radius):
        #distance é dada em metros
        #speed em metros por segundo
        #mass em quilos
        
        self.position= Cardinal(position, 0, 0)
        self.speed= Cardinal(0, speed, 0)
        self.mass= mass
        self.radius= radius
        
        self.celestial_neighbor= []
        
        self.tick= 0
        
        self.lista_dis = []
    
    def update(self):
        self.update_speed()
        self.update_position()
        
        self.tick+= 1
        self.tick%= 1024
    
    def update_position(self):
        
        self.position.x+= self.speed.x*TIME_RESOLUTION
        self.position.y+= self.speed.y*TIME_RESOLUTION
        self.position.z+= self.speed.z*TIME_RESOLUTION
        
    def update_speed(self):        
        
        for celestial_body in self.celestial_neighbor:
            
            distance= Cardinal(
                self.position.x - celestial_body.position.x,
                self.position.y - celestial_body.position.y,
                self.position.z - celestial_body.position.z)
                
            relative_constant= distance.vectorize()**3/(GRAVCONST*celestial_body.mass)
            self.speed.x+= ( distance.x/relative_constant )*TIME_RESOLUTION
            self.speed.y+= ( distance.y/relative_constant )*TIME_RESOLUTION
            self.speed.z+= ( distance.z/relative_constant )*TIME_RESOLUTION
        
    def add_neighbor(self, celestial_body):
        
        self.celestial_neighbor.append(celestial_body)
        
    def draw(self):
        #draw pulse
        draw.circle(canvas, color.make_transparent(color.BLACK, color.WHITE, 0.5 + (self.tick%64)/128), (int(WINDOW_HEIGHT//2+self.position.x/SCALE), int(WINDOW_WIDTH//2+self.position.y/SCALE)), int(self.radius/SCALE)+int( ((self.tick%64)/2)**0.7 ))
        #draw itself
        draw.circle(canvas, color.WHITE, (int(WINDOW_HEIGHT//2+self.position.x/SCALE), int(WINDOW_WIDTH//2+self.position.y/SCALE)), int(self.radius/SCALE))
        #draw.circle(canvas, color.WHITE, (int(WINDOW_HEIGHT//2+self.position.x/SCALE), int(WINDOW_WIDTH//2+self.position.y/SCALE)), 20)
#

def summon_asteroid():

    speed= None
    mass= None
    RADIUS= None
    #asteroid= OrbitalBody(position, speed, mass, RADIUS)

event= EventHandler()

dome= StarDome()
celestial_cluster= CelestialCluster()
#--MAIN LOOP--
while not event.quit:
    sleep( 20)
    
    event.update()
    
    #update things
    dome.update()
    celestial_cluster.update()
    
    #draw things
    dome.draw()
    celestial_cluster.draw()
    
    display.flip()