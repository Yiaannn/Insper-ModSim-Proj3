from gcolor import Gcolor
import gtime
import pygame.display
import pygame.draw
import pygame.font

pygame.font.init()
#print(pygame.font.get_fonts())

class Banner():
    WIDTH= 260
    HEIGTH= 60
    STRAP_WIDTH= 20
    FONT= pygame.font.SysFont('verdana',  42)

    def  __init__(self, text, color, canvas):
        self.color= color
        self.canvas= canvas
        self.text=text
        
        #draw strap
        pygame.draw.rect(self.canvas, self.color.burn( 0.9), ( (0, 0), (Banner.STRAP_WIDTH, Banner.HEIGTH) ) )
                
        #draw main
        pygame.draw.rect(self.canvas, self.color.get(), ( (Banner.STRAP_WIDTH, 0), (Banner.WIDTH-Banner.STRAP_WIDTH, Banner.HEIGTH) ) )
        self.canvas.blit(self.text, (Banner.STRAP_WIDTH, 0) )
        

class Panel:
    WIDTH= Banner.WIDTH
    HEIGTH= 900
    MAX_TICK= 20
    MAX_TICK2= 20
    def __init__(self, canvas, ptype, color, index):
        
        self.canvas= canvas
        self.ptype= ptype
        self.color= color
        self.text=  Banner.FONT.render(ptype, True, self.color.mix(self.color.WHITE, 0.8))
        self.index= index
        self.banner= Banner(self.text, self.color, pygame.Surface((Banner.WIDTH, Banner.HEIGTH) ) )
        
        self.active= False
        self.mouse_over= False
        self.busy= False
        self.tick= 0
        self.tick2= 0
        
    def event_mouse(self, etype, position):
        if not self.busy:
            if not self.active:
                if etype == "move":
                    self.mouse_over= True
                    
                elif etype == "click":
                    self.busy= True
                    
            else:
                if etype == "move":
                    if position[0] < self.banner.WIDTH:
                        self.mouse_over= True
                        
                if etype == "click":
                    if position[0] >= self.banner.WIDTH:
                        #detectar em que widget do menu eu cliquei
                        #passar o controle pra esse widget
                        pass
                    else:
                        self.busy= True
    
    def update(self):
        
        if self.active:
            if self.busy == False:
                pass
            
            else:
                pass
        
        else:
            if self.busy == False:
                if self.mouse_over and self.tick != self.MAX_TICK:
                    self.tick+=1
                elif not self.mouse_over and self.tick!= 0:
                    self.tick-=1
                    
            else:
                if self.tick != self.MAX_TICK:
                    self.tick+=1
                elif self.tick2 != self.MAX_TICK2:
                    self.tick2+= 1
                else:
                    self.busy= False
                    self.active= True
        
        self.mouse_over= False
        self.draw()
    
    def draw(self):
        gamma=1/2
    
        if self.active:
            pygame.draw.rect(self.canvas, self.color.get(), ( (self.banner.STRAP_WIDTH, 0), (Panel.WIDTH-self.banner.STRAP_WIDTH, Panel.HEIGTH) ) )
            
        else:
            #draw banner
            offset= (self.banner.WIDTH-Banner.STRAP_WIDTH) - (self.tick**gamma)*(self.banner.WIDTH-Banner.STRAP_WIDTH)//(self.MAX_TICK**gamma)
            self.canvas.blit(self.banner.canvas, (offset, self.index*self.banner.HEIGTH))
            
            if self.busy:
                #offset=
                pass
        
        
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
    
        if position[0] > (Display.WIDTH - Banner.WIDTH):
            position[0]-= (Display.WIDTH - Banner.WIDTH)
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
    HEIGTH= Display.HEIGTH
    CANVAS= Display.CANVAS.subsurface( (Display.WIDTH - WIDTH, 0), (WIDTH, HEIGTH) )
    MENU= [
        Panel(CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Camera", Gcolor( Gcolor.chill(Gcolor.EARTH, 0.8) ), 0) ,
        Panel(CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Create", Gcolor( Gcolor.chill(Gcolor.VENUS, 0.8) ), 1) ,
        Panel(CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Erase", Gcolor( Gcolor.chill(Gcolor.MARS, 0.8) ), 2) ,
        Panel(CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Graph",  Gcolor( Gcolor.chill(Gcolor.SUN, 0.8) ), 3) ,
        Panel(CANVAS.subsurface( (0, 0), (Panel.WIDTH, Panel.HEIGTH) ), "Save", Gcolor( Gcolor.chill(Gcolor.NEPTUNE, 0.8) ), 4) ]
    active_panel= None
        
    def update():   
        if Sidebar.active_panel == None:
            for panel in Sidebar.MENU:
                panel.update()
        else:
            Sidebar.active_panel.update()
            
    def event_mouse(etype, position):
        if not Sidebar.active_panel:
            panel_index= position[1]//Banner.HEIGTH
            
            if panel_index < len(Sidebar.MENU):
               Sidebar.MENU[panel_index].event_mouse(etype, position)
        else:
            Sidebar.active_panel.event_mouse(etype, position)