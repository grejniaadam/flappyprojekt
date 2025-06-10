import pygame
import random
import settings


class GameObject:
    def __init__(self, x=0, y=0, radius=0, test=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.test = test


    def draw(self, screen, color=settings.WHITE, radius=0):
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        pass


class Bird(GameObject):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = -5
        self.gravity = 0.3
        self.jump_strength = -5

    def jump(self):
        self.velocity += self.jump_strength

    def update(self, floor_y):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y + self.radius > floor_y:
            self.y = floor_y - self.radius
            self.velocity = 0
            print("JANUSZ WPIERDOLIŁ SIĘ W ZIEMIĘ!")
 
        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity = 0
            print("KURŁA JEBŁEM W SUFIT!")

    # def draw(self, screen, color):
    #     super().draw(screen, color, self.radius)
        # pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)


class Coin(GameObject):
    def __init__(self, x, y, radius=8):
        super().__init__(x, y, radius)
        self.collected = False

    def draw(self, screen, color):
        if not self.collected:
            super().draw(screen, color)
            # pygame.draw.circle(screen, settings.YELLOW, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, bird):
        distance = ((self.x - bird.x) ** 2 + (self.y - bird.y) ** 2) ** 0.5
        if distance < self.radius + bird.radius and not self.collected:
            self.collected = True
            return True
        return False


class Pipe(GameObject):
    def __init__(self, x, width, gap_height, speed):
        super().__init__(x)
        self.width = width
        self.gap_height = gap_height
        self.speed = speed
        self.gap_y = random.randint(100, settings.HEIGHT - settings.floor_height - 100)
        self.scored = False

        coin_y = random.randint(
            self.gap_y + 10, self.gap_y + self.gap_height - 10)
        self.coin = Coin(self.x + self.width // 2, coin_y)

    def update(self):
        self.x -= self.speed

        if self.x + self.width < 0:
            self.x = settings.WIDTH
            self.gap_y = random.randint(
                100, settings.HEIGHT - settings.floor_height - 100)
            self.scored = False
            coin_y = random.randint(
                self.gap_y + 10, self.gap_y + self.gap_height - 10)
            self.coin = Coin(self.x + self.width // 2, coin_y)

        self.coin.x = self.x + self.width // 2

    def draw(self, screen):
        pygame.draw.rect(screen, settings.GREEN, (self.x, 0, self.width, self.gap_y))
        pygame.draw.rect(screen, settings.GREEN, (self.x, self.gap_y + self.gap_height, self.width, 
                                                  settings.HEIGHT - self.gap_y - self.gap_height - settings.floor_height))

    def check_collision(self, bird):
        bird_top = bird.y - bird.radius
        bird_bottom = bird.y + bird.radius
        bird_left = bird.x - bird.radius
        bird_right = bird.x + bird.radius

        pipe_right = self.x + self.width
        pipe_left = self.x

        in_x_range = bird_right > pipe_left and bird_left < pipe_right
        in_gap = bird_top > self.gap_y and bird_bottom < self.gap_y + self.gap_height

        if in_x_range and (
                abs(bird_top - self.gap_y) < 10 or
                abs(bird_bottom - (self.gap_y + self.gap_height)) < 10):
            return "bounce"

        if in_x_range and not in_gap:
            return "hit"

        return "clear"
