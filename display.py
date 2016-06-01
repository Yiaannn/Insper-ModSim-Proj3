import color
import pygame.display

class Label:
    MAX_WIDTH= 120

    def  __init__(self, text, color):
        self.text= text
        self.color= color
        
    def update():
        pass
        #
    def draw():
        pass
        
class Display:
    WIDTH= 1000
    HEIGTH= 600
    CANVAS= pygame.display.set_mode( (WIDTH, HEIGTH) )

    def update():
        Display.CANVAS.fill(color.BLACK)
        MainFrame.update()
        Sidebar.update()
        pygame.display.flip()
     
class MainFrame:

    WIDTH= 800
    HEIGTH= Display.HEIGTH
    CANVAS= Display.CANVAS.subsurface( (0, 0), (WIDTH-1, HEIGTH-1) )

    drawable=[]

    def update():
        for thing in MainFrame.drawable:
            thing.draw(MainFrame)

class Sidebar:
    WIDTH= 200
    HEIGTH= Display.HEIGTH
    CANVAS= Display.CANVAS.subsurface( (MainFrame.WIDTH, 0), (WIDTH-1, HEIGTH-1) )
    MENU= [
        Label("Camera", color.EARTH) ,
        Label("Create", color.VENUS) ,
        Label("Erase", color.MARS) ,
        Label("Graph", color.SUN) ,
        Label("Save", color.NEPTUNE) ]
        
    def update():
        Sidebar.CANVAS.fill(color.WHITE)
        
    def __init__(self):
        canvas = None#??
        label= MENU

    def event_mouse():
        #detectar em que 
        pass