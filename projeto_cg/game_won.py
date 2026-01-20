import pygame
import sys

def draw_game_won(screen, font, WIDTH, HEIGHT):
    GREEN = (60, 180, 75)
    RED = (220, 50, 50)
    BLACK = (0, 0, 0)

    # Texto principal
    text = font.render("VOCÊ GANHOU!", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 80))

    # Botões
    restart_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    exit_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)

    pygame.draw.rect(screen, GREEN, restart_rect)
    pygame.draw.rect(screen, RED, exit_rect)

    screen.blit(font.render("REINICIAR", True, BLACK),
                (restart_rect.x + 20, restart_rect.y + 10))
    screen.blit(font.render("SAIR", True, BLACK),
                (exit_rect.x + 60, exit_rect.y + 10))

    return restart_rect, exit_rect
