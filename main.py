# Plik: main.py
import pygame
import time
import settings
from game_objects import Bird, Heavy_bird, Light_Bird, Random_Bird, Pipe, Background
from strategies import StaticCoinStrategy, VerticalCoinStrategy, StaticPipeStrategy, VerticalPipeStrategy
from exceptions import InvalidPipeConfigError
from game_states import State, MenuState, PlayingState
from textures import Textures

# Klasa Game - główna klasa
class Game:
    def __init__(self):
        """Główne ustawienia gry"""
        # Inicjalizacja pygame i okna
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        Textures.load()
        self.background = Background()
        pygame.display.set_caption("Flappy Janusz")

        # Inicjalizacja stanu gry
        self.running = True
        self.state: State = None

        self._high_score = 0
        self._score = 0
        self.pipes_passed = 0
        self.bird = None
        self.pipe = None
        self.title = settings.big_font.render("FLAPPY JANUSZ", True, settings.BLUE)
        self.start_game_title = settings.font.render("SPACAJA = START", True, settings.BLUE)

        self.change_state(MenuState(self))

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

    def change_state(self, new_state: State):
        self.state = new_state

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
 
    def _reset_game_logic(self):
        """Metoda do resetowania stanu gry"""
        self.bird = Bird(50, settings.HEIGHT // 2, 15)

        try:
            """Statyczne rury"""
            #movement_pipe = StaticPipeStrategy()

            """Ruchome rury"""
            movement_pipe = VerticalPipeStrategy()

            self.pipe = Pipe(settings.WIDTH, width=60, gap_height=150, speed=3, movement_strategy=movement_pipe)
 
        except InvalidPipeConfigError as e:
            print(f"Błąd konfiguracji! {e}")
            print("Gra nie może zostać poprawnie uruchomiona")
            self.running = False

        self.score = 0
        self.pipes_passed = 0
        

    def run(self):
        while self.running:
            events = pygame.event.get()

            self.state.handle_events(events)
            self.state.update()
            self.background.update()
            self.background.draw(self.screen)
            self.state.draw(self.screen)

            pygame.display.update()
            self.clock.tick(settings.FPS)
        

if __name__ == "__main__":
    game = Game()
    game.run()
