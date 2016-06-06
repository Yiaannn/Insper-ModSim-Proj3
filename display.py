from gcolor import Gcolor
from panel import Panel
import pygame.display
import pygame.draw
        
class Display:
    WIDTH= 1600
    HEIGTH= 900
    CANVAS= pygame.display.set_mode( (WIDTH, HEIGTH) )

    def update():
        Display.CANVAS.fill(Gcolor.BLACK)
        MainFrame.update()
        Sidebar.update()
        pygame.display.flip()
        
    def event_mouse(etype, position):
    
        if position[0] > (Display.WIDTH - Sidebar.WIDTH):
            position[0]-= (Display.WIDTH - Sidebar.WIDTH)
            Sidebar.event_mouse(etype, position)
        
     
class MainFrame:

    WIDTH= Display.WIDTH
    HEIGTH= Display.HEIGTH
    CANVAS= Display.CANVAS.subsurface( (0, 0), (WIDTH, HEIGTH) )

    drawable=[]

    def update():
        for thing in MainFrame.drawable:
            thing.draw(MainFrame)

class Sidebar:
    WIDTH= Panel.WIDTH
    HEIGTH= Panel.HEIGTH
    CANVAS= Display.CANVAS.subsurface( (Display.WIDTH - WIDTH, 0), (WIDTH, HEIGTH) )
    MENU= [
        Panel(CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Camera", Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.EARTH, 0.7), 0.7) ), 0) ,
        Panel(CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Create", Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.VENUS, 0.7), 0.7) ), 1) ,
        Panel(CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Erase", Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.MARS, 0.7), 0.7) ), 2) ,
        Panel(CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Graph",  Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.SUN, 0.7), 0.7) ), 3) ,
        Panel(CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Save", Gcolor( Gcolor.darken( Gcolor.chill(Gcolor.NEPTUNE, 0.7), 0.7) ), 4) ]
    active_panel= None
        
    def update():
        Sidebar.active_panel= None
        for panel in Sidebar.MENU:
            panel.update()
            if panel.active or panel.busy:
                Sidebar.active_panel= panel
        
        if Sidebar.active_panel != None:
            Sidebar.active_panel.draw()
            
    def event_mouse(etype, position):
        if not Sidebar.active_panel:
            panel_index= position[1]//Panel.BANNER_HEIGTH
            
            if panel_index < len(Sidebar.MENU):
               Sidebar.MENU[panel_index].event_mouse(etype, position)
        else:
            Sidebar.active_panel.event_mouse(etype, position)