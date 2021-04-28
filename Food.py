import pygame
from random import randint

FOOD_COLOR = (0, 0, 255)


class Food:

    def __init__(self, grid_size, snake):
        self.is_eaten = False
        self.grid_size = grid_size

        x, y = -1, -1
        while x == -1 or y == -1:  # TODO: needs to check if empty blocks exist
            x = randint(0, self.grid_size[0] - 1)
            y = randint(0, self.grid_size[1] - 1)
            for i in range(snake.get_size()):
                block_x, block_y = snake.get_block(i).get_pos()
                if x == block_x and y == block_y:
                    x, y = -1, -1
                    break
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def is_eaten(self):
        return self.is_eaten

    def eat(self):
        self.is_eaten = True

    def draw(self, screen, grid):
        block = grid.get_block(self.x, self.y)
        if block and not self.is_eaten:
            pygame.draw.rect(screen, FOOD_COLOR, block.rect, width=0)
