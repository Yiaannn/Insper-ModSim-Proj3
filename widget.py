import gsignal
from gcolor import Gcolor
import pygame.draw as draw
import pygame.font
import pygame.transform
import pygame

pygame.font.init()

SIZE= 1
BASE_HEIGTH= 60
WIDTH= 380
    
class Widget:
    BASE_HEIGTH= 60
    WIDTH= 380
    TAB= 20
    
    SIZE= 1
    
    FONT= pygame.font.SysFont('verdana',  30)
    
    def __init__(self):
        self.canvas= pygame.Surface( ( self.WIDTH, self.BASE_HEIGTH*self.SIZE ) )
    
    def update(self):
        pass
        
    def event_mouse(self, etype, position):
        pass
        
    def read_signal(self, signal):
        pass
        
    def draw(self):
        pass
        
class Label(Widget):
    FONT= pygame.font.SysFont('verdana',  42)
    HEIGTH= BASE_HEIGTH*SIZE
    
    def __init__(self, text, color):
        self.HEIGTH
        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH) )
        self.color= color
        self.text_color= Gcolor.darken( self.color.mix(self.color.WHITE, 0.5), 0.1)
        
        draw.rect(self.canvas, self.color.get(), ( (0, 0), (self.WIDTH, self.HEIGTH) ))
        self.canvas.blit( self.FONT.render(text, True, self.text_color), (self.TAB, 0) )
        
        
class DynamicGraph(Widget):
    SIZE= 5
    HEIGTH= BASE_HEIGTH*SIZE
    
    FONT= pygame.font.SysFont('verdana',  22)
    
    def __init__(self, color, sender):
        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH ) )
        self.color= color
        self.graph_color= self.color.darken(0.05)
        self.line_color= self.color.chill(0.8)
        self.line_thickness= 1
        self.support_line_color= self.color.darken(0.3)
        self.highlight_color= self.color.mix(self.color.WHITE, 0.5)
        self.text_color= Gcolor.darken( self.highlight_color, 0.1)
        self.color= self.color.get()
        #self.header= self.FONT.render(text, True, self.text_color)
        
        self.gWIDTH= self.WIDTH-4*self.TAB
        self.gHEIGTH= self.HEIGTH- 4*self.TAB
        self.min_value= 0
        self.max_value= 0
        self.min_is_set= False
        self.max_is_set= False
        
        sender.set_listener(self)
        
    def reset(self, ylabel):
        xlabel= self.FONT.render("Time (tu)", True, self.text_color)
        ylabel= self.FONT.render(ylabel, True, self.text_color)
        ylabel= pygame.transform.rotate(ylabel, 90)
        self.graph= pygame.Surface( ( self.gWIDTH, self.gHEIGTH ) )
        self.min_is_set= False
        self.max_is_set= False
        self.content= 0
        self.previous_point= None
        
        self.tick= 0
        
        #init graph
        draw.rect(self.graph, self.graph_color, ((0, 0), (self.gWIDTH, self.gHEIGTH)))
        for i in range(10, self.gWIDTH, 10):
            draw.line(self.graph, self.support_line_color, (i,0), (i, self.gHEIGTH))
        for i in range(10, self.gHEIGTH, 10):
            draw.line(self.graph, self.support_line_color, (0,i), (self.gWIDTH, i))
            
        draw.rect(self.canvas, self.color, ( (0, 0), (self.WIDTH, self.HEIGTH) ) )
        self.canvas.blit(self.graph, (3*self.TAB, self.TAB ) )
        
        self.canvas.blit(ylabel, (self.TAB, self.TAB ) )
        self.canvas.blit(xlabel, (3*self.TAB, 2*self.TAB+self.gHEIGTH ) )
        
    def draw(self):
        #draw graph
        backdrop= self.graph.copy()
        self.graph.blit(backdrop, (-1, 0))
        if self.tick%10 != 0:
            draw.line(self.graph, self.graph_color, (self.gWIDTH-1, 0), (self.gWIDTH-1, self.gHEIGTH-1))
            for i in range(10, self.gHEIGTH, 10):
                self.graph.set_at( (self.gWIDTH-1,i), self.support_line_color )
        else:
            draw.line(self.graph, self.support_line_color, (self.gWIDTH-1, 0), (self.gWIDTH-1, self.gHEIGTH-1))
        
        
        point= (3*self.gWIDTH//4, int( (self.content -self.min_value)*self.gHEIGTH/(self.max_value - self.min_value) ) )
        if self.previous_point:
            draw.aaline(self.graph, self.line_color, self.previous_point, point)
            
        x, y= point
        self.previous_point= (x-1, y)
        self.tick+=1
        
        #draw canvas
        self.canvas.blit(self.graph, (3*self.TAB, self.TAB ) )
        
        
    def read_signal(self, signal):
        if signal.type == gsignal.ACTION:
            if not self.min_is_set or self.min_value > signal.content:
                self.min_value= signal.content
                self.min_is_set= True
            if not self.max_is_set or self.max_value < signal.content:
                self.max_value= signal.content
                self.max_is_set= True
                
            if self.min_is_set and self.max_is_set and self.min_value < self.max_value:
                self.content= signal.content
                self.draw()
                
        elif signal.type == gsignal.RESET:
            self.reset(signal.content)
        
class valueTracker(Widget):
    HEIGTH= BASE_HEIGTH*SIZE
    
    def __init__(self, text, color, sender):
        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH ) )
        self.color= color
        self.highlight_color= self.color.mix(self.color.WHITE, 0.5)
        self.text_color= Gcolor.darken( self.highlight_color, 0.1)
        self.header= self.FONT.render(text, True, self.text_color)
        self.content= ""
        
        sender.set_listener(self)
        
    def draw(self):
        draw.rect(self.canvas,  self.color.get(), ((0, 0), (self.WIDTH, self.BASE_HEIGTH*self.SIZE)) )
        self.canvas.blit(self.header, (self.TAB,0))
        
        content= self.FONT.render(str(self.content), True, self.highlight_color)
        self.canvas.blit( content, (self.header.get_width()+ 2*self.TAB, 0))
            
    def read_signal(self, signal):
        if signal.type == gsignal.ACTION:
            self.content= signal.content
            
            self.draw()
    
