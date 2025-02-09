import math as m

positions = {}
Objekts = {}

def objektOn(x,y,eps):
    res = 0
    for varx in positions.keys():
        if abs(varx - x) < eps:
            vary = positions[varx]
            if abs(vary - y) < eps:
                res = Objekts[str(varx)+str(vary)]
                break
    return res    
    
def addToSystem(sysObj):
    x = sysObj.pos[0]
    y = sysObj.pos[1]
    Objekts[str(x)+str(y)] = sysObj
    positions[x] = y

def removeFromSystem(sysObj):
    x = sysObj.pos[0]
    y = sysObj.pos[1]
    Objekts.pop(str(x)+str(y))
    positions.pop(x)
