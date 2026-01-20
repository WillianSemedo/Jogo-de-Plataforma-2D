import pygame
import sys
from player import Player
from platform import Platform
from enemy import Enemy
from collectible import Collectible
from game_won import draw_game_won  # ✅ NOVO

pygame.init()

# --------------------
# CONFIGURAÇÕES
# --------------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Plataforma 2D")

clock = pygame.time.Clock()
FPS = 60

# Cores
BLUE = (100, 149, 237)
BLACK = (0, 0, 0)
GREEN = (60, 180, 75)
RED = (220, 50, 50)
DARK = (50, 50, 50)
YELLOW = (255, 215, 0)

font = pygame.font.SysFont(None, 48)

# --------------------
# OBJETOS
# --------------------
player = Player(100, HEIGHT - 100, color=RED)

platforms = [
    Platform(200, 450),
    Platform(450, 350), 
    #Platform(300, 250),
    Platform(600, 500),
    Platform(750, 400),
    Platform(900, 300),
    Platform(1100, 450),
    Platform(1300, 350),
    Platform(1500, 250),
    Platform(1700, 400)
]

# Plataformas fixas
for plat in platforms:
    plat.update = lambda: None

# Chão fixo
ground = Platform(0, HEIGHT - 40, width=2000, height=40, color=GREEN)
ground.update = lambda: None
platforms.append(ground)

enemies = [
    Enemy(220, 420, 200, 350),
    Enemy(470, 320, 450, 600, speed=3),
    Enemy(650, 470, 600, 750),
    Enemy(950, 270, 900, 1050, speed=3),
    Enemy(1350, 320, 1300, 1450, speed=2),
    Enemy(1600, 370, 1500, 1750, speed=3)
]

collectibles = [
    Collectible(220, 420),
    Collectible(480, 320),
    Collectible(780, 380),
    Collectible(920, 280),
    Collectible(1120, 420),
    Collectible(1320, 320),
    Collectible(1520, 230),
    Collectible(1720, 370)
]

# --------------------
# VARIÁVEIS DO JOGO
# --------------------
game_over = False
game_won = False  # ✅ NOVO
score = 0
camera_x = 0

# --------------------
# LOOP PRINCIPAL
# --------------------
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # ✅ Agora o jogo só atualiza enquanto não perdeu e não ganhou
    if not game_over and not game_won:
        # Jogador
        player.update(keys, platforms)

        # Inimigos
        for enemy in enemies:
            enemy.update()
            if player.rect.colliderect(enemy.rect):
                game_over = True

        # Coletáveis
        for collectible in collectibles:
            if collectible.check_collision(player.rect):
                score += 50

        # ✅ Verificar vitória (todas as moedas apanhadas)
        if all(c.collected for c in collectibles):
            game_won = True

        # Câmara 2D
        camera_x = player.rect.centerx - WIDTH // 2
        if camera_x < 0:
            camera_x = 0

    # --------------------
    # DESENHO
    # --------------------
    screen.fill(BLUE)

    # Plataformas
    for plat in platforms:
        shadow = pygame.Rect(plat.rect.x - camera_x + 5, plat.rect.y + 5,
                             plat.rect.width, plat.rect.height)
        pygame.draw.rect(screen, DARK, shadow)

        pygame.draw.rect(
            screen,
            plat.color,
            pygame.Rect(plat.rect.x - camera_x, plat.rect.y,
                        plat.rect.width, plat.rect.height)
        )

    # Inimigos
    for enemy in enemies:
        shadow = pygame.Rect(enemy.rect.x - camera_x + 5, enemy.rect.y + 5,
                             enemy.rect.width, enemy.rect.height)
        pygame.draw.rect(screen, DARK, shadow)

        pygame.draw.rect(
            screen,
            enemy.color,
            pygame.Rect(enemy.rect.x - camera_x, enemy.rect.y,
                        enemy.rect.width, enemy.rect.height)
        )

    # Jogador
    shadow = pygame.Rect(player.rect.x - camera_x + 5, player.rect.y + 5,
                         player.rect.width, player.rect.height)
    pygame.draw.rect(screen, DARK, shadow)

    pygame.draw.rect(
        screen,
        player.color,
        pygame.Rect(player.rect.x - camera_x, player.rect.y,
                    player.rect.width, player.rect.height)
    )

    # Coletáveis
    for collectible in collectibles:
        collectible.draw(screen, camera_x)

    # Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # --------------------
    # GAME OVER
    # --------------------
    if game_over:
        text = font.render("GAME OVER", True, BLACK)
        screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 60))

        restart_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
        exit_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50)

        pygame.draw.rect(screen, GREEN, restart_rect)
        pygame.draw.rect(screen, RED, exit_rect)

        screen.blit(font.render("REINICIAR", True, BLACK),
                    (restart_rect.x + 20, restart_rect.y + 10))
        screen.blit(font.render("SAIR", True, BLACK),
                    (exit_rect.x + 60, exit_rect.y + 10))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if mouse_click:
            if restart_rect.collidepoint(mouse_pos):
                # RESET TOTAL
                player.rect.x = 100
                player.rect.y = HEIGHT - 100
                player.velocity_y = 0
                score = 0
                game_over = False
                game_won = False  # ✅ garante que sai do estado de vitória também

                for enemy in enemies:
                    enemy.reset()

                for collectible in collectibles:
                    collectible.collected = False

            elif exit_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    # --------------------
    # VITÓRIA (GAME WON)
    # --------------------
    if game_won:
        restart_rect, exit_rect = draw_game_won(screen, font, WIDTH, HEIGHT)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if mouse_click:
            if restart_rect.collidepoint(mouse_pos):
                # RESET TOTAL
                player.rect.x = 100
                player.rect.y = HEIGHT - 100
                player.velocity_y = 0
                score = 0
                game_over = False
                game_won = False

                for enemy in enemies:
                    enemy.reset()

                for collectible in collectibles:
                    collectible.collected = False

            elif exit_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    pygame.display.flip()

pygame.quit()
sys.exit()
