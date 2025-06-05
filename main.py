import pygame
import sys
import time
import settings
from game_objects import Bird, Pipe
pygame.init()


screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Flappy Janusz')

high_score = 0
game_active = False


def draw_start_menu():
    screen.fill(settings.WHITE)
    title = settings.big_font.render("FLAPPY JANUSZ", True, settings.BLUE)
    start = settings.font.render("SPACJA = START", True, (0, 0, 0))
    hs = settings.font.render(f"REKORD: {high_score}", True, (100, 0, 0))
    screen.blit(title, (settings.WIDTH // 2 - title.get_width() // 2, 150))
    screen.blit(start, (settings.WIDTH // 2 - start.get_width() // 2, 250))
    screen.blit(hs, (settings.WIDTH // 2 - hs.get_width() // 2, 300))
    pygame.display.update()


def draw_game_over(score):
    screen.fill(settings.WHITE)
    msg = settings.big_font.render("JANUSZ JEBNĄŁ W RURĘ!", True, (200, 0, 0))
    wynik = settings.font.render(f"WYNIK: {score}", True, (0, 0, 0))
    screen.blit(msg, (settings.WIDTH // 2 - msg.get_width() // 2, 200))
    screen.blit(wynik, (settings.WIDTH // 2 - wynik.get_width() // 2, 250))
    pygame.display.update()


# === POCZĄTKOWY STAN ===
bird = Bird(50, settings.HEIGHT // 2, 15)
pipe = Pipe(settings.WIDTH, 60, 150, 3)
score = 0

running = True
while running:
    clock.tick(settings.FPS)

    if not game_active:
        draw_start_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird = Bird(50, settings.HEIGHT // 2, 15)
                pipe = Pipe(settings.WIDTH, 60, 150, 3)
                score = 0
                game_active = True
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    bird.update(settings.floor_y)
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

    screen.fill(settings.WHITE)
    bird.draw(screen, settings.BLUE)
    pipe.draw(screen)
    pipe.coin.draw(screen)
    pygame.draw.rect(screen, (100, 100, 100),
                     (0, settings.floor_y, settings.WIDTH, settings.floor_height))
    score_text = settings.font.render(f'WYNIK: {score}', True, settings.BLUE)
    screen.blit(score_text, (10, 10))
    pygame.display.update()

pygame.quit()
sys.exit()
