import pygame
import random
from gcolor import Gcolor
import gtime
from perspective import Perspective
from cardinal import Cardinal
import math
from display import MainFrame
from display import Display

import os
from graficos import grafico

GRAVCONST= 6.67*(10**(-11))*(gtime.RESOLUTION**2) #em Newton*(Metro quadrado)/(quilos quadrados)
draw= pygame.draw

'''
equaçoes de colisão(2D):
Vf * cos{angulo final} *(m1 + m2) = m1 * v1 + m2 * v2 * cos{angulo entre obj1 e obj2}
Vf * sin{angulo final} *(m1 + m2) = m2 * v2 *sin{angulo entre obj1 e obj2}


Algebra:
Vf  = m1 * v1 + m2 * v2 * cos{angulo entre obj1 e obj2} / (cos{angulo final} *(m1 + m2))

sin{angulo final} = m2 * v2 *sin{angulo entre obj1 e obj2} / (m1 * v1 + m2 * v2 * cos{angulo entre obj1 e obj2} / (cos{angulo final} *(m1 + m2)) *(m1 + m2)) 


'''
def colisão_2D_a(orbi_1,orbi_2):

    m1 = orbi_1.mass
    v1 =(orbi_1.speed.x**2 + orbi_1.speed.y**2) **(1/2)
    v1 = math.fabs(v1)

    m2 = orbi_2.mass
    v2 =(orbi_2.speed.x**2 + orbi_2.speed.y**2) **(1/2)
    v2 = math.fabs(v2)
    
    angulo = (((orbi_1.speed.x * orbi_2.speed.x) + (orbi_1.speed.y * orbi_2.speed.y)) / (math.sqrt((orbi_1.speed.x ** 2) * (orbi_1.speed.y ** 2)) * (math.sqrt((orbi_1.speed.y ** 2) * (orbi_1.speed.y ** 2)))))
    angulo = math.cos(angulo)

    angulo_final_SemSin = m2 * v2 * math.sin(angulo)/ ((m1 * v1 + m2 * v2 * math.cos(angulo))/ (math.cos(angulo) * (m1 + m2)) *(m1 + m2)) 
    angulo_final = math.sin(angulo_final_SemSin)

    Vf = m1 * v1 + m2 * v2 * math.cos(angulo) / (math.cos(angulo_final) *(m1 + m2))

    return Vf,angulo_final
    
def distancia(orbi_a,orbi_b):
    dist = math.sqrt(((orbi_a.position.x - orbi_b.position.x)**2) + ((orbi_a.position.y - orbi_b.position.y) **2))
    return math.fabs(dist)
    
def distancia_2_planetas(cluster,orbi_1,orbi_2):
    try:
        for planet in cluster:
            if planet.color == orbi_1:
                planeta_1 = planet
#                print(planeta_1)
                
            if planet.color == orbi_2:
                planeta_2 = planet
#                print(planeta_2)
                
        return distancia(planeta_1,planeta_2)
    except:
        print('planeta não encontrado')
    
    
class EventHandler():

    def __init__(self, perspective):
        self.perspective= perspective
        self.buffer= []
        self.quit= False

    def update(self):
        pygame.event.pump()
        
        self.buffer= pygame.event.get()
        ORDER= {
            pygame.MOUSEBUTTONDOWN: self.update_mouse,
            pygame.QUIT: self.update_quit}
        
        Display.event_mouse("move", list(pygame.mouse.get_pos()))
        
        for stuff in self.buffer:
            if stuff.type in ORDER:
               ORDER[stuff.type](stuff)

    def update_mouse(self, stuff):
        if stuff.button == 1:
            Display.event_mouse("click", list(pygame.mouse.get_pos()))
        elif stuff.button == 4:
            perspective.scale= int(perspective.scale**(1/1.01))
        elif stuff.button == 5:
            perspective.scale= int(perspective.scale**(1.01/1))

    def update_quit(self, stuff):
        self.quit= True

