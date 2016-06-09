import gtime
from gcolor import Gcolor
from cardinal import Cardinal
import gsignal
import pygame.draw as draw

GRAVCONST= 6.67*(10**(-11)) #em Newton*(Metro quadrado)/(quilos quadrados)

class CelestialCluster():
    #"KEY": (name, distance, speed, mass, radius, color)
    #note que a velocidade [e relativa ao ponto da órbita indicado, caso haja nota do contrário assuma que a distância é dada no afélio da órbita, com a velocidade nesse ponto (velocidade orbital mínima)
    #EARTHSYS= lambda: (
    #    CelestialBody( 0, 0*gtime.RESOLUTION, 5.97237*(10**24), 6.371*(10**3), gcolor.EARTH) ,
    #    CelestialBody(405400*(10**3) , 959.583333333333333333333*gtime.RESOLUTION, 7.342* (10**22), 1737.1*(10**3), gcolor.WHITE) )

    SOLARSYS= lambda: (
        CelestialBody("Sun", 0, 0, 1988500*(10**24), 695700*(10**3), Gcolor(Gcolor.SUN) ) ,
        CelestialBody("Mercury", 69.82*(10**9), 38.7*(10**3), 0.33011*(10**24), 2439.9*(10**3), Gcolor(Gcolor.MERCURY) ) ,
        CelestialBody("Venus", 108.94*(10**9), 34.74*(10**3), 4.8675*(10**24), 6051.8*(10**3), Gcolor(Gcolor.VENUS) ) ,
        CelestialBody("Earth", 152.10*(10**9), 29.29*(10**3), 5.9723*(10**24), 6371.0*(10**3), Gcolor(Gcolor.EARTH) ) ,
        CelestialBody("Mars", 249.23*(10**9), 21.97*(10**3), 0.64171*(10**24), 3389.5*(10**3), Gcolor(Gcolor.MARS) ) ,
        CelestialBody("Jupiter", 816.04*(10**9), 12.44*(10**3), 1.8986*(10**24), 69911*(10**3), Gcolor(Gcolor.JUPITER) ) ,
        CelestialBody("Saturn", 1514.5*(10**9), 9.09*(10**3), 568.34*(10**24), 58232*(10**3), Gcolor(Gcolor.SATURN) ) ,
        CelestialBody("Uranus", 3003.62*(10**9), 6.49*(10**3), 86.813*(10**24), 25362*(10**3), Gcolor(Gcolor.URANUS) ) ,
        CelestialBody("Neptune", 4545.67*(10**9), 5.37*(10**3), 102.413*(10**24), 24622*(10**3), Gcolor(Gcolor.NEPTUNE) ) )
        
    cluster=[]
    watchlist=[None, None, None] #[string, celestial_body, celestial_body]
    listener= None
    word_list=["Distance", "Relative Speed"]
    
    def load(sysname):
        
        if sysname == "Solar":
            orbital_list= CelestialCluster.SOLARSYS()
        elif sysname == "Earth - Moon":
            orbital_list= CelestialCluster.EARTHSYS()
        
        
        for orbital in orbital_list:
            CelestialCluster.include(orbital)
            
    def init():
        
        orbital_list= CelestialCluster.SOLARSYS()
        
        for orbital in orbital_list:
            CelestialCluster.include(orbital)

    def update():
        for celestial_body in CelestialCluster.cluster:
            celestial_body.update()
            
        if not None in CelestialCluster.watchlist and CelestialCluster.listener:
            CelestialCluster.watch()
            
    def watch():
        VECTOR= CelestialCluster.watchlist[0]
        CBODY1= CelestialCluster.watchlist[1]
        CBODY2= CelestialCluster.watchlist[2]
        
        if VECTOR == "Distance":
            value= CelestialCluster.distance(CBODY1, CBODY2)
            signal= gsignal.build( {
                "type": gsignal.ACTION ,
                "content": value } )
        
        CelestialCluster.listener.read_signal(signal)
        
    def distance(cbody1, cbody2):
        distance= Cardinal(
            cbody1.position.x - cbody2.position.x ,
            cbody1.position.y - cbody2.position.y ,
            cbody1.position.z - cbody2.position.z )
        
        return distance.vectorize()
        
    def draw():
        for celestial_body in CelestialCluster.cluster:
            celestial_body.draw()
            
    def read_signal(signal):
        if signal.type == gsignal.WATCH1:
            CelestialCluster.watchlist[1]= signal.target
            if CelestialCluster.listener:
                signal= gsignal.build( {
                    "type": gsignal.RESET ,
                    "content": CelestialCluster.watchlist[0] } )
                CelestialCluster.listener.read_signal(signal)
        elif signal.type == gsignal.WATCH2:
            CelestialCluster.watchlist[2]= signal.target
            if CelestialCluster.listener:
                signal= gsignal.build( {
                    "type": gsignal.RESET ,
                    "content": CelestialCluster.watchlist[0] } )
                CelestialCluster.listener.read_signal(signal)
        elif signal.type == gsignal.WATCH0:
            CelestialCluster.watchlist[0]= signal.target
            if CelestialCluster.listener:
                signal= gsignal.build( {
                    "type": gsignal.RESET ,
                    "content": CelestialCluster.watchlist[0] } )
                CelestialCluster.listener.read_signal(signal)
            
        elif signal.type == gsignal.COLLISION:
            pass
            #TODO tratar colisão
            
        elif signal.type == gsignal.DELETE:
            CelestialCluster.remove(signal.content)
            
        else:
            print("possible error at celestialcluster")
            
    def set_listener(listener):
        CelestialCluster.listener= listener
        if not None in CelestialCluster.watchlist:
            signal= gsignal.build( {
                "type": gsignal.RESET ,
                "content": CelestialCluster.watchlist[0] } )
            CelestialCluster.listener.read_signal(signal)
        
    def include( celestial_body):
        for cluster_body in CelestialCluster.cluster:
            cluster_body.add_neighbor(celestial_body)
            celestial_body.add_neighbor(cluster_body)
        CelestialCluster.cluster.append(celestial_body)
        
    def remove( celestial_body):
        for cluster_body in CelestialCluster.cluster:
            if cluster_body != celestial_body:
                cluster_body.remove_neighbor(celestial_body)
        CelestialCluster.cluster.remove(celestial_body)
        
