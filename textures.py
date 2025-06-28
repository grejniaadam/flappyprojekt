import pygame
import settings
import os

class Textures:
    # Definiujemy tylko te przyciski, których faktycznie używamy
    BUTTON_EASY = None
    BUTTON_MEDIUM = None
    BUTTON_HARD = None
    BUTTON_RANDOM = None
    BUTTON_MENU = None
    BUTTON_RESTART = None
    
    # Pozostałe atrybuty
    PIPE_BODY = None
    PIPE_END = None
    PIPE_END_FLIPPED = None
    COIN = None
    BIRD = None
    BACKGROUND = None
    FLOOR = None

    @classmethod
    def load(cls):
        # Ustawiamy jednolity rozmiar dla przycisków
        button_size = (220, 55)

        # --- WCZYTYWANIE NOWYCH PRZYCISKÓW ---
        # Menu główne
        cls.BUTTON_EASY = pygame.transform.scale(pygame.image.load(os.path.join(settings.ASSETS_DIR, "easy.png")).convert_alpha(), button_size)
        cls.BUTTON_MEDIUM = pygame.transform.scale(pygame.image.load(os.path.join(settings.ASSETS_DIR, "medium.png")).convert_alpha(), button_size)
        cls.BUTTON_HARD = pygame.transform.scale(pygame.image.load(os.path.join(settings.ASSETS_DIR, "hard.png")).convert_alpha(), button_size)
        cls.BUTTON_RANDOM = pygame.transform.scale(pygame.image.load(os.path.join(settings.ASSETS_DIR, "random.png")).convert_alpha(), button_size)

        # Menu końca gry
        cls.BUTTON_MENU = pygame.transform.scale(pygame.image.load(os.path.join(settings.ASSETS_DIR, "button_menu.png")).convert_alpha(), button_size)
        cls.BUTTON_RESTART = pygame.transform.scale(pygame.image.load(os.path.join(settings.ASSETS_DIR, "button_reset.png")).convert_alpha(), button_size)
        
        # Reszta zasobów gry
        pipe_body_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "pipe.png")).convert_alpha()
        pipe_end_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "pipe_end.png")).convert_alpha()
        coin_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "coin.png")).convert_alpha()
        bird_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "bird.png")).convert_alpha()
        background_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "background1.png")).convert_alpha()
        floor_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "floor.png")).convert_alpha()
        
        size = 50
        body_height = int(pipe_body_raw.get_height() * (size / pipe_body_raw.get_width()))
        end_height = int(pipe_end_raw.get_height() * (size / pipe_end_raw.get_width()))

        cls.PIPE_BODY = pygame.transform.scale(pipe_body_raw, (size, body_height))
        cls.PIPE_END = pygame.transform.scale(pipe_end_raw, (size, end_height))
        cls.PIPE_END_FLIPPED = pygame.transform.flip(cls.PIPE_END, False, True)
        cls.COIN = pygame.transform.scale(coin_raw, (size/3, size/3))
        cls.BIRD = pygame.transform.scale(bird_raw, (size*0.9, size*0.8))
        cls.BACKGROUND = pygame.transform.scale(background_raw, (settings.WIDTH, settings.HEIGHT))
        cls.FLOOR = pygame.transform.scale(floor_raw, (settings.WIDTH+1, 100))
