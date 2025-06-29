from abc import ABC, abstractmethod
from typing import TYPE_CHECKING # Specjalny import
if TYPE_CHECKING:
    from game_objects import Bird

""" Implementacja wzorca Command
    Hermetyzuje akcje skoku jako obiekt"""


class Command(ABC):
    """Abstrakcujna klasa bazowa dla wszystkich poleceń"""
    @abstractmethod
    def execute(self):
        pass


class JumpCommand(Command):
    """Konkretne polecenie, które wie jak wykonać skok na danym obiekcie ptaka """
    def __init__(self, bird: 'Bird'):
        self.bird = bird

    def execute(self):
        self.bird.jump()
