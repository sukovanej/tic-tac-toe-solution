from __future__ import annotations

from collections.abc import Iterable
from itertools import product

from .models import Game, GameResult, GameRules, Player, Position, Square


def get_next_player(player: Player) -> Player:
    if player == Square.CIRCLE:
        return Square.CROSS

    return Square.CIRCLE


def play_move(position: Position, game: Game) -> Game:
    row, column = position

    new_board = [row.copy() for row in game.board]

    if new_board[row][column] != Square.EMPTY:
        raise Exception(f"Tried to write on non-empty ({row}, {column}) square.")

    new_board[row][column] = game.player_to_move

    return Game(
        player_to_move=get_next_player(game.player_to_move),
        board=new_board,
        rules=game.rules,
    )


def get_possible_moves(game: Game) -> list[Position]:
    return [(row, column) for row, column in get_all_positions(game.rules) if game.board[row][column] == Square.EMPTY]


def get_all_positions(game_rules: GameRules) -> Iterable[tuple[int, int]]:
    return product(range(game_rules.rows), range(game_rules.columns))


def square_on_position(position: Position, game: Game) -> Square:
    row, column = position
    return game.board[row][column]


def get_game_result(game: Game) -> GameResult:
    has_empty_squares = False

    for position in get_all_positions(game.rules):
        square = square_on_position(position, game)
        if square == Square.EMPTY:
            has_empty_squares = True
            continue

        if has_connected_on_position(position, game):
            if square == Square.CIRCLE:
                return GameResult.CIRCLE_WINS
            else:
                return GameResult.CROSS_WINS

    if has_empty_squares:
        return GameResult.IN_PROGRESS
    return GameResult.DRAW


def has_connected_on_position(position: Position, game: Game) -> bool:
    connected_to_win = game.rules.connected_to_win
    rows, columns = game.rules.rows, game.rules.columns

    current_row, current_column = position
    square = square_on_position(position, game)

    column_range = range(current_column, min(current_column + connected_to_win, rows))
    row_range = range(current_row, min(current_row + connected_to_win, columns))

    has_enough_in_column = rows - current_row >= connected_to_win
    has_enough_in_row = columns - current_column >= connected_to_win

    connected_in_row = has_enough_in_row and all(
        square_on_position((current_row, column), game) == square for column in column_range
    )
    connected_in_column = has_enough_in_column and all(
        square_on_position((row, current_column), game) == square for row in row_range
    )
    connected_in_diagonal = (
        has_enough_in_column
        and has_enough_in_row
        and all(square_on_position(position, game) == square for position in zip(row_range, column_range))
    )

    row_range_opposite = range(current_row, max(current_row - connected_to_win, -1), -1)
    has_enough_in_column_opposite = current_row + 1 >= connected_to_win

    connected_in_diagonal_2 = (
        has_enough_in_column_opposite
        and has_enough_in_row
        and all(square_on_position(position, game) == square for position in zip(row_range_opposite, column_range))
    )

    return connected_in_row or connected_in_column or connected_in_diagonal or connected_in_diagonal_2


def initialize_game(rules: GameRules) -> Game:
    board = [[Square.EMPTY] * rules.columns for _ in range(rules.rows)]
    return Game(board=board, rules=rules, player_to_move=Square.CIRCLE)


def find_winner(game: Game, depth: int = 0) -> GameResult:
    possible_moves = get_possible_moves(game)
    is_last_move = len(possible_moves) == 1
    results = []

    for move in possible_moves:
        new_game = play_move(move, game)
        result = get_game_result(new_game)

        if player_wins(game.player_to_move, result):
            return result

        if not is_last_move:
            result = find_winner(new_game, depth + 1)

        if player_wins(game.player_to_move, result):
            return result

        results.append(result)

    if any(result == GameResult.DRAW for result in results):
        return GameResult.DRAW

    if not results:
        raise Exception("Should never happen")

    return results[0]


def player_wins(player: Player, result: GameResult) -> bool:
    cross_wins = result == GameResult.CROSS_WINS and player == Square.CROSS
    circle_wins = result == GameResult.CIRCLE_WINS and player == Square.CIRCLE
    return cross_wins or circle_wins
