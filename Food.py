import pygame
from random import randint

FOOD_COLOR = (0, 0, 255)


class Food:

    def __init__(self, grid_size, snake):
        self.is_eaten = False
        self.grid_size = grid_size
        x = -1
        while x == -1:  # TODO: Build better way of selecting grid spot in case there are none left / more efficient
            x = randint(0, self.grid_size[0] - 1)
            for i in range(snake.get_size() - 1):
                if x == snake.get_block(i).get_pos()[0]:
                    x = -1
                    continue
                else:
                    self.x = x
        y = -1
        while y == -1:
            y = randint(0, self.grid_size[1] - 1)
            for i in range(snake.get_size() - 1):
                if y == snake.get_block(i).get_pos()[1]:
                    y = -1
                    continue
                else:
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
