from poker.action import Action
from poker.game_state import GameState


def myAI(state: GameState) -> Action:
    # Raises by the big blind whenever nobody has bet more than the big blind, and folds to anything bigger
    biggest_bet = max(player.chips_bet for player in state.players)
    to_call = biggest_bet - state.my_player.chips_bet

    if biggest_bet > state.big_blind:
        return Action.check() if to_call == 0 else Action.fold()

    return Action.raise_by(state.big_blind)  # Never less than the smallest raise here, as nobody has bet more than the big blind
