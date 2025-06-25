import pygame
import random
import settings
from abc import ABC, abstractmethod

class MovementStrategy(ABC):
    @abstractmethod
    def update(self, pipe):
        pass

class StaticMovmentStrategy(MovementStrategy):
    def update(self, pipe):
        pipe.x -= pipe.speed

class VerticalMovmentStrategy(MovementStrategy):
    def __init__(self, vertical_speed=1, move_range=40):
        self.vertical_speed = vertical_speed
        self.move_range = move_range
        self.direction = 1

    def update(self, pipe):
        pipe.x -= pipe.speed
        pipe.gap_y += self.vertical_speed * self.direction

        if pipe.gap_y > pipe.initial_gap_y + self.move_range or pipe.gap_y < pipe.initial_gap_y - self.move_range: 
            self.direction *= -1

        
class InvalidPipeConfigError(Exception):
    """Błąd rzucany w momencie gdy paramerty rury są nielogiczne"""
    pass

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
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

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
    def __init__(self, x, y, radius=8):
        super().__init__(x, y)
        self.radius = radius
        self.collected = False
        self.color = settings.YELLOW

    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, bird):
        distance = ((self.x - bird.x) ** 2 + (self.y - bird.y) ** 2) ** 0.5
        if distance < self.radius + bird.radius and not self.collected:
            self.collected = True
            return True
        return False

# W pliku game_objects.py

class Pipe(GameObject):
    def __init__(self, x, width, gap_height, speed, movement_strategy: MovementStrategy):
        super().__init__(x)
        self.width = width
        self.gap_height = gap_height
        self.speed = speed
        self.scored = False
        self.movement_strategy = movement_strategy

        # Losujemy pozycję przerwy i od razu zapisujemy ją jako pozycję początkową
        min_y = 100
        max_y = settings.HEIGHT - settings.floor_height - self.gap_height - 100
        self.gap_y = random.randint(min_y, max_y)
        self.initial_gap_y = self.gap_y 

        self._create_coin()

    def update(self):
        self.movement_strategy.update(self)

        if self.x + self.width < 0:
            self.x = settings.WIDTH
            # Resetujemy pozycję przerwy do nowego, losowego miejsca
            min_y = 100
            max_y = settings.HEIGHT - settings.floor_height - self.gap_height - 100
            self.gap_y = random.randint(min_y, max_y)
            self.initial_gap_y = self.gap_y 
            
            self.scored = False
            self._create_coin()

            # self.movement_strategy.reset()

        # Moneta nadal podąża za rurą
        self.coin.x = self.x + self.width // 2

    def _create_coin(self):
        coin_y = random.randint(self.gap_y + 20, self.gap_y + self.gap_height - 20)
        self.coin = Coin(self.x + self.width // 2, coin_y)

    def draw(self, screen):
        pygame.draw.rect(screen, settings.GREEN, (self.x, 0, self.width, self.gap_y))
        pygame.draw.rect(screen, settings.GREEN, (self.x, self.gap_y + self.gap_height, self.width, settings.HEIGHT - self.gap_y - self.gap_height - settings.floor_height))

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
