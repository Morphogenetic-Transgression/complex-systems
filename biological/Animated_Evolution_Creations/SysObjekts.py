import math as m
import System
import time 

def norma(vektor):
    return (vektor[0]**2 + vektor[1]**2)**(1/2)

#==============================class SystemObjekt()
class SystemObjekt():
    def __init__(self,pos,calor,size):
        self.pos = pos
        self.calor = calor
        self.size = size
        self.eatten = False
        System.addToSystem(self)

    def info(self):
        print("pos = ")
        print(self.pos)
        print("calor = "+self.calor)
        print("size = "+str(self.size))
        print("eatten = ")
        print(self.eatten)

#================================class SystemObjekt()

#================================class Creature(SystemObjekt)
class Creature(SystemObjekt):
    def __init__(self,pos,calor,size,dest,age,mared,R_see):
        SystemObjekt.__init__(self,pos,calor,size)
        self.age = age
        self.mared = mared
        self.piksUp = False
        self.R_see = R_see
        self.dest = dest

    def pikUp(self):
        self.piksUp = True

    def makeKid(self):
        pass

    def move(self):
        print("move")
        self.pos[0] += self.dest[0]
        self.pos[1] += self.dest[1]
        time.sleep(1) #========================== time.sleep()

    def moveToObj(self,sysObj,KpFi,KpNor,eps):
        print("startmove")
        target = []
        target.append(sysObj.pos[0])
        target.append(sysObj.pos[1])
        nor = norma(self.dest)
        erX = target[0] - self.pos[0]
        erY = target[1] - self.pos[1]
        while abs(erX) > eps or abs(erY) > eps: # пока не дошел
            fi = m.atan2(self.dest[1],self.dest[0])
            teta = m.atan2(erY,erX)
            fi += KpFi*(teta-fi)
            self.dest[0] = KpNor*nor*m.cos(fi)
            self.dest[1] = KpNor*nor*m.sin(fi)
            self.move()
            # можно походу проверять не пропал ли объект с места
            erX = target[0] - self.pos[0]
            erY = target[1] - self.pos[1]
        pred1 = (erX < eps and erY < eps)
        pred2 = (target[0] == sysObj.pos[0] and target[1] == sysObj.pos[1])
        if pred1 and pred2:
            #если объект все еще на месте и мы дошли до него
            return True
        else:
            return False

    def lookInDest(self,n):
        d = self.R_see/n
        nor = norma(self.dest)
        sysObj = 0
        for i in range(5,n+1):
            x = self.pos[0] + i*d*self.dest[0]/nor
            y = self.pos[1] + i*d*self.dest[1]/nor
            sysObj = System.objektOn(x,y,3) # 3 это большая погрешность
            if not(sysObj == 0):
                break
        return sysObj
                
            
    def lookAround(self): # смотреть значит жить
        nor = norma(self.dest)
        fi = m.atan(self.dest[1]/self.dest[0])
        sysObj = 0
        while True:
            sysObj = self.lookInDest(10) # ищим в этом направлении
            if sysObj == 0: # добавить условия
                fi += m.pi/180 # поварачиваем вектор направления на один градус
                self.dest[0] = nor*m.cos(fi)
                self.dest[1] = nor*m.sin(fi)
            else:
                break
        self.analisTheObjekt(sysObj)

    def eat(self,food):
        self.size += food.size
        self.age += 0.2
        food.eatten = True
        System.removeFromSystem(food)        

    def analisTheObjekt(self,sysObj):
        print(sysObj)
        if sysObj == 0:
            print("sysObj == 0")
        if sysObj.calor == "food":
            get = self.moveToObj(sysObj,0.4,0.3,0.5)
            if get:
                self.eat(sysObj)
            else:
                print("не дошли до объекта")
        else:
            print("not known objekt")

    def info(self):
        print("pos = ")
        print(self.pos)
        print("calor = "+self.calor)
        print("size = "+str(self.size))
        print("dest = ")
        print(self.dest)
        print("age = "+str(self.age))
        print("mared = "+str(self.mared))
        print("R_see = "+str(self.R_see))
#============================================class Creature(SystemObjekt)

#sys.getrefcount(a) - проверка числа ссылок

        




                
