import pygame

class Player:
    def __init__(self, x, y, width=50, height=60, color=(220, 50, 50)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_strength = -15
        self.on_ground = False

    def update(self, keys, platforms):
        # --------------------
        # MOVIMENTO HORIZONTAL
        # --------------------
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Colisão horizontal
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.rect.centerx < plat.rect.centerx:
                    self.rect.right = plat.rect.left
                else:
                    self.rect.left = plat.rect.right

        # --------------------
        # SALTO
        # --------------------
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False

        # --------------------
        # GRAVIDADE
        # --------------------
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Colisão vertical
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.velocity_y > 0:  # caindo
                    self.rect.bottom = plat.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # subindo
                    self.rect.top = plat.rect.bottom
                    self.velocity_y = 0

        # Limites do nível
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 2000:
            self.rect.right = 2000
