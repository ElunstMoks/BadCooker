from dataclasses import dataclass
from typing import Dict, Any

from game import Game

@dataclass
class BadCookerData:
    games: [Game]

    @staticmethod
    def from_dict(dict: Dict[str, Any]) -> "BadCookerData":
        return BadCookerData(
            games=Game.from_dict(dict_game) for dict_game in dict["games"]
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "games": [game.to_dict() for game in self.games]
        }
