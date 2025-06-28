from abc import ABC, abstractmethod
import settings
import pygame
import time
from strategies import StaticPipeStrategy, VerticalPipeStrategy, StaticCoinStrategy, VerticalCoinStrategy
from exceptions import InvalidPipeConfigError
from game_objects import Bird, Light_Bird, Heavy_bird, Random_Bird, Pipe, Coin
from commands import JumpCommand
from textures import Textures

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
    """Ostateczne, działające menu gry z 5 nowymi przyciskami."""
    def __init__(self, game):
        super().__init__(game)
        button_width, button_height = 220, 55
        center_x = settings.WIDTH / 2

        # Definiujemy 5 prostokątów dla naszych przycisków
        rect_start = pygame.Rect(0, 0, button_width, button_height)
        rect_start.center = (center_x, 180)

        rect_easy = pygame.Rect(0, 0, button_width, button_height)
        rect_easy.center = (center_x, 240)

        rect_medium = pygame.Rect(0, 0, button_width, button_height)
        rect_medium.center = (center_x, 300)

        rect_hard = pygame.Rect(0, 0, button_width, button_height)
        rect_hard.center = (center_x, 360)
        
        rect_random = pygame.Rect(0, 0, button_width, button_height)
        rect_random.center = (center_x, 420)

        # Przypisujemy Twoje nowe grafiki i akcje do każdego przycisku
        self.buttons = [
            # {"image": Textures.BUTTON_START, "rect": rect_start, "action": "start_medium"}, # START domyślnie uruchamia poziom średni
            {"image": Textures.BUTTON_EASY, "rect": rect_easy, "action": "start_easy"},
            {"image": Textures.BUTTON_MEDIUM, "rect": rect_medium, "action": "start_medium"},
            {"image": Textures.BUTTON_HARD, "rect": rect_hard, "action": "start_hard"},
            {"image": Textures.BUTTON_RANDOM, "rect": rect_random, "action": "start_random"}
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        if button['rect'].collidepoint(event.pos):
                            if button['action'] == 'start_easy':
                                self.game.change_state(PlayingState(self.game, 'easy'))
                            elif button['action'] == 'start_medium':
                                self.game.change_state(PlayingState(self.game, 'medium'))
                            elif button['action'] == 'start_hard':
                                self.game.change_state(PlayingState(self.game, 'hard'))
                            elif button['action'] == 'start_random':
                                self.game.change_state(PlayingState(self.game, 'random'))

    def update(self):
        pass

    def draw(self, screen):
        # Rysowanie tytułu i rekordu
        title_rect = self.game.title.get_rect(center=(settings.WIDTH // 2, 80))
        screen.blit(self.game.title, title_rect)
        highScore = settings.font.render(f"REKORD: {self.game._high_score}", True, settings.BLACK)
        highScore_rect = highScore.get_rect(center=(settings.WIDTH // 2, 520))
        screen.blit(highScore, highScore_rect)

        # Rysowanie gotowych przycisków
        for button in self.buttons:
            screen.blit(button["image"], button["rect"])

class PlayingState(State):
    def __init__(self, game, difficulty):
        super().__init__(game)
        self.difficulty = difficulty
        self.game._reset_game_logic(self.difficulty)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                command = JumpCommand(self.game.bird)
                command.execute()

    def update(self):
        # self.game.bird.update(settings.floor_y)
        self.game.bird.update()
        self.game.pipe.update()
        
        collision = self.game.pipe.check_collision(self.game.bird)
        if self.game.pipe.coin.check_collision(self.game.bird):
            self.game.score += 1
        
        if not self.game.pipe.scored and self.game.pipe.x + self.game.pipe.width < self.game.bird.x:
            self.game.pipe.scored = True
            self.game.pipes_passed += 1

        bird_top = self.game.bird.y - self.game.bird.radius
        bird_bottom = self.game.bird.y + self.game.bird.radius

        if collision == "hit" or bird_bottom > settings.floor_y or bird_bottom <- 0:
            self.game.pipe.crash_sound.play()
            self.game.change_state(GameOverState(self.game))

    def draw(self, screen):
        
        self.game.bird.draw(screen)
        self.game.pipe.draw(screen)
        self.game.pipe.coin.draw(screen)
        
        score_text = settings.font.render(f"Monety: {self.game.score}", True, settings.BLUE)
        screen.blit(score_text, (10, 10))
        
        pipes_text = settings.font.render(f"Rury: {self.game.pipes_passed}", True, settings.BLUE)
        pipes_text_rect = pipes_text.get_rect(topright=(settings.WIDTH - 10, 10))
        screen.blit(pipes_text, pipes_text_rect)


class GameOverState(State):
    def __init__(self, game):
        super().__init__(game)
        print("Koniec Gry")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.change_state(MenuState(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(settings.WHITE)

        msg_if_bird_dead = settings.big_font.render("JANUSZ JEBNĄŁ W RURĘ!", True, (200, 0, 0))
        end_score = settings.font.render(f"WYNIK: {self.game._score}", True, (0, 0, 0))
        back_to_menu_text = settings.font.render("SPACJA = POWRÓT DO MENU", True, settings.BLUE)

        msg_rect = msg_if_bird_dead.get_rect(center=(settings.WIDTH // 2, 200))
        score_rect = end_score.get_rect(center=(settings.WIDTH // 2, 250))
        back_to_menu_rect = back_to_menu_text.get_rect(center=(settings.WIDTH // 2, 350))
        
        screen.blit(msg_if_bird_dead, msg_rect)
        screen.blit(end_score, score_rect)
        screen.blit(back_to_menu_text, back_to_menu_rect)
