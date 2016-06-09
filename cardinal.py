class Cardinal:
    
    def __init__(self, x, y, z):
        self.x= x
        self.y= y
        self.z= z
		
    def vectorize(self):
        return (self.x**2 + self.y**2 + self.z**2)**(1/2)
        
    def copy(self):
        return Cardinal(self.x, self.y, self.z)