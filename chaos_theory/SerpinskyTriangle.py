import pygame
import sys
import random
import time

font_ = pygame.font.Font("freesansbold.ttf", 36)

DOT_SIZE = 2


def pp():
    x = round(random.random() * 600)
    y = round(random.random() * 400)
    return pygame.draw.circle(screen, [0, 0, 0], [x, y], DOT_SIZE, 0)


pygame.init()
pygame.display.set_caption("Serpinsky Triangle")
screen = pygame.display.set_mode([700, 500])
screen.fill([250, 250, 250])

A = pp()
pygame.display.flip()
B = pp()
pygame.display.flip()
C = pp()
pygame.display.flip()

D = pp()
pygame.display.flip()

running = flag = True

wait_sec = 0.01


while running:

    time.sleep(wait_sec)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            flag = not flag

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                wait_sec = max(0.0, wait_sec - 0.01)  # decrease delay
            elif event.key == pygame.K_DOWN:
                wait_sec += 0.01  # increase delay

    pres = D
    inFront = 0
    z = random.randint(1, 3)
    if z == 1:
        inFront = A
    if z == 2:
        inFront = B
    if z == 3:
        inFront = C
    inFrontCords = inFront.center
    presCords = pres.center
    x = round((inFrontCords[0] - presCords[0]) / 2 + presCords[0])
    y = round((inFrontCords[1] - presCords[1]) / 2 + presCords[1])
    if flag:
        D = pygame.draw.circle(screen, [0, 0, 0], [x, y], DOT_SIZE, 0)
        pygame.display.flip()

    text = font_.render(f"Sleep time: {wait_sec:.2f}s", True, (255, 255, 255))
    screen.blit(text, (50, 130))
    pygame.display.flip()

pygame.quit()
