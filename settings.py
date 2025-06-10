import pygame

# === USTAWIENIE OKNA I GRY ===
WIDTH = 400
HEIGHT = 600
FPS = 60
floor_height = 50
floor_y = HEIGHT - floor_height


# === KOLORY ===
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 215, 0)


# === CZCIONKI ===

pygame.font.init()
font = pygame.font.SysFont("comicsans", 24)
big_font = pygame.font.SysFont("comicsans", 30)
