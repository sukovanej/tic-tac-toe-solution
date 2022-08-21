import pytest

from src.cli import TIC_TAC_TOE_RULES
from src.models import Board
from src.tic import GameResult, Player, Square, find_winner, initialize_game

BOARD1 = """
xox
xoo
   
"""

BOARD2 = """
   
 ox
   
"""

BOARD31 = """
 o 
   
  x
"""

BOARD32 = """
 o 
   
x  
"""


def char_to_square(ch: str) -> Square:
    match ch:
        case "x":
            return Square.CROSS
        case "o":
            return Square.CIRCLE
        case " ":
            return Square.EMPTY
        case _:
            raise ValueError


def board_from_text(text: str) -> Board:
    if text[0] == "\n":
        text = text[1:]

    return [[char_to_square(ch) for ch in line] for line in text.splitlines()]


@pytest.mark.parametrize(
    "board, player_to_move, expected_result",
    [
        (BOARD1, Square.CIRCLE, GameResult.CIRCLE_WINS),
        (BOARD1, Square.CROSS, GameResult.CROSS_WINS),
        (BOARD2, Square.CIRCLE, GameResult.CIRCLE_WINS),
    ],
)
def test_find_winner(board: str, player_to_move: Player, expected_result: GameResult) -> None:
    game = initialize_game(TIC_TAC_TOE_RULES)
    game.board = board_from_text(board)
    game.player_to_move = player_to_move

    winner = find_winner(game)

    assert winner == expected_result


def test_find_winner_must_be_same_for_symetrical_response() -> None:
    game1 = initialize_game(TIC_TAC_TOE_RULES)
    game1.board = board_from_text(BOARD31)
    game1.player_to_move = Square.CIRCLE

    game2 = initialize_game(TIC_TAC_TOE_RULES)
    game2.board = board_from_text(BOARD32)
    game2.player_to_move = Square.CIRCLE

    assert find_winner(game1) == find_winner(game2)
