import math
import time
import pygame
from Grid import Grid
from Snake import Snake
from lib.GameState import GameState
from lib.Direction import Direction

WIDTH = 810
HEIGHT = 505
PAD = 5

BLACK = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])

# -- Game Vars --
state = GameState.RUNNING
last_tick = math.floor(time.time() * 1000)
grid = Grid(0, 100, WIDTH, HEIGHT - 100, 15, 15, 0, 5)
snake = Snake(grid.get_size())
player_direction = Direction.RIGHT

print("Grid size: %s" % (grid.get_size(),))

running = True
while running:
    time_now = math.floor(time.time() * 1000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                player_direction = Direction.RIGHT
            elif event.key == pygame.K_UP:
                player_direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                player_direction = Direction.DOWN

    if (time_now - last_tick) >= 250 and state == GameState.RUNNING:  # Each tick of the game, do this
        is_on_map = snake.move(player_direction)
        if not is_on_map:
            state = GameState.FINISHED
            print('Game over')
        last_tick = math.floor(time.time() * 1000)
    elif state == GameState.PAUSED:
        last_tick = math.floor(time.time() * 1000)

    screen.fill((255, 255, 255))

    grid.draw(screen)
    snake.draw(screen, grid)

    pygame.display.flip()

pygame.quit()
