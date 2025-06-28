from abc import ABC, abstractmethod
from typing import TYPE_CHECKING # Specjalny import b
if TYPE_CHECKING:
    from game_objects import Bird


class Command(ABC):
    """Abstrakcyjny interfejs dla wszystkich poleceń."""
    @abstractmethod
    def execute(self):
        pass


class JumpCommand(Command):
    """Konkretne polecenie, które wie, jak wykonać akcję skoku."""
    def __init__(self, bird: 'Bird'):
        self.bird = bird

    def execute(self):
        self.bird.jump()
