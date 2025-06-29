import pygame
import settings
import random
import os
from game_objects import Bird, Heavy_bird, Light_Bird, Random_Bird, Pipe, Background, Floor
from strategies import StaticCoinStrategy, VerticalCoinStrategy, StaticPipeStrategy, VerticalPipeStrategy
from exceptions import InvalidPipeConfigError
from game_states import State, MenuState, PlayingState
from textures import Textures

""" Klasa Game - główna klasa
    Klasa Game jest centrum dowodzenia grą. Zarządza główną pęltlą
    stanem gry, ogólną logiką - punktacja
    Użycie klas """

class Game:
    def __init__(self):
        """Główne ustawienia gry i inicjalizacja zasobów"""

        # Inicjalizacja pygame, okna i dźwięków
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(settings.ASSETS_DIR, "music.wav"))
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()

        # Jednorazowe wczytanie wszystkich tekstur przy starcie gry
        Textures.load()

        self.background = Background(Textures.BACKGROUND)
        pygame.display.set_caption("Flappy Janusz")

        # Inicjalizacja atrybutów i stanu gry
        self.running = True
        self.state: State = None
        self.muted = False
        self._high_score = 0
        self._score = 0
        self._pipes_passed = 0
        self.bird = None
        self.pipe = None
        self.title = settings.big_font.render("FLAPPY JANUSZ", True, settings.BLACK)

        # Ustawienie początkowego stanu gry na Menu główne
        self.change_state(MenuState(self))


    # Użycie enkapsulacji - gettery i settery
    # Oddzielamy dostęp do atrybutów, pozwalacją na dodanie
    # dodatkowej logiki podczas ich odczytu lub zapisu
    @property
    def score(self):
        """Getter dla wyniku monet"""
        return self._score
    
    @score.setter
    def score(self, value):
        """Setter dla wyniku monet. Pilnuje by wynik nie był ujemny""" # Na wszelki wypadek, błąd programisty itp
        if value > 0:
            self._score = value
        else:
            self._score = 0

        if self._score > self._high_score:
            self._high_score = self._score

    
    @property
    def pipes_passed(self):
        """Getter dla wyniku ominiętych rur"""
        return self._pipes_passed
    
    @pipes_passed.setter
    def pipes_passed(self, value):
        """Setter dla wyniku ominiętych rur. Aktualizuje wynik jeśli został pobity"""
        self._pipes_passed = value

        if self._pipes_passed > self._high_score:
            self._high_score = self._pipes_passed

    def change_state(self, new_state: State):
        """Metoda do przechodzenia między stanami gry"""
        self.state = new_state

    def _reset_game_logic(self, difficulty):
        """Resetuje i konfiguruje logikę gry na podstawie wybranego poziomu gry"""
        self.score = 0
        self.pipes_passed = 0

        #Wybór tła zależnie od poziomu trudności
        if difficulty == 'medium':
            self.background = Background(Textures.BACKGROUND2)
        elif difficulty == 'hard':
            self.background = Background(Textures.BACKGROUND3)
        elif difficulty == 'random':
            self.background = Background(Textures.BACKGROUND4)

        else:
            self.background = Background(Textures.BACKGROUND)

        # Konfiguracja ptaka, rur i monet dla każdego poziomu
        # Użycie własnego wyjątku InvalidPipeConfigError
        try:
            if difficulty == 'easy':
                self.bird = Light_Bird(50, settings.HEIGHT // 2, 15)
                pipe_movement_strategy = StaticPipeStrategy()
                coin_movement_strategy = StaticCoinStrategy()
                self.pipe = Pipe(settings.WIDTH, width=80, gap_height=200, speed=2, movement_strategy=pipe_movement_strategy, coin_strategy=coin_movement_strategy)
                self.floor = Floor(speed=2)
            elif difficulty == 'medium':
                self.bird = Bird(50, settings.HEIGHT // 2, 15)
                pipe_movement_strategy = StaticPipeStrategy()
                coin_movement_strategy = VerticalCoinStrategy(vertical_speed=1, move_range=25)
                self.pipe = Pipe(
                    settings.WIDTH,
                    width=70,
                    gap_height=170,
                    speed=3,
                    movement_strategy=pipe_movement_strategy,
                    coin_strategy=coin_movement_strategy,
                    pipe_img=Textures.PIPE_BODY2,
                    pipe_end_img=Textures.PIPE_END2,
                    pipe_end_flipped_img=Textures.PIPE_END2_FLIPPED
                )
                self.floor = Floor(speed=3)
                self.floor.image = Textures.FLOOR2
            elif difficulty == 'hard':
                self.bird = Heavy_bird(50, settings.HEIGHT // 2, 15)
                pipe_movement_strategy = VerticalPipeStrategy(vertical_speed=2, move_range=50)
                coin_movement_strategy = VerticalCoinStrategy(vertical_speed=3, move_range=35)
                self.pipe = Pipe(
                    settings.WIDTH,
                    width=70,
                    gap_height=170,
                    speed=3,
                    movement_strategy=pipe_movement_strategy,
                    coin_strategy=coin_movement_strategy,
                    pipe_img=Textures.PIPE_BODY3,
                    pipe_end_img=Textures.PIPE_END3,
                    pipe_end_flipped_img=Textures.PIPE_END3_FLIPPED
                )
                self.floor = Floor(speed=4)
                self.floor.image = Textures.FLOOR3

            elif difficulty == 'random':
                self.bird = Random_Bird(50, settings.HEIGHT // 2, 15)
                
                if random.choice([True, False]):
                    pipe_movement_strategy = StaticPipeStrategy()
                else:
                    pipe_movement_strategy = VerticalPipeStrategy(vertical_speed=random.randint(1, 3), move_range=random.randint(30, 60))

                if random.choice([True, False]):
                    coin_movement_strategy = StaticCoinStrategy()
                else:
                    coin_movement_strategy = VerticalCoinStrategy(vertical_speed=random.randint(2, 4), move_range=random.randint(25, 40))

                rand_speed = random.randint(2, 5)

                self.pipe = Pipe(
                    settings.WIDTH,
                    width=70,
                    gap_height=170,
                    speed=3,
                    movement_strategy=pipe_movement_strategy,
                    coin_strategy=coin_movement_strategy,
                    pipe_img=Textures.PIPE_BODY4,
                    pipe_end_img=Textures.PIPE_END4,
                    pipe_end_flipped_img=Textures.PIPE_END4_FLIPPED
                )
                self.floor = Floor(speed=rand_speed)
                self.floor.image = Textures.FLOOR4

        # Własny wyjątek rzucany w momencie próby utworzenia rury
        # z nielogicznymi (np. ujemnymi) wartościami
        except InvalidPipeConfigError as e:
            print(f"Błąd konfiguracji rur! {e}")
            print("Gra nie może zostać poprawnie uruchomiona.")
            self.running = False
    
    def run(self):
        """Główna pętla gry"""
        while self.running:
            events = pygame.event.get() # Pobranie zdarzeń o kliknięciu myszki lub klawisza

            # Przekazanie kontroli do aktualnego stanu gry
            self.state.handle_events(events) 
            self.state.update()
        
            self.background.update()
            self.background.draw(self.screen)
            self.state.draw(self.screen)

            # Rysowanie podłogi tylko w stanie gry
            if isinstance(self.state, PlayingState): 
                self.floor.update()
                self.floor.draw(self.screen)

            # Aktualizacja ekranu
            pygame.display.update()
            self.clock.tick(settings.FPS)
        
"""Uruchomienie gry"""
if __name__ == "__main__":
    game = Game()
    game.run()
