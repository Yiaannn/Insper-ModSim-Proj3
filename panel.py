from gcolor import Gcolor
from gevent import Gevent
from widget import Widget
import pygame.font
import pygame.draw
import pygame.display

pygame.font.init()
#print(pygame.font.get_fonts())

class Banner():
    WIDTH= 280
    HEIGTH= 60
    STRAP_WIDTH= 20

    def  __init__(self, text, color, canvas):
        self.color= color
        self.canvas= canvas
        self.text=text
        
        #draw strap
        pygame.draw.rect(self.canvas, Gcolor.darken(self.color.burn( 0.9), 0.5), ( (0, 0), (Banner.STRAP_WIDTH, Banner.HEIGTH) ) )
                
        #draw main
        pygame.draw.rect(self.canvas, self.color.get(), ( (Banner.STRAP_WIDTH, 0), (Banner.WIDTH-Banner.STRAP_WIDTH, Banner.HEIGTH) ) )
        self.canvas.blit(self.text, (Banner.STRAP_WIDTH*2, 0) )
        
class Body():
    WIDTH= Banner.WIDTH - Banner.STRAP_WIDTH
    HEIGTH= 9*Banner.HEIGTH
    
    def __init__(self, text, text_color, color, canvas, widget_list):
        self.color= color
        self.text_color= text_color
        self.text= text
        self.canvas= canvas
        self.widget_list= widget_list
        
        self.draw()
        
    def draw(self):
        
        #draw panel
        pygame.draw.rect( self.canvas, self.color.get(), ( (0, 0), (self.WIDTH, self.HEIGTH) ) )
        
        #draw widgets
        for widget in self.widget_list:
            widget.draw()
        

class Panel:
    WIDTH= Banner.WIDTH
    HEIGTH= 10*Banner.HEIGTH
    BANNER_HEIGTH= 60
    
    FONT= pygame.font.SysFont('verdana',  42)
    
    MAX_TICK= 20
    MAX_TICK2= 20
    
    WIDGET_LIST={
        "Camera": [] ,
        "Create": [] ,
        "Erase": [] ,
        "Graph": [] ,
        "Save": [] }
    def __init__(self, canvas, ptype, color, index):
        
        self.canvas= canvas
        self.ptype= ptype
        self.color= color
        self.text_color= self.color.mix(self.color.WHITE, 0.5)
        self.text=  self.FONT.render(ptype, True, self.text_color)
        self.index= index
        
        self.banner= Banner(self.text, self.color, pygame.Surface((Banner.WIDTH, Banner.HEIGTH) ) )
        self.body= Body( self.text, self.text_color, self.color, pygame.Surface( (Body.WIDTH, Body.HEIGTH) ), Panel.WIDGET_LIST[ptype])
        
        self.active= False
        self.mouse_over= False
        self.busy= False
        self.tick= 0
        self.tick2= 0
        
    def event_mouse(self, event):
        if not self.busy:
            if not self.active:
                if event.type == Gevent.MOVE:
                    self.mouse_over= True
                    
                elif event.type == Gevent.CLICK:
                    self.busy= True
                    
            else:
                if event.type == Gevent.MOVE:
                    if event.position.x < self.banner.STRAP_WIDTH:
                        self.mouse_over= True
                        
                if event.type == Gevent.CLICK:
                    if event.position.x >= self.banner.STRAP_WIDTH:
                        #detectar em que widget do menu eu cliquei
                        #passar o controle pra esse widget
                        pass
                    else:
                        self.busy= True
    
    def update(self):
        
        if self.active:
            if not self.busy:
                if self.mouse_over and self.tick != self.MAX_TICK//2:
                    self.tick+=1
                elif not self.mouse_over and self.tick!= 0:
                    self.tick-=1
            
            else:
                if self.tick!= self.MAX_TICK:
                    self.tick+= 1
                else:
                    self.tick= 0
                    self.active= False
                    self.busy= False
        
        else:
            if not self.busy:
                if self.mouse_over and self.tick != self.MAX_TICK:
                    self.tick+=1
                elif not self.mouse_over and self.tick != 0:
                    self.tick-=1
                    
            else:
                if self.tick != self.MAX_TICK:
                    self.tick+=1
                elif self.tick2 != self.MAX_TICK2:
                    self.tick2+= 1
                else:
                    self.busy= False
                    self.active= True
                    self.tick= 0
                    self.tick2= 0
        
        self.mouse_over= False
        self.draw()
    
    def draw(self):
        gamma=1/3
    
        if self.active:
                gamma= 3
                offset= (self.tick**gamma)*(self.banner.WIDTH-Banner.STRAP_WIDTH)//(self.MAX_TICK**gamma)
                
                #draw banner
                self.canvas.blit(self.banner.canvas,   (offset, self.index*self.banner.HEIGTH) )
                
                #draw panel
                self.canvas.blit(self.body.canvas, ( self.banner.STRAP_WIDTH + offset, self.BANNER_HEIGTH) )
                
                #draw header
                pygame.draw.rect( self.canvas, self.color.get(), ( (self.banner.STRAP_WIDTH+offset, 0), (self.WIDTH, self.BANNER_HEIGTH) ) )
                self.canvas.blit(self.text, ( self.banner.STRAP_WIDTH*2+offset, 0) )
                pygame.draw.aaline(self.canvas, Gcolor.darken(self.color.illuminate(), 0.4), (2*self.banner.STRAP_WIDTH + offset, self.BANNER_HEIGTH), (self.banner.WIDTH + offset - self.banner.STRAP_WIDTH, self.BANNER_HEIGTH), True)
                
            
        else:
            offset= (self.tick**gamma)*(self.banner.WIDTH-Banner.STRAP_WIDTH)//(self.MAX_TICK**gamma)
            self.canvas.blit(self.banner.canvas,  ( (self.banner.WIDTH-Banner.STRAP_WIDTH) - offset, self.index*self.banner.HEIGTH))
            
            if self.busy:
                offset= (self.tick**gamma)*(self.banner.WIDTH-Banner.STRAP_WIDTH)//(self.MAX_TICK**gamma)
                self.canvas.blit(self.banner.canvas,  ( (self.banner.WIDTH-Banner.STRAP_WIDTH) - offset, self.index*self.banner.HEIGTH))
            
                gamma= 1
                offset2_1= (self.tick2**gamma)*(self.index*self.banner.HEIGTH)//(self.MAX_TICK2**gamma)
                offset2_2= (self.tick2**gamma)*(self.HEIGTH - (self.index+1)*self.banner.HEIGTH )//(self.MAX_TICK2**gamma)
                pygame.draw.rect( self.canvas, self.color.get(), ( ( (self.banner.WIDTH-Banner.STRAP_WIDTH) - offset + self.banner.STRAP_WIDTH, (self.index*self.banner.HEIGTH) - offset2_1), ( self.banner.WIDTH -self.banner.STRAP_WIDTH, self.banner.HEIGTH + offset2_1 + offset2_2) ) )
                self.canvas.blit(self.text, ( Body.WIDTH - offset + self.banner.STRAP_WIDTH*2, (self.index*self.banner.HEIGTH) - offset2_1) )
                #pygame.draw.aaline(self.canvas, Gcolor.darken(self.color.illuminate(), 0.4), (2*self.banner.STRAP_WIDTH + Body.WIDTH - offset, (self.index+1)*self.banner.HEIGTH - offset2_1), (2*Body.WIDTH - self.banner.STRAP_WIDTH - offset,  (self.index+1)*self.banner.HEIGTH - offset2_1), True)
                
                
                
                
                
        