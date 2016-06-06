from celestial_cluster import CelestialCluster
from collections import namedtuple
import pygame.event

class Gevent():
    MOVE= 0
    CLICK= 1
    SCROLLUP= 2
    SCROLLDOWN= 3
    
    quit= False
    buffer= []

    def update():
        from display import Display
        
        ORDER= {
            pygame.MOUSEBUTTONDOWN: Gevent.event_mouse ,
            pygame.QUIT: Gevent.event_quit }
            
        pygame.event.pump()
        
        Gevent.buffer+= pygame.event.get()
        
        x, y= pygame.mouse.get_pos()
        event= Gevent.build_event( {
            "type": Gevent.MOVE ,
            "position": {"x": x, "y": y}  } )
        Display.event_mouse(event)
        
        while len(Gevent.buffer) != 0:
            if Gevent.buffer[0].type in ORDER:
                ORDER[Gevent.buffer[0].type](Gevent.buffer[0])
            Gevent.buffer.pop(0)
    
    def push(event):
        Gevent.buffer.append(event)
        
    def build_event(paramdict):
        for param in paramdict:
            if isinstance(paramdict[param], dict):
                paramdict[param] = Gevent.build_event(paramdict[param])
                
        Event= namedtuple("Event", paramdict.keys())
        event= Event(*paramdict.values())
        
        return event
        
    def edit_event(event, keylist, value):
            event= event._asdict()
            if  getattr(event[keylist[0] ], "_asdict", None) != None:
                event[keylist[0]]= Gevent.edit_event(event[keylist[0]], keylist[1:], value)
            else:
                event[keylist[0]] = value
                
            return Gevent.build_event(event)
        
    def event_mouse(stuff):
        x, y= pygame.mouse.get_pos()
        from display import Display
        
        if stuff.button == 1:
            event= Gevent.build_event( {
                "type": Gevent.CLICK ,
                "position":  {"x": x, "y": y} } )
            Display.event_mouse(event)
        elif stuff.button == 4:
            event= Gevent.build_event( {
                "type": Gevent.SCROLLDOWN ,
                "position":  {"x": x, "y": y} } )
            Display.event_mouse(event)
        elif stuff.button == 5:
            event= Gevent.build_event( {
                "type": Gevent.SCROLLUP ,
                "position": {"x": x, "y": y} } )
            Display.event_mouse(event)

    def event_quit(self, stuff):
        self.quit= True