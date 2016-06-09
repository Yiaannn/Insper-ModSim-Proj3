from gcolor import Gcolor
import gsignal
import widget
import pygame.font
import pygame.draw
import pygame.display

pygame.font.init()
#print(pygame.font.get_fonts())

class Banner():
    WIDTH= 400
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
    
    def __init__(self, text, text_color, color, widget_list):
        self.widget_list= widget_list
        self.WIDTH= widget.WIDTH
        self.HEIGTH= len(widget_list)*widget.BASE_HEIGTH
        
        self.color= color
        self.text_color= text_color
        self.text= text
        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH ) )
        
    def update(self):
        for i in range(len(self.widget_list)):
            if self.widget_list[i]:
                self.widget_list[i].update()
                self.canvas.blit(self.widget_list[i].canvas, (0, i*widget.BASE_HEIGTH))
        for i in range(len(self.widget_list)):
            if self.widget_list[i] and i !=0:
                pygame.draw.aaline(self.canvas, Gcolor.darken(self.color.illuminate(), 0.4), (widget.Widget.TAB, widget.Widget.BASE_HEIGTH*i), (widget.Widget.WIDTH - 2*widget.Widget.TAB, widget.Widget.BASE_HEIGTH*i), True)
                
    def read_signal(self, signal):
        if signal.type == gsignal.CLICK or signal.type == gsignal.LCLICK:
            unit= signal.position.y//widget.Widget.BASE_HEIGTH
            if unit < len(self.widget_list):
                while not self.widget_list[unit]:
                    unit-= 1
                signal= gsignal.edit(signal, ["position", "y"], signal.position.y - unit*widget.Widget.BASE_HEIGTH)
                self.widget_list[unit].read_signal(signal)
            
        

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
        
    def __init__(self, canvas, ptype, color, index, listener):
        
        self.canvas= canvas
        self.ptype= ptype
        self.color= color
        self.text_color= Gcolor.darken( self.color.mix(self.color.WHITE, 0.5), 0.1 )
        self.text=  self.FONT.render(ptype, True, self.text_color)
        self.index= index
        self.listener= listener
        
        widget_list=[ widget.Label(self.ptype, self.color) ]
        
        if self.ptype == "Camera":
            from celestial_cluster import CelestialCluster
            from perspective import Perspective
            widget_list+= [
                widget.Scrollbar("Lock on", self.color, CelestialCluster.cluster, False, gsignal.ACTION, Perspective) ]
                
        elif self.ptype == "Graph":
            from celestial_cluster import CelestialCluster
            widget_list+= [
                widget.Scrollbar("Measure", self.color, CelestialCluster.word_list, True, gsignal.WATCH0, CelestialCluster) ,
                widget.Scrollbar("Between", self.color, CelestialCluster.cluster, False, gsignal.WATCH1, CelestialCluster) ,
                widget.Scrollbar("And", self.color, CelestialCluster.cluster, False, gsignal.WATCH2, CelestialCluster) ,
                widget.DynamicGraph( self.color, CelestialCluster) ,
                None ,
                None ,
                None ,
                None ]
                
        elif self.ptype == "Erase":
            from celestial_cluster import CelestialCluster
            widget1= widget.BoundButton("Confirm", self.color, CelestialCluster, gsignal.DELETE, )
            widget2= widget.Scrollbar("Erase", self.color, CelestialCluster.cluster, False, gsignal.ACTION, widget1)
            widget_list+= [ widget2, widget1 ]
        #if self.ptype == "Create":
        #    widget_list+= [
            
        self.banner= Banner(self.text, self.color, pygame.Surface((Banner.WIDTH, Banner.HEIGTH) ) )
        self.body= Body( self.text, self.text_color, self.color, widget_list)
        
        self.active= False
        self.mouse_over= False
        self.busy= False
        self.tick= 0
        self.tick2= 0
        
    def  read_signal(self, signal):
        if not self.busy:
            if not self.active:
                if signal.type == gsignal.MOVE:
                    self.mouse_over= True
                    
                elif signal.type == gsignal.CLICK:
                    self.busy= True
                    signal= gsignal.build( {
                        "type": gsignal.ACTION ,
                        "target": self } )
                    self.listener.read_signal(signal)
                    
            else:
                if signal.type == gsignal.MOVE:
                    if signal.position.y < self.banner.HEIGTH:
                        self.mouse_over= True
                        
                if signal.type == gsignal.CLICK or signal.type == gsignal.LCLICK:
                    if signal.position.x >= self.banner.STRAP_WIDTH and signal.position.y >= self.banner.HEIGTH:
                        signal= gsignal.edit(signal, ["position", "x"], signal.position.x - self.banner.STRAP_WIDTH)
                        self.body.read_signal(signal)
                    else:
                        self.busy= True
                        signal= gsignal.build( {
                            "type": gsignal.ACTION ,
                            "target": self } )
                        self.listener.read_signal(signal)
    
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
                if self.tick2 != self.MAX_TICK2:
                    self.tick2+= 1
                if self.tick == self.MAX_TICK and self.tick2 == self.MAX_TICK2:
                    self.busy= False
                    self.active= True
                    self.tick= 0
                    self.tick2= 0
                    
                    signal= gsignal.build( {
                        "type": gsignal.REINDEX ,
                        "target": self } )
                    self.listener.read_signal(signal)
        
        self.mouse_over= False
        self.draw()
        self.body.update()
    
    def draw(self):
        gamma=1/3
    
        if self.active:
                gamma= 3
                offset= (self.tick**gamma)*(self.banner.WIDTH-Banner.STRAP_WIDTH)//(self.MAX_TICK**gamma)
                
                #draw banner
                self.canvas.blit(self.banner.canvas,   (offset, 0) )
                
                #draw body
                self.canvas.blit(self.body.canvas, ( self.banner.STRAP_WIDTH + offset, 0) )
                
        else:
            if not self.busy:
                offset= (self.tick**gamma)*(self.banner.WIDTH-Banner.STRAP_WIDTH)//(self.MAX_TICK**gamma)
                self.canvas.blit(self.banner.canvas,  ( (self.banner.WIDTH-Banner.STRAP_WIDTH) - offset, self.index*self.banner.HEIGTH))
            
            else:
                offset= (self.tick**gamma)*(self.banner.WIDTH-Banner.STRAP_WIDTH)//(self.MAX_TICK**gamma)
            
                gamma= 1
                offset2_1= (self.tick2**gamma)*(self.index*self.banner.HEIGTH)//(self.MAX_TICK2**gamma)
                offset2_2= (self.tick2**gamma)*(self.HEIGTH - (self.index+1)*self.banner.HEIGTH )//(self.MAX_TICK2**gamma)
                
                temp1= (self.banner.HEIGTH*(self.index))- offset2_1
                temp2= (self.tick2*(self.body.HEIGTH-widget.BASE_HEIGTH))//self.MAX_TICK2 + widget.BASE_HEIGTH -1
                print(temp1)
                print( ( (0, 0), ( self.body.WIDTH, temp2 ) ) )
                
                self.canvas.blit(self.banner.canvas,  ( (self.banner.WIDTH-Banner.STRAP_WIDTH) - offset, self.index*self.banner.HEIGTH- offset2_1) )
                
                canvi= self.body.canvas.subsurface( ( (0, 0), ( self.body.WIDTH, temp2 ) ) )
                self.canvas.blit(canvi, ( ( self.banner.STRAP_WIDTH + (self.banner.WIDTH-Banner.STRAP_WIDTH) - offset, temp1), (canvi.get_width(), canvi.get_height() ) ) )        
