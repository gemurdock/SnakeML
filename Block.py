import pygame


class Block:

    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2- y1)
        self.color = color

    def set_pos(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.rect = pygame.Rect(x1, y1, x1 - x2, y1 - y2)

    def set_color(self, color):
        self.color = color

    def get_pos(self):
        return self.x1, self.y1, self.x2, self.y2

    def intersects(self, block):
        if self.x1 < block.x2 and self.x2 > block.x1 and self.y1 > block.y2 and self.y2 < block.y1:
            return True
        else:
            return False

    def draw(self, screen, width=1):
        pygame.draw.rect(screen, self.color, self.rect, width)
