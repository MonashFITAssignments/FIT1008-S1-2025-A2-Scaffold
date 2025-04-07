
from enum import Enum, IntEnum


class TeamGameResult(IntEnum):
    """
    Enum class to represent the possible game results for a team
    Valid results are: Win, Draw, Loss
    """
    WIN = 3
    DRAW = 1
    LOSS = 0


class PlayerPosition(Enum):
    """
    Enum class to represent the soccer positions
    Valid positions are: Striker, Midfielder, Defender, Goalkeeper
    """
    GOALKEEPER = "Goalkeeper"
    DEFENDER = "Defender"
    MIDFIELDER = "Midfielder"
    STRIKER = "Striker"
