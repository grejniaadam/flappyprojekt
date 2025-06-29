import pygame
import os

# === USTAWIENIE OKNA I GRY ===
WIDTH = 400
HEIGHT = 600
FPS = 60
floor_height = 50
floor_y = HEIGHT - floor_height #550


# === KOLORY ===
WHITE = (255, 255, 255) 
GREEN = (0, 255, 0) 
YELLOW = (255, 215, 0) 
BLUE = (0, 0, 255) 
RED = (255, 0, 0) 
ORANGE = (251, 152, 2)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)


# === CZCIONKI ===
pygame.font.init()
font = pygame.font.SysFont("comicsans", 24)
big_font = pygame.font.SysFont("comicsans", 30)


# === ŚCIŻKA DO PLIKU SETTINGS ===
# Tworzenie bezpieczych i abslutynch ścieżek do zasobów gry
# Dzięki temu pogram zadziała niezależnie od miejsca jego uruchomienia
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
