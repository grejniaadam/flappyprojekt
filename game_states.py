from abc import ABC, abstractmethod
import settings
import pygame
from commands import JumpCommand
from textures import Textures

""" Plik zarządzający stanem gry - implementacja wzorca State
    Definuje stany gry - Menu, Gra, Koniec gry. Zarząda też logiką każdego z nich """

def draw_text_with_shadow(screen, text, font, position, text_color, shadow_color=(0, 0, 0)):
    """Funkcja do rysowania tekstu z cieniem"""
    shadow_surface = font.render(text, True, shadow_color)
    text_surface = font.render(text, True, text_color)

    screen.blit(shadow_surface, (position[0] + 2, position[1] + 2))
    screen.blit(text_surface, position)

class State(ABC):
    """Abstrakcyjna klasa bazowa dla wszystkich stanów gry"""
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
    """Menu główne gry z 4 przyciskami wyboru poziomu."""
    def __init__(self, game):
        super().__init__(game)

        button_width, button_height = 220, 55
        center_x = settings.WIDTH / 2
        start_y = 210
        gap_y = 70

        rect_easy = pygame.Rect(0, 0, button_width, button_height)
        rect_easy.center = (center_x, start_y)

        rect_medium = pygame.Rect(0, 0, button_width, button_height)
        rect_medium.center = (center_x, start_y + gap_y)

        rect_hard = pygame.Rect(0, 0, button_width, button_height)
        rect_hard.center = (center_x, start_y + 2 * gap_y)
        
        rect_random = pygame.Rect(0, 0, button_width, button_height)
        rect_random.center = (center_x, start_y + 3 * gap_y)

        self.buttons = [
            {"image": Textures.BUTTON_EASY, "rect": rect_easy, "action": "start_easy"},
            {"image": Textures.BUTTON_MEDIUM, "rect": rect_medium, "action": "start_medium"},
            {"image": Textures.BUTTON_HARD, "rect": rect_hard, "action": "start_hard"},
            {"image": Textures.BUTTON_RANDOM, "rect": rect_random, "action": "start_random"}
        ]
        self.muted_icon_rect = pygame.Rect(settings.WIDTH - 55, settings.HEIGHT - 50, 40, 40)

    def handle_events(self, events):
        """Metoda obsługująca kliknięcia przycisków w menu"""
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.button == 1 and self.muted_icon_rect.collidepoint(event.pos):
                        self.game.muted = not self.game.muted
                        pygame.mixer.music.set_volume(0.0 if self.game.muted else 0.01)
                        return  # przerywamy, żeby nie kliknęło w przyciski

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
        """Rysuje wszystkie elementy interfejsu"""
        logo = Textures.LOGO
        logo_rect = logo.get_rect(center=(settings.WIDTH // 2, 100))
        screen.blit(logo, logo_rect)
        best_label_img = Textures.BEST
        best_label_rect = best_label_img.get_rect(center=(settings.WIDTH // 2, 505))
        screen.blit(best_label_img, best_label_rect)

        score_text = settings.font.render(str(self.game._high_score), True, settings.GOLD)
        score_rect = score_text.get_rect(center=(settings.WIDTH // 2, best_label_rect.bottom - 29))
        screen.blit(score_text, score_rect)
        icon = Textures.MUTED if self.game.muted else Textures.UNMUTED
        screen.blit(icon, self.muted_icon_rect)

        for button in self.buttons:
            screen.blit(button["image"], button["rect"])


class PlayingState(State):
    """Klasa reprezentująca aktywną rozrywkę"""
    def __init__(self, game, difficulty):
        super().__init__(game)
        self.difficulty = difficulty
        self.game._reset_game_logic(self.difficulty)

    def handle_events(self, events):
        """Obsługa sterowania ptakiem - mysz lub spcaja"""
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or \
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                command = JumpCommand(self.game.bird)
                command.execute()

    def update(self):
        """Aktualizuje wszystkie obiekty w grze i sprawdza kolizję"""
        self.game.bird.update()
        self.game.pipe.update()
        
        collision = self.game.pipe.check_collision(self.game.bird)
        if self.game.pipe.coin.check_collision(self.game.bird):
            self.game.score += 1
        
        if not self.game.pipe.scored and self.game.pipe.x + self.game.pipe.width < self.game.bird.x:
            self.game.pipe.scored = True
            self.game.pipes_passed = self.game.pipes_passed + 1

        bird_top = self.game.bird.y - self.game.bird.radius
        bird_bottom = self.game.bird.y + self.game.bird.radius

        if collision == "hit" or bird_bottom > settings.floor_y or bird_top < 0:
            self.game.pipe.crash_sound.play()
            last_frame = self.game.screen.copy()
            self.game.change_state(GameOverState(self.game, self.difficulty, last_frame))

    def draw(self, screen):
        """Rysuje wszystkie elementy rozgrywki - ptak, rura, monety i wyniki"""
        self.game.bird.draw(screen)
        self.game.pipe.draw(screen)
        self.game.pipe.coin.draw(screen)

        draw_text_with_shadow(screen, f"Coin: {self.game.score}", settings.font, (10, 10), settings.WHITE)

        pipes_surface = settings.font.render(f"Pipe: {self.game.pipes_passed}", True, settings.WHITE)
        pipes_pos_x = settings.WIDTH - pipes_surface.get_width() - 10
        draw_text_with_shadow(screen, f"Pipe: {self.game.pipes_passed}", settings.font, (pipes_pos_x, 10), settings.WHITE)


class GameOverState(State):
    """Klasa reprezentująca ekran końca gry"""
    def __init__(self, game, last_played_difficulty, last_frame_surface):
        super().__init__(game)
        self.last_played_difficulty = last_played_difficulty
        self.background_surface = last_frame_surface

        self.overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128)) 

        button_width, button_height = 220, 55
        center_x = settings.WIDTH / 2
        
        rect_restart = pygame.Rect(0, 0, button_width, button_height)
        rect_restart.center = (center_x, 300)

        rect_menu = pygame.Rect(0, 0, button_width, button_height)
        rect_menu.center = (center_x, 370)

        self.buttons = [
            {"image": Textures.BUTTON_RESTART, "rect": rect_restart, "action": "restart"},
            {"image": Textures.BUTTON_MENU, "rect": rect_menu, "action": "menu"}
        ]

    def handle_events(self, events):
        """Obsługa klinięć w menu końca gry - menu - reset"""
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        if button['rect'].collidepoint(event.pos):
                            if button['action'] == 'restart':
                                self.game.change_state(PlayingState(self.game, self.last_played_difficulty))
                            elif button['action'] == 'menu':
                                self.game.change_state(MenuState(self.game))

    def update(self):
        pass

    def draw(self, screen):
        """Rysuje ostatnią klatkę gry"""
        screen.blit(self.background_surface, (0,0))
        screen.blit(self.overlay, (0,0))

        game_over_text = settings.big_font.render("GAME OVER", True, settings.WHITE)
        game_over_rect = game_over_text.get_rect(center=(settings.WIDTH // 2, 150))
        screen.blit(game_over_text, game_over_rect)

        score_text = settings.font.render(f"COIN SCORE: {self.game.score}", True, settings.WHITE)
        score_rect = score_text.get_rect(center=(settings.WIDTH // 2, 220))
        screen.blit(score_text, score_rect)

        for button in self.buttons:
            screen.blit(button["image"], button["rect"])
