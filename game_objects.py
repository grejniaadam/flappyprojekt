import pygame
import random
import settings
import math
import os
from strategies import PipeMovementStrategy, CoinMovementStrategy
from exceptions import InvalidPipeConfigError
from textures import Textures
import pygame.mixer

""" Plik odpowiedzialny za wszystkie obiekty w grze
    Ptaki, rury, monety, tło i podłoga """

class GameObject:
    """Abstrakcyjna lasa bazowa dla wszystkich obiektów w grze - dziedziczą i nadpisują z niej metody"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def draw(self, screen):
        pass

    def update(self):
        pass

class Bird(GameObject):
    """Główna klasa tworząca ptaka - zachowanie i fizyka"""
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius
        self.velocity = -5
        self.gravity = 0.3
        self.jump_strength = -5
        self.color = settings.BLUE
        self.flap_sound = pygame.mixer.Sound(os.path.join(settings.ASSETS_DIR, "flap.wav"))

    def jump(self):
        """Metoda wykonująca skok ptaka"""
        self.velocity += self.jump_strength
        self.flap_sound.play()
        self.flap_sound.set_volume(0.3)

    def draw(self, screen):
        """Rysowanie grafiki ptaka na ekranie"""
        bird_image = Textures.BIRD
        bird_rect = bird_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(bird_image, bird_rect)

    def update(self):
        """Aktualizacaj pozycji ptaka"""
        self.velocity += self.gravity
        self.y += self.velocity

"""Potomne klasy ptaka - dziedziczenie z Bird"""
class Heavy_bird(Bird):
    """Cięzki ptak - trudny poziom"""
    gravity = 0.5
    jump_strength = -7

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.gravity = Heavy_bird.gravity
        self.jump_strength = Heavy_bird.jump_strength
        self.color = settings.RED

class Light_Bird(Bird):
    """Lekki ptak - łatwy poziom"""
    gravity = 0.2
    jump_strength = -4

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.gravity = Light_Bird.gravity
        self.jump_strength = Light_Bird.jump_strength
        self.color = settings.ORANGE

class Random_Bird(Bird):
    """Ptak z losowymi parametrami - poziom losowy"""
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.gravity = random.uniform(0.2, 0.7)
        self.jump_strength = random.uniform(-8.0, -4.0)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))


class Coin(GameObject):
    """Klasa reprezentująca monetę, którą gracz może zbierać w grze"""
    def __init__(self, x, y, movement_strategy, radius=None):
        super().__init__(x)
        self.y = y
        self.collected = False
        self.color = settings.YELLOW
        self.movement_strategy = movement_strategy
        self.coin_sound = pygame.mixer.Sound(os.path.join(settings.ASSETS_DIR, "coin.wav"))

        if radius is None:
            self.radius = Textures.COIN.get_width() // 2
        else:
            self.radius = radius

        self.initial_y = y

    def update(self, pipe):
        """Aktualizacja pozycji zmnety zależna od wybranej strategii ruchu"""
        self.movement_strategy.update(self, pipe)

    def draw(self, screen):
        """Rysowanie monety"""
        if not self.collected:
            screen.blit(Textures.COIN, (self.x - self.radius, self.y - self.radius))

    def check_collision(self, bird):
        """Wychwytuje kolizje ptaka z monetą i zwraca True jeśli do niej doszło"""
        distance = ((self.x - bird.x) ** 2 + (self.y - bird.y) ** 2) ** 0.5
        if distance <= self.radius + bird.radius and not self.collected:
            self.collected = True
            self.coin_sound.play()
            return True
        return False

class Pipe(GameObject):
    """Klasa reprezentująca rurę - przeszkodę do pokonania"""
    def __init__(self, x, width, gap_height, speed,
                 movement_strategy: PipeMovementStrategy,
                 coin_strategy: CoinMovementStrategy,
                 pipe_img=None,
                 pipe_end_img=None,
                 pipe_end_flipped_img=None):
        super().__init__(x)
        self.crash_sound = pygame.mixer.Sound(os.path.join(settings.ASSETS_DIR, "crash.wav"))

        if gap_height <= 0:
            raise InvalidPipeConfigError(f"Wysokość przerwy (gap_height) musi być dodatnia, a jest: {gap_height}")
        if gap_height >= settings.HEIGHT - settings.floor_height:
             raise InvalidPipeConfigError("Wysokość przerwy (gap_height) jest większa niż dostępna wysokość ekranu.")

        self.width = width
        self.gap_height = gap_height
        self.speed = speed
        self.scored = False
        self.movement_strategy = movement_strategy
        self.coin_strategy = coin_strategy

        self.pipe_img = pipe_img or Textures.PIPE_BODY
        self.pipe_end_img = pipe_end_img or Textures.PIPE_END
        self.pipe_end_flipped_img = pipe_end_flipped_img or Textures.PIPE_END_FLIPPED

        min_y = 100
        max_y = settings.HEIGHT - settings.floor_height - self.gap_height - 100
        self.gap_y = random.randint(min_y, max_y)
        self.initial_gap_y = self.gap_y
        self._create_coin()

    def update(self):
        """Aktualizuje pozycję rury"""
        self.movement_strategy.update(self)

        if self.x + self.width < 0:
            self.x = settings.WIDTH
            min_y = 100
            max_y = settings.HEIGHT - settings.floor_height - self.gap_height - 100
            self.gap_y = random.randint(min_y, max_y)
            self.initial_gap_y = self.gap_y
            self.scored = False
            self._create_coin()

        self.coin.x = self.x + self.width // 2
        self.coin.update(self)

    def _create_coin(self):
        """Tworzy monetę między rurami"""
        coin_y = random.randint(self.gap_y + 40, self.gap_y + self.gap_height - 40)
        self.coin = Coin(self.x + self.width // 2, coin_y, movement_strategy=self.coin_strategy)

    def draw(self, screen):
        """Rysuje rurę górną i dolną"""
        # GÓRNA rura
        y = self.gap_y - self.pipe_end_img.get_height()
        while y > -self.pipe_img.get_height():
            screen.blit(self.pipe_img, (self.x, y))
            y -= self.pipe_img.get_height()
        screen.blit(self.pipe_end_flipped_img, (self.x, self.gap_y - self.pipe_end_img.get_height()))

        # DOLNA rura
        bottom_y = self.gap_y + self.gap_height
        y = bottom_y
        while y < settings.HEIGHT - settings.floor_height:
            screen.blit(self.pipe_img, (self.x, y))
            y += self.pipe_img.get_height()
        screen.blit(self.pipe_end_img, (self.x, bottom_y - 1))  # -1 żeby się ładnie stykało

    def check_collision(self, bird):
        """"Spradza czy doszło do kolizji ptaka z rurą"""
        bird_top = bird.y - bird.radius
        bird_bottom = bird.y + bird.radius
        bird_left = bird.x - bird.radius
        bird_right = bird.x + bird.radius
        pipe_right = self.x + self.width
        pipe_left = self.x
        in_x_range = bird_right > pipe_left and bird_left < pipe_right
        in_gap = bird_top > self.gap_y and bird_bottom < self.gap_y + self.gap_height
        
        if in_x_range and (abs(bird_top - self.gap_y) < 10 or abs(bird_bottom - (self.gap_y + self.gap_height)) < 10):
            return "bounce"
        if in_x_range and not in_gap:
            self.crash_sound.play()
            return "hit"
        return "clear"
    
    @classmethod
    def create_easy_pipe(cls, movement_strategy, coin_strategy):
        """Alternatywny konstruktor do tworzenia predefiniowanej 'łatwej' rury."""
        # Wywołujemy główny konstruktor __init__, przekazując wszystkie potrzebne strategie
        return cls(x=settings.WIDTH, width=80, gap_height=200, 
                   speed=2,movement_strategy=movement_strategy,
                   coin_strategy=coin_strategy)

