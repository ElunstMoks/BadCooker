from dataclasses import dataclass
from typing import Dict, Any

from unit_resources.unit_resources import UnitResources, GameTime, Cash

@dataclass
class Game:
    unit_resources: UnitResources

    @staticmethod
    def from_dict(dict: Dict[str, Any]) -> "Game":
        return Game(
            unit_resources=UnitResources(
                time=GameTime(dict["unit_resources"]["time"]),
                cash=Cash(dict["unit_resources"]["cash"])
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
                "unit_resources":
                    {"time": int(self.unit_resources.time),
                     "cash": int(self.unit_resources.cash)
                     }
                }
