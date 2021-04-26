import math
import pygame
from Grid import Grid

WIDTH = 810
HEIGHT = 505
PAD = 5

BLACK = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])

# -- Game Vars --
grid = Grid(0, 100, WIDTH, HEIGHT - 100, 20, 20, 0, 5)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    grid.draw(screen)

    pygame.display.flip()

pygame.quit()
