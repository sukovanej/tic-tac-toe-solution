from .models import GameRules
from .find_winner import find_winner, initialize_game

TIC_TAC_TOE_RULES = GameRules(rows=3, columns=3, connected_to_win=3)


def run():
    game = initialize_game(TIC_TAC_TOE_RULES)
    result = find_winner(game)
    print(result)