class CelestialBody:

    def __init__(self, name, position, speed, mass, radius, color):
        #distance é dada em metros
        #speed em metros por segundo
        #mass em quilos
        
        self.name= name
        self.position= Cardinal(int(position), 0, 0)
        self.speed= Cardinal(0, speed, 0)
        self.mass= int(mass)
        self.radius= int(radius)
        self.color= color

        self.celestial_neighbor= []

        self.tick= 0

        self.lista_dis = []
        
    def __str__(self):
    
        return self.name

    def update(self):
        self.update_speed()
        self.update_position()

        self.tick+= 1
        self.tick%= 1024

    def update_position(self):

        self.position.x+= int(self.speed.x*gtime.RESOLUTION)
        self.position.y+= int(self.speed.y*gtime.RESOLUTION)
        self.position.z+= int(self.speed.z*gtime.RESOLUTION)

    def update_speed(self): 
        #print( type(self.speed.x) )

        for celestial_body in self.celestial_neighbor:

            distance= Cardinal(
                celestial_body.position.x - self.position.x ,
                celestial_body.position.y - self.position.y ,
                celestial_body.position.z - self.position.z )
                
            relative_speed= Cardinal(
                celestial_body.speed.x - self.speed.x ,
                celestial_body.speed.y - self.speed.y ,
                celestial_body.speed.z - self.speed.z )
                
            #if distance.vectorize() > self.radius + celestial_body.radius:
            if distance.vectorize() > ( self.radius + celestial_body.radius ) + relative_speed.vectorize()*gtime.RESOLUTION:
                #Não tou muito confiante nessa checagem de colisão, mas ok
                relative_constant= GRAVCONST*celestial_body.mass/(distance.vectorize()**2)
                
                self.speed.x+= relative_constant*distance.x*gtime.RESOLUTION/distance.vectorize()
                self.speed.y+= relative_constant*distance.y*gtime.RESOLUTION/distance.vectorize()
                self.speed.z+= relative_constant*distance.z*gtime.RESOLUTION/distance.vectorize()
            else:
                #aconteceu uma colisão, tratar aqui
                #print("DEBUG2: Collision")
                CelestialCluster.read_signal( gsignal.build( {
                    "type": gsignal.COLLISION ,
                    "celestial_bodies": [self, celestial_body] } ) )
            
    def add_neighbor(self, celestial_body):
        self.celestial_neighbor.append(celestial_body)
        
    def remove_neighbor(self, celestial_body):
        self.celestial_neighbor.remove(celestial_body)
        
    def draw(self, display):
        from perspective import Perspective
        
        size= Perspective.perceived_size(self)
        if size < 3:
            size= 3
        
        #draw pulse
        if self.tick%128 >= 64:
            draw.circle(display.CANVAS, self.color.mix(self.color.BLACK, ((self.tick%128))**2/(128**2)), Perspective.window(self),  size+int( ((self.tick%128)/32)))
            draw.circle(display.CANVAS, self.color.mix(self.color.BLACK, (((self.tick+64)%128))**2/(128**2)), Perspective.window(self),  size+int( (((self.tick+64)%128)/32)))
        else:
            draw.circle(display.CANVAS, self.color.mix(self.color.BLACK, (((self.tick+64)%128)**2)/(128**2)), Perspective.window(self),  size+int( (((self.tick+64)%128)/32)))
            draw.circle(display.CANVAS, self.color.mix(self.color.BLACK, ((self.tick%128) )**2/(128**2)), Perspective.window(self),  size+int( ((self.tick%128)/32)))
        #draw itself
        draw.circle(display.CANVAS, self.color.get(), Perspective.window(self), Perspective.perceived_size(self))
