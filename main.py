import math
import pygame

WIDTH = 810
HEIGHT = 505
PAD = 5

BLACK = (0, 0, 0)

def draw_grid(screen, x_start, y_start, x_end, y_end, x_tiles, y_tiles):
    width = x_end - x_start
    height = y_end - y_start
    tile_width = math.floor(width / x_tiles)
    tile_height = math.floor(height / y_tiles)
    for x in range(x_start, x_start + width, tile_width):
        for y in range(y_start, y_start + height, tile_height):
            rect = pygame.Rect(x, y, tile_width, tile_height)
            pygame.draw.rect(screen, BLACK, rect, 1)

pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    draw_grid(screen, PAD, 100, WIDTH - PAD, HEIGHT - PAD, 40, 20)

    pygame.display.flip()

pygame.quit()
