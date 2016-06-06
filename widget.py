import gsignal

class Widget:
    Size= 1
    
    def __init__(self):
        pass
    
    def update(self):
        pass
        
    def event_mouse(self, etype, position):
        pass
        
    def draw(self):
        pass
        
class Scrollbar(Widget):
    SIZE= 1
    
    def __init__(text, color, list, signal, receiver):
        self.text= text
        self.text_color= text_color
        self.color= color
        self.scrollable= list
        self.event= event
        
        self.tick= 0
    
    def update(self):
        pass
        
    def event_mouse(self, etype, position):
        if etype == "click":
            self.tick+= 1
            self.tick%= len(self.scrollable)
        #throw event
    
    def draw():
        pass
'''
class Tool:

class Graph(Tool):
    
    def set()
'''