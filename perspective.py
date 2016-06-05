from cardinal import Cardinal
from display import MainFrame

class Perspective():

    def __init__(self, cluster):
        self.cluster= cluster
        self.position= Cardinal(0, 0, 0)
        self.scale= 3*(10**7) #em quilômetros por pixel
        
        self.lock_on(cluster[0])
        
    def lock_on(self, new_lock):
        self.position= new_lock.position

    def window(self, celestial_body):

        x= (MainFrame.WIDTH//2) + (celestial_body.position.x - self.position.x)//self.scale
        y= (MainFrame.HEIGTH//2) - (celestial_body.position.y - self.position.y)//self.scale

        return x, y

    def perceived_size(self, celestial_body):
        radius= celestial_body.radius//self.scale
        return radius
        