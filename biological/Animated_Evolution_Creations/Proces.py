from threading import Thread
import pygame, sys
import SysObjekts as obs
import random
import time

Face = obs.Creature([20,30],"man",10,[9/4,7/4],3,False,10)
Food = 0 #obs.SystemObjekt([0,0],"food",5)
 
class Thread_Visualise(Thread):
    def __init__(self, name):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name
    
    def run(self):
        """Запуск потока"""
        amount = random.randint(3, 9) #15
        time.sleep(amount)
        
        pygame.init()
        screen = pygame.display.set_mode([700,500])
        screen.fill([255,255,255])
        face = pygame.image.load('Face.png')
        food = pygame.image.load('Food.png')
        pygame.display.flip()    
        running = True
        foodPos = [0,0]
        facePos = [0,0]
        while running:
            pygame.time.delay(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # забеливаем прошлое место
                    pygame.draw.rect(screen,[255,255,255],[foodPos[0],foodPos[1],40,40],0)
                    foodPos = event.pos
                    screen.blit(food,foodPos)
                    Food = obs.SystemObjekt([foodPos[0]/10,foodPos[1]/10],"food",5)
            pygame.draw.rect(screen,[255,255,255],[facePos[0],facePos[1],40,40],0)
            facePos[0] = Face.pos[0]*10
            facePos[1] = Face.pos[1]*10
            screen.blit(face,facePos)
            pygame.display.flip()
            #if Food.eatten:
             #   pygame.draw.rect(screen,[255,255,255],[foodPos[0],foodPos[1],90,90],0)
                
        pygame.quit()
        
        

class Thread_Proces(Thread):
    def __init__(self, name):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name
    
    def run(self):
        """Запуск потока"""
        amount = random.randint(3, 15)
        time.sleep(amount)

        #for i in range(5):
        print(Face)
        #print(Food)
        Face.info()
        #print("=================")
        #Food.info()
        print("=================")
        Face.lookAround()
        print("=================")
        Face.info()
        print("=================")
        #Food.info()
        time.sleep(7)           
        
        
def create_threads():
    proc = Thread_Proces("proces")
    proc.start()
    visual = Thread_Visualise("visual")
    visual.start()
    
if __name__ == "__main__":
    create_threads()







