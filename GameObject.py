import pygame
from lib.Direction import Direction


class GameObject:

    # grid_size should be tuple (x_len, y_len)
    def __init__(self, x, y, color, grid_size):
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        self.color = color
        self.grid_size = grid_size

    def get_pos(self):
        return self.x, self.y

    def get_trail_direction(self, target_block):
        result = target_block.last_x - self.x, target_block.last_y - self.y
        if -1 <= result[0] - result[1] <= 1:
            if result[0] == -1 and result[1] == 0:
                return Direction.LEFT
            elif result[0] == 1 and result[1] == 0:
                return Direction.RIGHT
            elif result[0] == 0 and result[1] == -1:
                return Direction.UP
            elif result[0] == 0 and result[1] == 1:
                return Direction.DOWN
            else:
                return Direction.HALT
        return False

    def get_last_pos(self):
        return self.last_x, self.last_y

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y

    def set_color(self, color):
        self.color = color

    def is_on_map(self):
        if 0 <= self.x < self.grid_size[0] and 0 <= self.y < self.grid_size[1]:
            return True
        else:
            return False

    def move(self, direction):
        self.last_x = self.x
        self.last_y = self.y
        if direction == Direction.LEFT:
            self.x -= 1
        elif direction == Direction.RIGHT:
            self.x += 1
        elif direction == Direction.UP:
            self.y -= 1
        elif direction == Direction.DOWN:
            self.y += 1
        return self.is_on_map()

    def draw(self, screen, grid):
        block = grid.get_block(self.x, self.y)
        if block:
            pygame.draw.rect(screen, self.color, block.rect, width=0)
