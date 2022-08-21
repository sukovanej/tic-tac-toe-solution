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

    max_column = min(current_column + connected_to_win, rows)
    column_range = range(current_column, max_column)

    max_row = min(current_row + connected_to_win, columns)
    row_range = range(current_row, max_row)

    in_row = [square_on_position((current_row, column), game) for column in column_range]
    connected_in_row = len(in_row) >= connected_to_win and all(c == square for c in in_row)

    in_column = [square_on_position((row, current_column), game) for row in row_range]
    connected_in_column = len(in_column) >= connected_to_win and all(c == square for c in in_column)

    in_diagonal = [square_on_position(position, game) for position in zip(row_range, column_range)]
    connected_in_diagonal = len(in_diagonal) >= connected_to_win and all(c == square for c in in_diagonal)

    result = connected_in_row or connected_in_column or connected_in_diagonal

    return result


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

        if player_wins(get_next_player(game.player_to_move), result):
            continue

        if not is_last_move:
            result = find_winner(new_game, depth + 1)

        results.append(result)

    if all(player_wins(game.player_to_move, r) for r in results if r != GameResult.DRAW):
        return GameResult.CIRCLE_WINS if game.player_to_move == Square.CIRCLE else GameResult.CROSS_WINS

    if any(result == GameResult.DRAW for result in results):
        return GameResult.DRAW

    if not results:
        raise Exception("Should never happen")

    return results[0]


def player_wins(player: Player, result: GameResult) -> bool:
    cross_wins = result == GameResult.CROSS_WINS and player == Square.CROSS
    circle_wins = result == GameResult.CIRCLE_WINS and player == Square.CIRCLE
    return cross_wins or circle_wins
