import math
import pygame
from Block import Block


class Grid:

    def __init__(self, x1, y1, width, height, square_width, square_height, square_margin, grid_pad):
        self.grid = []
        x_count = math.floor((width - (grid_pad * 2)) / (square_width + square_margin * 2)) - 1
        y_count = math.floor((height - grid_pad * 2) / (square_height + square_margin * 2)) - 1
        x_pad = (width - ((grid_pad * 2) + (x_count * square_width) + (x_count * square_margin) + square_margin)) / 2 # Additional pad needed to center grid
        y_pad = (height - ((grid_pad * 2) + (y_count * square_height) + (y_count * square_margin) + square_margin)) / 2
        for i in range(0, y_count):
            self.grid.append([])
            for ii in range(0, x_count):
                block_x = x1 + grid_pad + x_pad + (ii * square_width)
                block_y = y1 + grid_pad + y_pad + (i * square_height)
                self.grid[i].append(Block(block_x, block_y, block_x + square_width, block_y + square_height, (0, 0, 0)))

    def get_size(self):
        return len(self.grid[0]), len(self.grid)

    def get_block(self, x, y):
        if x < 0 or y < 0 or x >= len(self.grid[0]) or y >= len(self.grid):
            return False
        return self.grid[y][x]

    def draw(self, screen):
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                block = self.grid[y][x]
                pygame.draw.rect(screen, block.color, block.rect, 1)
