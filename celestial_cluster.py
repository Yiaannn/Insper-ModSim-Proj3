import gtime
from gcolor import Gcolor
from cardinal import Cardinal
import pygame.draw as draw

GRAVCONST= 6.67*(10**(-11))*(gtime.RESOLUTION**2) #em Newton*(Metro quadrado)/(quilos quadrados)

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
        
    cluster=[]

    def init():
        
        orbital_list= CelestialCluster.SOLARSYS()
        
        for orbital in orbital_list:
            CelestialCluster.include(orbital)

    def update():
        for celestial_body in CelestialCluster.cluster:
            celestial_body.update()
            
    def draw():
        for celestial_body in CelestialCluster.cluster:
            celestial_body.draw()
            
    def event_collision(event):
        print("DEBUG2: Collision")
        
    def include( celestial_body):
        for cluster_body in CelestialCluster.cluster:
            cluster_body.add_neighbor(celestial_body)
            celestial_body.add_neighbor(cluster_body)
        CelestialCluster.cluster.append(celestial_body)
        
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
                
            if distance.vectorize() > self.radius + celestial_body.radius:
                relative_constant= GRAVCONST*celestial_body.mass/(distance.vectorize()**2)
                
                self.speed.x+= relative_constant*distance.x/distance.vectorize()
                self.speed.y+= relative_constant*distance.y/distance.vectorize()
                self.speed.z+= relative_constant*distance.z/distance.vectorize()
            else:
                #aconteceu uma colisão, tratar aqui
                print("DEBUG2: Collision")
                Gevent.push( Gevent.build_event( {
                    "type": Gevent.COLLISION ,
                    "celestial_bodies": [self, celestial_body] } ) )
            
    def add_neighbor(self, celestial_body):
        
        self.celestial_neighbor.append(celestial_body)
        
    def draw(self, display):
        from perspective import Perspective
        
        #draw pulse
        if self.tick%64 >= 32:
            draw.circle(display.CANVAS, self.color.mix(self.color.BLACK, 0.5 + (self.tick%64)/128), Perspective.window(self),  Perspective.perceived_size(self)+int( ((self.tick%64)/2)**0.7 ))
            draw.circle(display.CANVAS, self.color.mix(self.color.BLACK, 0.5 + ((self.tick+32)%64)/128), Perspective.window(self),  Perspective.perceived_size(self)+int( (((self.tick+32)%64)/2)**0.7 ))
        else:
            draw.circle(display.CANVAS, self.color.mix(self.color.BLACK, 0.5 + ((self.tick+32)%64)/128), Perspective.window(self),  Perspective.perceived_size(self)+int( (((self.tick+32)%64)/2)**0.7 ))
            draw.circle(display.CANVAS, self.color.mix(self.color.BLACK, 0.5 + (self.tick%64)/128), Perspective.window(self),  Perspective.perceived_size(self)+int( ((self.tick%64)/2)**0.7 ))
        #draw itself
        draw.circle(display.CANVAS, self.color.get(), Perspective.window(self), Perspective.perceived_size(self))
