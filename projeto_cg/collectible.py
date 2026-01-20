import pygame

class Collectible:
    def __init__(self, x, y, radius=10, color=(255, 215, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.rect = pygame.Rect(x - radius, y - radius, radius*2, radius*2)
        self.collected = False

    def check_collision(self, player_rect):
        if not self.collected and self.rect.colliderect(player_rect):
            self.collected = True
            return True
        return False

    def draw(self, screen, camera_x):
        if not self.collected:
            pygame.draw.circle(screen, self.color, (self.x - camera_x, self.y), self.radius)
