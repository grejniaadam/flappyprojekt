import pygame
import settings
import os

class Textures:
    BUTTON_START = None
    BUTTON_EASY = None
    BUTTON_MEDIUM = None
    BUTTON_HARD = None
    BUTTON_RANDOM = None
    PIPE_BODY = None
    PIPE_END = None
    PIPE_END_FLIPPED = None
    COIN = None
    BIRD = None
    BACKGROUND = None
    FLOOR = None

    @classmethod
    def load(cls):
        # Wczytujemy pliki, podając tylko ich NAZWĘ, a nie całą ścieżkę z "assets/"
        button_size = (220, 55)
        try:
            # Poprawione ścieżki
            # cls.BUTTON_START = pygame.transform.scale(pygame.image.load(os.path.join(settings.ASSETS_DIR, "start.png")).convert_alpha(), button_size)
            cls.BUTTON_EASY = pygame.transform.scale(pygame.image.load(os.path.join(settings.ASSETS_DIR, "easy.png")).convert_alpha(), button_size)
            cls.BUTTON_MEDIUM = pygame.transform.scale(pygame.image.load(os.path.join(settings.ASSETS_DIR, "medium.png")).convert_alpha(), button_size)
            cls.BUTTON_HARD = pygame.transform.scale(pygame.image.load(os.path.join(settings.ASSETS_DIR, "hard.png")).convert_alpha(), button_size)
            cls.BUTTON_RANDOM = pygame.transform.scale(pygame.image.load(os.path.join(settings.ASSETS_DIR, "random.png")).convert_alpha(), button_size)
            print("INFO: Wszystkie nowe grafiki przycisków załadowane pomyślnie.")
        except pygame.error as e:
            print(f"BŁĄD: Nie udało się wczytać którejś z grafik przycisków! Sprawdź nazwy plików w folderze 'assets'.")
            print(f"Szczegóły błędu: {e}")
            fallback = pygame.Surface(button_size)
            cls.BUTTON_START, cls.BUTTON_EASY, cls.BUTTON_MEDIUM, cls.BUTTON_HARD, cls.BUTTON_RANDOM = [fallback] * 5

        # Reszta tekstur - również poprawione ścieżki
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
