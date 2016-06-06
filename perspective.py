from cardinal import Cardinal
from celestial_cluster import CelestialCluster
from gevent import Gevent


class Perspective():
    position= Cardinal(0, 0, 0)
    cluster= CelestialCluster.cluster
    scale= 3*(10**7) #em metros por pixel
        
    def lock_on( new_lock):
        Perspective.position= new_lock.position

    def window(celestial_body):
        from display import MainFrame
        
        x= (MainFrame.WIDTH//2) + (celestial_body.position.x - Perspective.position.x)//Perspective.scale
        y= (MainFrame.HEIGTH//2) - (celestial_body.position.y - Perspective.position.y)//Perspective.scale

        return x, y

    def perceived_size(celestial_body):
        radius= celestial_body.radius//Perspective.scale
        return radius
        
    def event_mouse(event):
        if event.type == Gevent.SCROLLUP:
            Perspective.scale= int(Perspective.scale**(1.01/1))
        else:
            Perspective.scale= int(Perspective.scale**(1/1.01))
        