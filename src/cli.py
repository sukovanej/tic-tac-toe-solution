from .models import GameRules
from .print import print_game
from .tic import find_winner, initialize_game, play_move

TIC_TAC_TOE_RULES = GameRules(rows=3, columns=3, connected_to_win=3)


if __name__ == "__main__":
    game = initialize_game(TIC_TAC_TOE_RULES)

    game = play_move((0, 1), game)
    game = play_move((2, 2), game)
    print_game(game)

    result = find_winner(game)
    print(result)