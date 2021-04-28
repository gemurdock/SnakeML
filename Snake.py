import math
from GameObject import GameObject
from lib.Direction import Direction

HEAD_COLOR = (255, 0, 0)
BODY_COLOR = (0, 0, 0)


class Snake:

    def __init__(self, grid_size):
        spawn_x = math.floor(grid_size[0] / 2)
        spawn_y = math.floor(grid_size[1] / 2)
        self.grid_size = grid_size
        self.blocks = [GameObject(spawn_x, spawn_y, HEAD_COLOR, grid_size)]
        for _ in range(2):
            self.grow()

    def grow(self):
        last_block = self.blocks[len(self.blocks) - 1]
        self.blocks.append(GameObject(last_block.x, last_block.y, BODY_COLOR, self.grid_size))

    def move(self, direction):
        is_on_map = self.blocks[0].move(direction)
        for i in range(1, len(self.blocks)):
            previous_block = self.blocks[i - 1]
            target_direction = self.blocks[i].get_trail_direction(previous_block)
            if target_direction != Direction.HALT:
                self.blocks[i].move(target_direction)
        return is_on_map

    def draw(self, screen, grid):
        for i in range(len(self.blocks) - 1, -1, -1):
            self.blocks[i].draw(screen, grid)
