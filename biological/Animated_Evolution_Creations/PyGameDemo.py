import pygame, sys
import numpy as np
pygame.init()
screen = pygame.display.set_mode([640,480])
screen.fill([255,255,255])

face = pygame.image.load('Face.png')
x = 200
y = 200
screen.blit(face,[x,y])
#pygame.draw.circle(screen,[255,0,0],[320,240],30,0)
pygame.display.flip()    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            pygame.draw.rect(screen,[255,255,255],[x,y,90,90],0)
            [x,y] = event.pos      
    pygame.time.delay(20)
    pygame.draw.rect(screen,[255,255,255],[x,y,90,90],0) # забеливаем прошлое место
    x += np.cos(pygame.time.get_ticks()/1000)
    y += np.sin(pygame.time.get_ticks()/1000)
    screen.blit(face,[x,y])
    pygame.display.flip()
pygame.quit()
