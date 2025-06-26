# Plik: main.py
import pygame
import time
import settings
from game_objects import Bird, Heavy_bird, Light_Bird, Random_Bird, Pipe
from strategies import StaticCoinStrategy, VerticalCoinStrategy, StaticPipeStrategy, VerticalPipeStrategy
from exceptions import InvalidPipeConfigError

# Klasa Game - główna klasa
class Game:
    def __init__(self):
        """Główne ustawienia gry"""
        # Inicjalizacja pygame i okna
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Flappy Janusz")

        # Inicjalizacja stanu gry
        self.game_active = False
        self._high_score = 0
        self._score = 0

        self.title = settings.big_font.render("FLAPPY JANUSZ", True, settings.BLUE)
        self.start_game_title = settings.font.render("SPACAJA = START", True, settings.BLUE)

        # Tworzymy obiekty (Bird i Pipe)
        self._reset_game()

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, value):
        # print(f"--- JESTEM W SETTERZE --- {value}")
        if value > 0:
            self._score = value
        else:
            self._score = 0

        if self._score > self._high_score:
            self._high_score = self._score
     

    def _draw_start_menu(self):
        """Metoda do 'rysowania' głównego menu"""
        self.screen.fill((settings.WHITE))

        highScore = settings.font.render(f"REKORD: {self._high_score}", True, (0, 0, 0))

        title_rect = self.title.get_rect(center=(settings.WIDTH // 2, 150))
        start_game_rect = self.start_game_title.get_rect(center=(settings.WIDTH // 2, 300))
        highScore_rect = highScore.get_rect(center=(settings.WIDTH // 2, 400))

        self.screen.blit(self.title, title_rect)
        self.screen.blit(self.start_game_title, start_game_rect)
        self.screen.blit(highScore, highScore_rect)
        pygame.display.update()

    def _draw_game_over(self):
        """Metoda do 'rysowania' informacji po zakończeniu gry"""
        self.screen.fill((settings.WHITE))

        msg_if_bird_dead = settings.big_font.render("JANUSZ JEBNĄŁ W RURĘ!", True, (200, 0, 0))
        end_score = settings.font.render(f"WYNIK: {self._score}", True, (0, 0, 0))

        msg_rect = msg_if_bird_dead.get_rect(center=(settings.WIDTH // 2, 200))
        score_rect = end_score.get_rect(center=(settings.WIDTH // 2, 250))

        self.screen.blit(msg_if_bird_dead, msg_rect)
        self.screen.blit(end_score, score_rect)
        pygame.display.update()
 
    def _reset_game(self): 
        """Metoda do resetowania stanu gry"""
        self.bird = Bird(50, settings.HEIGHT // 2, 15)

        try:
            """Statyczne rury"""
            movement_pipe = StaticPipeStrategy()

            """Ruchome rury"""
            # movement_pipe = VerticalPipeStrategy()

            self.pipe = Pipe(settings.WIDTH, width=60, gap_height=150, speed=3, movement_strategy=movement_pipe)
 
        except InvalidPipeConfigError as e:
            print(f"Błąd konfiguracji! {e}")
            print("Gra nie może zostać poprawnie uruchomiona")
            pygame.quit()
            exit()

        self.score = 0
        

    def _run(self):
        running = True
        while running:
            self.clock.tick(settings.FPS)

            if self.game_active:
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

                if not self.pipe.scored and self.pipe.x + self.pipe.width < self.bird.x:
                    self.pipe.scored = True

                if collision == "hit":
                    self._draw_game_over()
                    time.sleep(2)
                    self.game_active = False

                self.screen.fill(settings.WHITE)
                self.bird.draw(self.screen)
                self.pipe.draw(self.screen)
                self.pipe.coin.draw(self.screen)
                pygame.draw.rect(self.screen, (100, 100, 100), (0, settings.floor_y, settings.WIDTH, settings.floor_height))
                score_text = settings.font.render(f"WYNIK: {self.score}", True, settings.BLUE)
                self.screen.blit(score_text, (10, 10))
            else:
                self._draw_start_menu()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self._reset_game()
                            self.game_active = True
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game._run()
