import pygame
import math

class Enemy:
    def __init__(self, x, y, min_x, max_x, speed=2, width=40, height=30, color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_x = min_x
        self.max_x = max_x
        self.speed = speed
        self.color = color

        self.base_y = y
        self.time = 0

        # Guardar estado inicial para reinício “limpo”
        self.start_x = x
        self.start_y = y
        self.start_speed = speed

    def reset(self):
        # Volta ao estado inicial (e evita começar colado a uma fronteira)
        self.rect.x = self.start_x
        self.base_y = self.start_y
        self.rect.y = self.start_y
        self.time = 0

        # Garante que não fica preso na fronteira ao reiniciar
        # (e mantém o sentido original)
        self.speed = self.start_speed
        if self.rect.left <= self.min_x:
            self.rect.left = self.min_x + 1
        if self.rect.right >= self.max_x:
            self.rect.right = self.max_x - 1

    def update(self):
        # Movimento horizontal
        self.rect.x += self.speed

        # Se passou dos limites, “encosta” e inverte (sem ficar a colar)
        if self.rect.left < self.min_x:
            self.rect.left = self.min_x
            self.speed *= -1
        elif self.rect.right > self.max_x:
            self.rect.right = self.max_x
            self.speed *= -1

        # Oscilação vertical suave
        self.time += 0.05
        self.rect.y = int(self.base_y + 5 * math.sin(self.time))