class BoundButton(Widget):
    HEIGTH= BASE_HEIGTH*SIZE
    
    def __init__(self, text, color, listener, signaltype, ):
        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH ) )
        self.color= color
        self.color2= Gcolor.darken(self.color, 0.2)
        self.highlight_color= self.color.mix(self.color.WHITE, 0.5)
        self.text_color= Gcolor.darken( self.highlight_color, 0.1)
        self.color= color.get()
        
        self.label= self.FONT.render(text, True, self.text_color)
        self.signaltype= signaltype
        self.listener= listener
        
        self.draw();

    def draw(self):
        #draw button
        temp= self.label.copy()
        draw.rect(temp, self.color2, ( (0, 0), (self.WIDTH, self.HEIGTH) ) )
        temp.blit(self.label, (0, 0) )
        
        #draw widget
        draw.rect(self.canvas, self.color, ( (0, 0), (self.WIDTH, self.HEIGTH) ) )
        self.canvas.blit(temp, (self.TAB,0))
        
    def read_signal(self, signal):
        if signal.type == gsignal.CLICK:
            signal= gsignal.build( {
                "type": self.signaltype ,
                "content": self.content } )
            self.listener.read_signal(signal)
            
        elif signal.type == gsignal.ACTION:
            self.content= signal.target
            
class Scrollbar(Widget):
    HEIGTH= BASE_HEIGTH*SIZE
    
    def __init__(self, text, color, scrollist, return_index, signaltype, listener):
        self.canvas= pygame.Surface( ( self.WIDTH, self.HEIGTH ) )
        self.color= color
        self.highlight_color= self.color.mix(self.color.WHITE, 0.5)
        self.text_color= Gcolor.darken( self.highlight_color, 0.1)
        self.header= self.FONT.render(text, True, self.text_color)
        
        self.scrollist= scrollist
        self.return_index= return_index
        #
        self.signaltype= signaltype
        self.send= listener.read_signal
        
        self.tick= 0
        
        self.nogoodnameyet()

    def draw(self):
        draw.rect(self.canvas,  self.color.get(), ((0, 0), (self.WIDTH, self.BASE_HEIGTH*self.SIZE)) )
        
        self.canvas.blit(self.header, (self.TAB,0))
        if len( self.scrollist)!= 0:
            #content= self.FONT.render(str(self.scrollist[self.tick]), True, self.scrollist[self.tick].color.get())
            content= self.FONT.render(str(self.scrollist[self.tick]), True, self.highlight_color)
            self.canvas.blit( content, (self.header.get_width()+ 2*self.TAB, 0))
            
    def nogoodnameyet(self):
        target= self.scrollist[self.tick]
        if self.return_index:
            target= self.tick
            
        signal= gsignal.build( {
            "type": self.signaltype ,
            "target": self.scrollist[self.tick] } )
        self.send(signal)
        self.draw()
        
    def read_signal(self, signal):
        if signal.type == gsignal.CLICK:
            self.tick+= 1
            self.tick%= len(self.scrollist)
            self.nogoodnameyet()
            
        elif signal.type == gsignal.LCLICK:
            self.tick-= 1
            self.tick%= len(self.scrollist)
            self.nogoodnameyet()
'''
class Tool:

class Graph(Tool):
    
    def set()
'''