class Background:
    """Klasa zarządzająca tłem gry"""
    def __init__(self, image=None):
        self.image = image if image else Textures.BACKGROUND
        self.time = 0
        self.base_x = 0
        self.base_y = 0

    def update(self):
        """Nadaje efekt bujania się tła"""
        self.time += 0.05
        self.offset_x = math.sin(self.time * 0.8) * 5 + math.sin(self.time * 1.3) * 2
        self.offset_y = math.cos(self.time * 0.6) * 3 + math.sin(self.time * 0.9) * 2

    def draw(self, screen):
        """Rysuje tło z przesunieciem animacji"""
        screen.blit(self.image, (self.base_x + self.offset_x, self.base_y + self.offset_y))

class Floor:
    """"Klasa zarządzająca podłogą i jej ruchem"""
    def __init__(self, speed):
        self.image = Textures.FLOOR
        self.speed = speed
        self.x1 = 0
        self.x2 = settings.WIDTH

    def update(self):
        """Przesuwa podłogę w lewo"""
        self.x1 -= self.speed
        self.x2 -= self.speed

        # Jeśli jedna z tekstur wyleci poza ekran, przesuń ją na prawo
        if self.x1 <= -settings.WIDTH:
            self.x1 = self.x2 + settings.WIDTH
        if self.x2 <= -settings.WIDTH:
            self.x2 = self.x1 + settings.WIDTH

    def draw(self, screen):
        """Rysuje dwa fragmenty podłogi tworząc efekt przesuwania"""
        y = settings.floor_y
        screen.blit(self.image, (self.x1, y))
        screen.blit(self.image, (self.x2, y))
