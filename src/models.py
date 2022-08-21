from dataclasses import dataclass
from enum import Enum
from typing import Literal


class Square(str, Enum):
    CROSS = "cross"
    CIRCLE = "circle"
    EMPTY = "empty"


class GameResult(str, Enum):
    CROSS_WINS = "cross_wins"
    CIRCLE_WINS = "circe_wins"
    DRAW = "draw"
    IN_PROGRESS = "in_progress"


Player = Literal[Square.CROSS, Square.CIRCLE]


Board = list[list[Square]]


@dataclass
class GameRules:
    rows: int
    columns: int
    connected_to_win: int


@dataclass
class Game:
    player_to_move: Player
    board: Board
    rules: GameRules


# (row, column)
Position = tuple[int, int]
