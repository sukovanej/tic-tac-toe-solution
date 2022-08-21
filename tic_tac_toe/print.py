from .models import Game, Square


def print_game(game: Game) -> None:
    starting_row_str = "━━━┳" * (game.rules.columns - 1) + "━━━"
    print("┏", starting_row_str, "┓", sep="")

    row_middle_str = "━━━╋" * (game.rules.columns - 1) + "━━━"
    for row_num, row in enumerate(game.board):
        for square in row:
            print("┃ ", print_square(square), " ", sep="", end="")

        print("┃")

        if row_num < game.rules.rows - 1:
            print("┣", row_middle_str, "┫", sep="")

    ending_row_str = "━━━┻" * (game.rules.columns - 1) + "━━━"
    print("┗", ending_row_str, "┛", sep="")


def print_square(square: Square):
    match square:
        case Square.CROSS:
            return "x"
        case Square.CIRCLE:
            return "o"
        case Square.EMPTY:
            return " "
