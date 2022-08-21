import pytest

from tic_tac_toe.cli import TIC_TAC_TOE_RULES
from tic_tac_toe.models import Board
from tic_tac_toe.find_winner import GameResult, Player, Square, find_winner, get_game_result, initialize_game

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

BOARD4 = """
   
 ox
  o
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
        (BOARD4, Square.CROSS, GameResult.CIRCLE_WINS),
    ],
)
def test_find_winner(board: str, player_to_move: Player, expected_result: GameResult) -> None:
    game = initialize_game(TIC_TAC_TOE_RULES)
    game.board = board_from_text(board)
    game.player_to_move = player_to_move

    winner = find_winner(game)

    assert winner == expected_result


def test_find_winner_must_be_same_for_symetrical_position() -> None:
    game1 = initialize_game(TIC_TAC_TOE_RULES)
    game1.board = board_from_text(BOARD31)
    game1.player_to_move = Square.CIRCLE

    game2 = initialize_game(TIC_TAC_TOE_RULES)
    game2.board = board_from_text(BOARD32)
    game2.player_to_move = Square.CIRCLE

    assert find_winner(game1) == find_winner(game2)


RESULT_BOARD1 = """
o  
 ox
 xo
"""

RESULT_BOARD2 = """
o  
oxx
o  
"""

RESULT_BOARD3 = """
ooo
 x 
 x 
"""

RESULT_BOARD4 = """
  o
 xo
 xo
"""

RESULT_BOARD5 = """
 x 
 x 
ooo
"""

RESULT_BOARD6 = """
  o
 ox
ox 
"""

@pytest.mark.parametrize("board, expected_result", [
    (RESULT_BOARD1, GameResult.CIRCLE_WINS),
    (RESULT_BOARD2, GameResult.CIRCLE_WINS),
    (RESULT_BOARD3, GameResult.CIRCLE_WINS),
    (RESULT_BOARD4, GameResult.CIRCLE_WINS),
    (RESULT_BOARD5, GameResult.CIRCLE_WINS),
    (RESULT_BOARD6, GameResult.CIRCLE_WINS),
])
def test_get_game_result(board: str, expected_result: GameResult) -> None:
    game = initialize_game(TIC_TAC_TOE_RULES)
    game.board = board_from_text(board)

    assert get_game_result(game) == expected_result
