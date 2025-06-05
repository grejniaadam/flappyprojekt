import pygame
import sys
import random
import time

pygame.init()

WIDTH = 400
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Flappy Janusz')

floor_height = 50
floor_y = HEIGHT - floor_height

font = pygame.font.SysFont("comicsans", 24)
big_font = pygame.font.SysFont("comicsans", 32)
high_score = 0
game_active = False


class Bird:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
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

    def draw(self, screen, color):
        pygame.draw.circle(
            screen, color, (int(self.x), int(self.y)), self.radius)


class Coin:
    def __init__(self, x, y, radius=8):
        self.x = x
        self.y = y
        self.radius = radius
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, (255, 215, 0),
                               (int(self.x), int(self.y)), self.radius)

    def check_collision(self, bird):
        distance = ((self.x - bird.x) ** 2 + (self.y - bird.y) ** 2) ** 0.5
        if distance < self.radius + bird.radius and not self.collected:
            self.collected = True
            return True
        return False


class Pipe:
    def __init__(self, x, width, gap_height, speed):
        self.x = x
        self.width = width
        self.gap_height = gap_height
        self.speed = speed
        self.gap_y = random.randint(100, HEIGHT - floor_height - 100)
        self.scored = False

        coin_y = random.randint(
            self.gap_y + 10, self.gap_y + self.gap_height - 10)
        self.coin = Coin(self.x + self.width // 2, coin_y)

    def update(self):
        self.x -= self.speed

        if self.x + self.width < 0:
            self.x = WIDTH
            self.gap_y = random.randint(100, HEIGHT - floor_height - 100)
            self.scored = False
            coin_y = random.randint(
                self.gap_y + 10, self.gap_y + self.gap_height - 10)
            self.coin = Coin(self.x + self.width // 2, coin_y)

        self.coin.x = self.x + self.width // 2

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_y))
        pygame.draw.rect(screen, GREEN, (
            self.x, self.gap_y + self.gap_height,
            self.width, HEIGHT - self.gap_y - self.gap_height - floor_height))

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


def draw_start_menu():
    screen.fill(WHITE)
    title = big_font.render("FLAPPY JANUSZ", True, BLUE)
    start = font.render("SPACJA = START", True, (0, 0, 0))
    hs = font.render(f"REKORD: {high_score}", True, (100, 0, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
    screen.blit(start, (WIDTH // 2 - start.get_width() // 2, 250))
    screen.blit(hs, (WIDTH // 2 - hs.get_width() // 2, 300))
    pygame.display.update()


def draw_game_over(score):
    screen.fill(WHITE)
    msg = big_font.render("JANUSZ JEBNĄŁ W RURĘ!", True, (200, 0, 0))
    wynik = font.render(f"WYNIK: {score}", True, (0, 0, 0))
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 200))
    screen.blit(wynik, (WIDTH // 2 - wynik.get_width() // 2, 250))
    pygame.display.update()


# === POCZĄTKOWY STAN ===
bird = Bird(50, HEIGHT // 2, 15)
pipe = Pipe(WIDTH, 60, 150, 3)
score = 0

running = True
while running:
    clock.tick(FPS)

    if not game_active:
        draw_start_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird = Bird(50, HEIGHT // 2, 15)
                pipe = Pipe(WIDTH, 60, 150, 3)
                score = 0
                game_active = True
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    bird.update(floor_y)
    pipe.update()
    collision = pipe.check_collision(bird)

    if pipe.coin.check_collision(bird):
        score += 1
        print("💰 MONETA ZEBRANA! +1 punkt")

    if not pipe.scored and pipe.x + pipe.width < bird.x:
        score += 1
        pipe.scored = True

    if collision == "hit":
        print("💀 JANUSZ WJEBANY W RURĘ – GAME OVER")
        if score > high_score:
            high_score = score
        draw_game_over(score)
        time.sleep(2)
        game_active = False
        continue

    elif collision == "bounce":
        print("🟡 JANUSZ OTARŁ SIĘ O RURĘ – ODBICIE")
        bird.velocity = -bird.velocity * 0.5

    screen.fill(WHITE)
    bird.draw(screen, BLUE)
    pipe.draw(screen)
    pipe.coin.draw(screen)
    pygame.draw.rect(screen, (100, 100, 100),
                     (0, floor_y, WIDTH, floor_height))
    score_text = font.render(f'WYNIK: {score}', True, BLUE)
    screen.blit(score_text, (10, 10))
    pygame.display.update()

pygame.quit()
sys.exit()
