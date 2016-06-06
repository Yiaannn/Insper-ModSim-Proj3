# -*- coding: utf-8 -*-

import random
from gcolor import Gcolor
import gtime
from perspective import Perspective
from cardinal import Cardinal
from celestial_cluster import CelestialCluster
from syscomm import SysComm
from display import Display
import os
from graficos import grafico

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
        for planet in CelestialCluster.cluster:
            if planet == orbi_1:
                planeta_1 = planet
#                print(planeta_1)
                
            if planet == orbi_2:
                planeta_2 = planet
#                print(planeta_2)
                
        return distancia(planeta_1,planeta_2)
    except:
        print('erro')

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

def summon_asteroid():

    speed= None
    mass= None
    RADIUS= None
    #asteroid= OrbitalBody(position, speed, mass, RADIUS)
    
#dome= StarDome()
CelestialCluster.init()
Perspective.lock_on(CelestialCluster.cluster[1])

distancia_corpos = []

os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 0"
#--MAIN LOOP--



while not SysComm.quit:
    current_time= gtime.current()
    
    #update system interface
    SysComm.update()
    
    #update things
    CelestialCluster.update()

    #draw things
    Display.update()
    
    gtime.update()
    elapsed_time= gtime.current()-current_time
    if elapsed_time < 16:
        gtime.sleep( 16 - elapsed_time)
    
    #print(distancia_corpos)
    #grafico(ticks,distancia_corpos,gtime.RESOLUTION)
    distancia_corpos.append(distancia_2_planetas(CelestialCluster.cluster,CelestialCluster.cluster[3],CelestialCluster.cluster[0]))
    print (distancia_corpos)
    
print ('final')