class CelestialCluster():
    #"KEY": (distance, speed, mass, radius, color)
    #note que a velocidade [e relativa ao ponto da órbita indicado, caso haja nota do contrário assuma que a distância é dada no afélio da órbita, com a velocidade nesse ponto (velocidade orbital mínima)
    #EARTHSYS= lambda: (
    #    CelestialBody( 0, 0*gtime.RESOLUTION, 5.97237*(10**24), 6.371*(10**3), gcolor.EARTH) ,
    #    CelestialBody(405400*(10**3) , 959.583333333333333333333*gtime.RESOLUTION, 7.342* (10**22), 1737.1*(10**3), gcolor.WHITE) )

    SOLARSYS= lambda: (
        CelestialBody(0, 0*gtime.RESOLUTION, 1988500*(10**24), 695700*(10**3), Gcolor(Gcolor.SUN) ) ,
        CelestialBody(69.82*(10**9), 38.7*(10**3)*gtime.RESOLUTION, 0.33011*(10**24), 2439.9*(10**3), Gcolor(Gcolor.MERCURY) ) ,
        CelestialBody(108.94*(10**9), 34.74*(10**3)*gtime.RESOLUTION, 4.8675*(10**24), 6051.8*(10**3), Gcolor(Gcolor.VENUS) ) ,
        CelestialBody(152.10*(10**9), 29.29*(10**3)*gtime.RESOLUTION, 5.9723*(10**24), 6371.0*(10**3), Gcolor(Gcolor.EARTH) ) ,
        CelestialBody(249.23*(10**9), 21.97*(10**3)*gtime.RESOLUTION, 0.64171*(10**24), 3389.5*(10**3), Gcolor(Gcolor.MARS) ) ,
        CelestialBody(816.04*(10**9), 12.44*(10**3)*gtime.RESOLUTION, 1.8986*(10**24), 69911*(10**3), Gcolor(Gcolor.JUPITER) ) ,
        CelestialBody(1514.5*(10**9), 9.09*(10**3)*gtime.RESOLUTION, 568.34*(10**24), 58232*(10**3), Gcolor(Gcolor.SATURN) ) ,
        CelestialBody(3003.62*(10**9), 6.49*(10**3)*gtime.RESOLUTION, 86.813*(10**24), 25362*(10**3), Gcolor(Gcolor.URANUS) ) ,
        CelestialBody(4545.67*(10**9), 5.37*(10**3)*gtime.RESOLUTION, 102.413*(10**24), 24622*(10**3), Gcolor(Gcolor.NEPTUNE) ) )

    def __init__(self):
        self.cluster= []
        
        orbital_list= CelestialCluster.SOLARSYS()
        
        for orbital in orbital_list:
            self.include(orbital)
            
    def update(self):
        for celestial_body in self.cluster:
            celestial_body.update()
            
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
        starnum= 30000
        self.star= []

        for num in range(starnum):
            self.star.append( [(random.randint(0, MainFrame.HEIGTH-1), random.randint(0, MainFrame.WIDTH-1)), random.randint(3, 8) ])

    def draw(self):
        canvas.fill(Gcolor.WHITE)
        for stup in self.star:
            draw.circle(MainFrame.CANVAS, Gcolor.BLACK, stup[0], stup[1])
            
    def update(self):
        pass

class CelestialBody:

    def __init__(self, position, speed, mass, radius, color):
        #distance é dada em metros
        #speed em metros por segundo
        #mass em quilos

        self.position= Cardinal(int(position), 0, 0)
        self.speed= Cardinal(0, speed, 0)
        self.mass= int(mass)
        self.radius= int(radius)
        self.color= color

        self.celestial_neighbor= []

        self.tick= 0

        self.lista_dis = []

    def update(self):
        self.update_speed()
        self.update_position()

        self.tick+= 1
        self.tick%= 1024

    def update_position(self):

        self.position.x+= int(self.speed.x)#*gtime.RESOLUTION
        self.position.y+= int(self.speed.y)#*gtime.RESOLUTION
        self.position.z+= int(self.speed.z)#*gtime.RESOLUTION

    def update_speed(self): 
        #print( type(self.speed.x) )

        for celestial_body in self.celestial_neighbor:

            distance= Cardinal(
                celestial_body.position.x - self.position.x ,
                celestial_body.position.y - self.position.y ,
                celestial_body.position.z - self.position.z )
                
            #relative_constant= int(distance.vectorize()**3/(GRAVCONST*celestial_body.mass))
            #self.speed.x+= ( distance.x*gtime.RESOLUTION)//relative_constant
            #self.speed.y+= ( distance.y*gtime.RESOLUTION)//relative_constant
            #self.speed.z+= ( distance.z*gtime.RESOLUTION)//relative_constant
            relative_constant= GRAVCONST*celestial_body.mass/(distance.vectorize()**2)
            #print(relative_constant*distance.x/distance.vectorize())
            self.speed.x+= relative_constant*distance.x/distance.vectorize()
            self.speed.y+= relative_constant*distance.y/distance.vectorize()
            self.speed.z+= relative_constant*distance.z/distance.vectorize()
            
    def add_neighbor(self, celestial_body):
        
        self.celestial_neighbor.append(celestial_body)
        
    def draw(self, display):
        #draw pulse
        draw.circle(display.CANVAS, self.color.mix(self.color.BLACK, 0.5 + (self.tick%64)/128), perspective.window(self),  perspective.perceived_size(self)+int( ((self.tick%64)/2)**0.7 ))
        
        #draw itself
        draw.circle(display.CANVAS, self.color.get(), perspective.window(self), perspective.perceived_size(self))

def summon_asteroid():

    speed= None
    mass= None
    RADIUS= None
    #asteroid= OrbitalBody(position, speed, mass, RADIUS)
dome= StarDome()
celestial_cluster= CelestialCluster()

MainFrame.drawable= celestial_cluster.cluster
perspective= Perspective(celestial_cluster.cluster)
event= EventHandler(perspective)
distancia_corpos = []

os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 0"
#--MAIN LOOP--


while not event.quit:
    gtime.sleep(10)
    
    #capture events
    event.update()
    gtime.update()

    #update things
    celestial_cluster.update()

    #draw things
    Display.update()
    
    #print(distancia_corpos)
    #grafico(ticks,distancia_corpos,gtime.RESOLUTION)
    #distancia_corpos.append(distancia_2_planetas(celestial_cluster.cluster,color.EARTH,color.SUN))