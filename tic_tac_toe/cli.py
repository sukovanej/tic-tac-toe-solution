from .models import GameRules
from .print import print_game
from .find_winner import find_winner, initialize_game, play_move

TIC_TAC_TOE_RULES = GameRules(rows=3, columns=3, connected_to_win=3)


def run():
    game = initialize_game(TIC_TAC_TOE_RULES)

    game = play_move((1, 1), game)
    game = play_move((0, 0), game)
    print_game(game)
    print(game.player_to_move)

    result = find_winner(game)
    print(result)
