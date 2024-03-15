from game_time import GameTime
from cash import Cash

from collections import namedtuple


class UnitResources(namedtuple):
    time: GameTime
    cash: Cash

    def __str__(self) -> str:
        return " | ".join(map(str, (self.time, self.cash)))
