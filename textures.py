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
    PIPE_BODY2 = None
    PIPE_END2 = None
    PIPE_END2_FLIPPED = None
    PIPE_BODY3 = None
    PIPE_END3 = None
    PIPE_END3_FLIPPED = None
    PIPE_BODY4 = None
    PIPE_END4 = None
    PIPE_END4_FLIPPED = None
    COIN = None
    BIRD = None
    BACKGROUND = None
    BACKGROUND2 = None
    BACKGROUND3 = None
    BACKGROUND4 = None
    FLOOR = None
    FLOOR2 = None
    FLOOR3 = None
    FLOOR4 = None
    LOGO = None
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
        pipe2_body_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "pipe2.png")).convert_alpha()
        pipe2_end_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "pipe_end2.png")).convert_alpha()
        pipe3_body_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "pipe3.png")).convert_alpha()
        pipe3_end_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "pipe_end3.png")).convert_alpha()
        pipe4_body_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "pipe4.png")).convert_alpha()
        pipe4_end_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "pipe_end4.png")).convert_alpha()
        coin_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "coin.png")).convert_alpha()
        bird_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "bird.png")).convert_alpha()
        background_1 = pygame.image.load(os.path.join(settings.ASSETS_DIR, "background1.png")).convert_alpha()
        background_2 = pygame.image.load(os.path.join(settings.ASSETS_DIR, "background2.png")).convert_alpha()
        background_3 = pygame.image.load(os.path.join(settings.ASSETS_DIR, "background3.png")).convert_alpha()
        background_4 = pygame.image.load(os.path.join(settings.ASSETS_DIR, "background4.png")).convert_alpha()
        floor_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "floor.png")).convert_alpha()
        floor2_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "floor2.png")).convert_alpha()
        floor3_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "floor3.png")).convert_alpha()
        floor4_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "floor4.png")).convert_alpha()
        logo_raw = pygame.image.load(os.path.join(settings.ASSETS_DIR, "logo.png")).convert_alpha()

        size = 50
        body_height = int(pipe_body_raw.get_height() * (size / pipe_body_raw.get_width()))
        end_height = int(pipe_end_raw.get_height() * (size / pipe_end_raw.get_width()))

        cls.PIPE_BODY = pygame.transform.scale(pipe_body_raw, (size, body_height))
        cls.PIPE_END = pygame.transform.scale(pipe_end_raw, (size, end_height))
        cls.PIPE_END_FLIPPED = pygame.transform.flip(cls.PIPE_END, False, True)
        cls.PIPE_BODY2 = pygame.transform.scale(pipe2_body_raw, (size, body_height))
        cls.PIPE_END2 = pygame.transform.scale(pipe2_end_raw, (size, end_height))
        cls.PIPE_END2_FLIPPED = pygame.transform.flip(cls.PIPE_END2, False, True)
        cls.PIPE_BODY3 = pygame.transform.scale(pipe3_body_raw, (size, body_height))
        cls.PIPE_END3 = pygame.transform.scale(pipe3_end_raw, (size, end_height))
        cls.PIPE_END3_FLIPPED = pygame.transform.flip(cls.PIPE_END3, False, True)
        cls.PIPE_BODY4 = pygame.transform.scale(pipe4_body_raw, (size, body_height))
        cls.PIPE_END4 = pygame.transform.scale(pipe4_end_raw, (size, end_height))
        cls.PIPE_END4_FLIPPED = pygame.transform.flip(cls.PIPE_END4, False, True)
        cls.COIN = pygame.transform.scale(coin_raw, (size/3, size/3))
        cls.BIRD = pygame.transform.scale(bird_raw, (size*0.9, size*0.8))
        cls.BACKGROUND = pygame.transform.scale(background_1, (settings.WIDTH, settings.HEIGHT))
        cls.FLOOR = pygame.transform.scale(floor_raw, (settings.WIDTH+1, 100))
        cls.FLOOR2 = pygame.transform.scale(floor2_raw, (settings.WIDTH+1, 100))
        cls.FLOOR3 = pygame.transform.scale(floor3_raw, (settings.WIDTH+1, 100))
        cls.FLOOR4 = pygame.transform.scale(floor4_raw, (settings.WIDTH+1, 100))
        cls.BACKGROUND2 = pygame.transform.scale(background_2, (settings.WIDTH, settings.HEIGHT))
        cls.BACKGROUND3 = pygame.transform.scale(background_3, (settings.WIDTH, settings.HEIGHT))
        cls.BACKGROUND4 = pygame.transform.scale(background_4, (settings.WIDTH, settings.HEIGHT))
        cls.LOGO = pygame.transform.scale(logo_raw, (300, 240))