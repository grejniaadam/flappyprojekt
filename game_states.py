from abc import ABC, abstractmethod
import settings
import pygame
import time
from strategies import StaticPipeStrategy, VerticalPipeStrategy, StaticCoinStrategy, VerticalCoinStrategy
from exceptions import InvalidPipeConfigError
from game_objects import Bird, Light_Bird, Heavy_bird, Random_Bird, Pipe, Coin

class State(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_events(self, events):
        """Metoda do obsługi zdarzeń(klawiatura, przyciski itp)"""
        pass

    @abstractmethod
    def update(self):
        """Aktualizacja logiki gry"""
        pass

    @abstractmethod
    def draw(self, screen):
        """Rysowanie stanu na ekranie"""
        pass


class MenuState(State):
    """Stan reprezentujący menu główne gry."""

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # print("SPACJA NACIŚNIĘTA - Zmieniam stan na PlayingState")
                    self.game.change_state(PlayingState(self.game))

    def update(self):
        pass

    def draw(self, screen):
        #screen.fill(settings.WHITE)
        
        highScore = settings.font.render(f"REKORD: {self.game._high_score}", True, (0, 0, 0))
        title_rect = self.game.title.get_rect(center=(settings.WIDTH // 2, 150))
        start_game_rect = self.game.start_game_title.get_rect(center=(settings.WIDTH // 2, 300))
        highScore_rect = highScore.get_rect(center=(settings.WIDTH // 2, 400))
        
        screen.blit(self.game.title, title_rect)
        screen.blit(self.game.start_game_title, start_game_rect)
        screen.blit(highScore, highScore_rect)

class PlayingState(State):
    def __init__(self, game):
        super().__init__(game)
        # print("PlayingState: Inicjalizuję i resetuję logikę gry...")
        self.game._reset_game_logic()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.bird.jump()

    def update(self):
        self.game.bird.update(settings.floor_y)
        self.game.pipe.update()
        
        collision = self.game.pipe.check_collision(self.game.bird)
        if self.game.pipe.coin.check_collision(self.game.bird):
            self.game.score += 1
        
        if not self.game.pipe.scored and self.game.pipe.x + self.game.pipe.width < self.game.bird.x:
            self.game.pipe.scored = True
            self.game.pipes_passed += 1

        if collision == "hit":
            # Mówimy GŁÓWNEJ grze, żeby zmieniła stan
            # TODO: W przyszłości zmienić na GameOverState
            self.game.change_state(MenuState(self.game))

    def draw(self, screen):
        #screen.fill(settings.WHITE)
        
        self.game.bird.draw(screen)
        self.game.pipe.draw(screen)
        self.game.pipe.coin.draw(screen)
        
        #pygame.draw.rect(screen, (100, 100, 100), (0, settings.floor_y, settings.WIDTH, settings.floor_height))
        score_text = settings.font.render(f"WYNIK: {self.game.score}", True, settings.BLUE)
        screen.blit(score_text, (10, 10))
        
        pipes_text = settings.font.render(f"RURY: {self.game.pipes_passed}", True, settings.BLUE)
        pipes_text_rect = pipes_text.get_rect(topright=(settings.WIDTH - 10, 10))
        screen.blit(pipes_text, pipes_text_rect)

        