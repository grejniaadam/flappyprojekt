import pygame
import settings

class Textures:
    @classmethod
    def load(cls):
        pipe_body_raw = pygame.image.load("assets/pipe.png").convert_alpha()
        pipe_end_raw = pygame.image.load("assets/pipe_end.png").convert_alpha()
        coin_raw = pygame.image.load("assets/coin.png").convert_alpha()
        bird_raw = pygame.image.load("assets/bird.png").convert_alpha()

        # Skalowanie
        size = 45

        body_height = int(pipe_body_raw.get_height() * (size / pipe_body_raw.get_width()))
        end_height = int(pipe_end_raw.get_height() * (size / pipe_end_raw.get_width()))

        cls.PIPE_BODY = pygame.transform.scale(pipe_body_raw, (size, body_height))
        cls.PIPE_END = pygame.transform.scale(pipe_end_raw, (size, end_height))
        cls.PIPE_END_FLIPPED = pygame.transform.flip(cls.PIPE_END, False, True)
        cls.COIN = pygame.transform.scale(coin_raw, (size/2, size/2))
        cls.BIRD = pygame.transform.scale(bird_raw, (size*1.1, size))