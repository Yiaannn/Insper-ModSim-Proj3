from collections import namedtuple

MOVE= 0
CLICK= 1
SCROLLUP= 2
SCROLLDOWN= 3
COLLISION= 400
        
def build(paramdict):
    for param in paramdict:
        if isinstance(paramdict[param], dict):
            paramdict[param] = build(paramdict[param])
            
    Signal= namedtuple("Signal", paramdict.keys())
    signal= Signal(*paramdict.values())
    
    return signal
        
def edit(signal, keylist, value):
        signal= signal._asdict()
        if  getattr(signal[keylist[0] ], "_asdict", None) != None:
            signal[keylist[0]]= edit(signal[keylist[0]], keylist[1:], value)
        else:
            signal[keylist[0]] = value
            
        return build(signal)
        