from cardinal import Cardinal
from celestial_cluster import CelestialCluster
import gsignal
import math


class Perspective():
    position= Cardinal(0,0,0)
    target= None
    tposition= Cardinal(0,0,0)
    cluster= CelestialCluster.cluster
    scale= 3*(10**7) #em metros por pixel
        
    def lock_on( target):
        Perspective.target= target
        Perspective.tposition=Perspective.target.position.copy()
        
    def update():
        RATIO= 8
        position= Perspective.position
        
        position.x+= math.ceil( (Perspective.tposition.x - position.x)/RATIO + (Perspective.target.position.x - Perspective.tposition.x))
        position.y+= math.ceil( (Perspective.tposition.y - position.y)/RATIO + (Perspective.target.position.y - Perspective.tposition.y))
        position.z+= math.ceil( (Perspective.tposition.z - position.z)/RATIO + (Perspective.target.position.z - Perspective.tposition.z))
        
        Perspective.tposition=Perspective.target.position.copy()

    def window(celestial_body):
        from display import MainFrame
        
        x= (MainFrame.WIDTH//2) + (celestial_body.position.x - Perspective.position.x)//Perspective.scale
        y= (MainFrame.HEIGTH//2) - (celestial_body.position.y - Perspective.position.y)//Perspective.scale

        return x, y

    def perceived_size(celestial_body):
        radius= celestial_body.radius//Perspective.scale
        return radius
        
    def read_signal(signal):
        if signal.type == gsignal.ACTION:
            Perspective.lock_on( signal.target )
        elif signal.type == gsignal.SCROLLUP:
            Perspective.scale= int(Perspective.scale**(1.01/1))
        elif signal.type == gsignal.SCROLLDOWN:
            Perspective.scale= int(Perspective.scale**(1/1.01))
        