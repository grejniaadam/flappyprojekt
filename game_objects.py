import pygame
import random
import settings
import math
from strategies import PipeMovementStrategy, StaticCoinStrategy, VerticalCoinStrategy, CoinMovementStrategy
from exceptions import InvalidPipeConfigError
from textures import Textures

class GameObject:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def draw(self, screen):
        pass

    def update(self):
        pass

class Bird(GameObject):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius
        self.velocity = -5
        self.gravity = 0.3
        self.jump_strength = -5
        self.color = settings.BLUE

    def jump(self):
        self.velocity += self.jump_strength

    def draw(self, screen):
        bird_image = Textures.BIRD
        bird_rect = bird_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(bird_image, bird_rect)

    def update(self, floor_y):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y + self.radius > floor_y:
            self.y = floor_y - self.radius
            self.velocity = 0
    
        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity = 0

class Heavy_bird(Bird):
    gravity = 0.5
    jump_strength = -7

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.gravity = Heavy_bird.gravity
        self.jump_strength = Heavy_bird.jump_strength
        self.color = settings.RED

class Light_Bird(Bird):
    gravity = 0.2
    jump_strength = -4

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.gravity = Light_Bird.gravity
        self.jump_strength = Light_Bird.jump_strength
        self.color = settings.ORANGE

class Random_Bird(Bird):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.gravity = random.uniform(0.2, 0.7)
        self.jump_strength = random.uniform(-8.0, -4.0)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))


class Coin(GameObject):
    def __init__(self, x, y, movement_strategy, radius=None):
        super().__init__(x)
        self.y = y
        self.collected = False
        self.color = settings.YELLOW
        self.movement_strategy = movement_strategy

        if radius is None:
            self.radius = Textures.COIN.get_width() // 2
        else:
            self.radius = radius

        self.initial_y = y

    def update(self, pipe):
        self.movement_strategy.update(self, pipe)

    def draw(self, screen):
        if not self.collected:
            screen.blit(Textures.COIN, (self.x - self.radius, self.y - self.radius))

    def check_collision(self, bird):
        distance = ((self.x - bird.x) ** 2 + (self.y - bird.y) ** 2) ** 0.5
        if distance <= self.radius + bird.radius and not self.collected:
            self.collected = True
            return True
        return False

class Pipe(GameObject):
    def __init__(self, x, width, gap_height, speed, movement_strategy: PipeMovementStrategy):
        super().__init__(x)
        if gap_height <= 0:
            raise InvalidPipeConfigError(f"Wysokość przerwy (gap_height) musi być dodatnia, a jest: {gap_height}")
        if gap_height >= settings.HEIGHT - settings.floor_height:
             raise InvalidPipeConfigError("Wysokość przerwy (gap_height) jest większa niż dostępna wysokość ekranu.")

        self.width = width
        self.gap_height = gap_height
        self.speed = speed
        self.scored = False
        self.movement_strategy = movement_strategy
        min_y = 100
        max_y = settings.HEIGHT - settings.floor_height - self.gap_height - 100
        self.gap_y = random.randint(min_y, max_y)
        self.initial_gap_y = self.gap_y
        self._create_coin()

    def update(self):
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
        coin_y = random.randint(self.gap_y + 40, self.gap_y + self.gap_height - 40)
        """Statyczna moneta"""
        #coin_strategy = StaticCoinStrategy()

        """Ruchoma moneta"""
        coin_strategy = VerticalCoinStrategy(vertical_speed=1, move_range=25)

        self.coin = Coin(self.x + self.width // 2, coin_y, movement_strategy=coin_strategy)

    def draw(self, screen):
        # GÓRNA rura (ciało)
        y = self.gap_y - Textures.PIPE_END.get_height()
        while y > -Textures.PIPE_BODY.get_height():
            screen.blit(Textures.PIPE_BODY, (self.x, y))
            y -= Textures.PIPE_BODY.get_height()
        screen.blit(Textures.PIPE_END_FLIPPED, (self.x, self.gap_y - Textures.PIPE_END.get_height()))

        # DOLNA rura (ciało)
        bottom_y = self.gap_y + self.gap_height
        y = bottom_y
        while y < settings.HEIGHT - settings.floor_height:
            screen.blit(Textures.PIPE_BODY, (self.x, y))
            y += Textures.PIPE_BODY.get_height()
        screen.blit(Textures.PIPE_END, (self.x, bottom_y - 1))  # -1 żeby się ładnie stykało


    def check_collision(self, bird):
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
            return "hit"
        return "clear"

class Background:
    def __init__(self):
        self.image = Textures.BACKGROUND
        self.time = 0
        self.base_x = 0
        self.base_y = 0

    def update(self):
        #efekt bujania sie tla
        self.time += 0.05  # tempo animacji
        self.offset_x = math.sin(self.time * 0.8) * 5 + math.sin(self.time * 1.3) * 2
        self.offset_y = math.cos(self.time * 0.6) * 3 + math.sin(self.time * 0.9) * 2

    def draw(self, screen):
        screen.blit(self.image, (self.base_x + self.offset_x, self.base_y + self.offset_y))

class Floor:
    def __init__(self, speed):
        self.image = Textures.FLOOR
        self.speed = speed
        self.x1 = 0
        self.x2 = settings.WIDTH

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        # Jeśli jedna z tekstur wyleci poza ekran, przesuń ją na prawo
        if self.x1 <= -settings.WIDTH:
            self.x1 = self.x2 + settings.WIDTH
        if self.x2 <= -settings.WIDTH:
            self.x2 = self.x1 + settings.WIDTH

    def draw(self, screen):
        y = settings.floor_y
        screen.blit(self.image, (self.x1, y))
        screen.blit(self.image, (self.x2, y))