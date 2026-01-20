import pygame
import math

class Platform:
    def __init__(self, x, y, width=150, height=20, color=(139, 69, 19)):
        self.rect = pygame.Rect(x, y, width, height)
        self.base_width = width
        self.base_height = height
        self.color = color
        self.time = 0

    def update(self):
        # Escala pulsante
        self.time += 0.05
        scale = 1 + 0.1 * math.sin(self.time)
        self.rect.width = int(self.base_width * scale)
        self.rect.height = int(self.base_height * scale)
