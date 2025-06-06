import pygame

import time
import settings
from game_objects import Bird, Pipe


# Klasa Game - główna klasa
class Game:
    def __init__(self):
        # Inicjalizacja pygame i okna
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Flappy Janusz")

        # Inicjalizacja stnu gry
        self.game_active = False
        self.high_score = 0
        self.score = 0  

        self.title = settings.big_font.render("FLAPPY JANUSZ", True, settings.BLUE)
        self.start_game_title = settings.font.render("SPACAJA = START", True, settings.BLUE)

        # Tworzenie obiektów
        self.bird = Bird(50, settings.HEIGHT // 2, 15)
        self.pipe = Pipe(settings.WIDTH, 60, 150, 3)

    def draw_start_menu(self):
        self.screen.fill((settings.WHITE))
        highScore = settings.font.render(f"REKORD: {self.high_score}", True, (0, 0, 0))
        self.screen.blit(self.title, (settings.WIDTH // 2 - self.title.get_width() // 2, 150))
        self.screen.blit(self.start_game_title, (settings.WIDTH // 2 - self.start_game_title.get_width() // 2, 300))
        self.screen.blit(highScore, (settings.WIDTH // 2 - highScore.get_width // 2, 400))
        pygame.display.update()

    def draw_game_over(self):
        self.screen.fill((settings.WHITE))
        msg_if_bird_dead = settings.big_font.render("JANUSZ JEBNĄŁ W RURĘ!", True, (200, 0, 0))
        end_score = settings.font.render(f"WYNIK: {self.score}", True, (0, 0, 0))
        self.screen.blit(msg_if_bird_dead, (settings.WIDTH // 2 - self.get_width() // 2, 150))
        self.screen.blit(end_score, (settings.WIDTH // 2 - self.title.get_width() // 2, 300))
        pygame.display.update()

    def run(self):
        running = True
        while True:
            self.clock.tick(settings.FPS)

            if not self.game_active:
                self.draw_start_menu

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump()

            self.bird.update(settings.floor_y)
            self.pipe.update()
            collision = self.pipe.check_collision(self.bird)

            if self.pipe.coin.check_collision(self.bird):
                self.score += 1
                print("💰 MONETA ZEBRANA! +1 punkt")

            if not self.pipe.scored and self.pipe.x + self.pipe.width < self.bird.x:
                self.score += 1
                self.pipe.scored = True

            if collision == "hit":
                print("💀 JANUSZ WJEBANY W RURĘ – GAME OVER")
                if self.score > self.high_score:
                    self.high_score = self.fscore
                self._draw_game_over(self.score)
                time.sleep(2)
                self.game_active = False
                continue

            elif collision == "bounce":
                print("🟡 JANUSZ OTARŁ SIĘ O RURĘ – ODBICIE")
                self.bird.velocity = -self.bird.velocity * 0.5

            self.screen.fill(settings.WHITE)
            self.bird.draw(self.screen, settings.BLUE)
            self.pipe.draw(self.screen)
            self.pipe.coin.draw(self.screen)
            pygame.draw.rect(self.screen, (100, 100, 100), (0, settings.floor_y, settings.WIDTH, settings.floor_height))
            score_text = settings.font.render(f"WYNIK: {self.score}", True, settings.BLUE)
            self.screen.blit(score_text, (10, 10))
            pygame.display.update()


game = Game()
game.run()
