from abc import ABC, abstractmethod

""" Plik zarządzający strategiami ruchu rur i monet
    Implementacja wzorca Strategy """

# --- Strategie dla Rury ---
class PipeMovementStrategy(ABC):
    """Abstrakcyjna klasa bazowa dla strategii ruchu rur"""
    @abstractmethod
    def update(self, pipe):
        pass

class StaticPipeStrategy(PipeMovementStrategy):
    """Rura statyczna - przesuwa się tylko w poziome"""
    def update(self, pipe):
        pipe.x -= pipe.speed

class VerticalPipeStrategy(PipeMovementStrategy):
    """Ruchoma rura - przesuwa się w pionie i poziomie"""
    def __init__(self, vertical_speed=1, move_range=40):
        self.vertical_speed = vertical_speed
        self.move_range = move_range
        self.direction = 1

    def update(self, pipe):
        pipe.x -= pipe.speed
        pipe.gap_y += self.vertical_speed * self.direction
        if pipe.gap_y > pipe.initial_gap_y + self.move_range or pipe.gap_y < pipe.initial_gap_y - self.move_range:
            self.direction *= -1

# --- Strategie dla Monety ---
class CoinMovementStrategy(ABC):
    """Abstrakcyjna klasa bazowa dla strategii ruchu monet"""
    @abstractmethod
    def update(self, coin, pipe):
        pass

class StaticCoinStrategy(CoinMovementStrategy):
    """Moneta statyczna - przesuwa się tylko w poziomie"""
    def update(self, coin, pipe):
        pass

class VerticalCoinStrategy(CoinMovementStrategy):
    """Ruchoma moneta - przesuwa się w pionie i poziomie"""
    def __init__(self, vertical_speed=2, move_range=30):
        self.vertical_speed = vertical_speed
        self.move_range = move_range
        self.direction = 1

    def update(self, coin, pipe):
        coin.y += self.vertical_speed * self.direction

        upper_boundary = pipe.gap_y + 20
        lower_boundary = pipe.gap_y + pipe.gap_height - 20

        if coin.y > lower_boundary or coin.y < upper_boundary:
            self.direction *= -1


        if coin.y > lower_boundary:
            coin.y = lower_boundary
        elif coin.y < upper_boundary:
            coin.y = upper_boundary
