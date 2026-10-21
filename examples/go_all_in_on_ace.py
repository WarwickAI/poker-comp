from poker.action import Action
from poker.card import Rank
from poker.game_state import GameState


def myAI(state: GameState) -> Action:
    # Goes all in when it holds an ace, and otherwise checks or folds
    to_call = max(player.chips_bet for player in state.players) - state.my_player.chips_bet

    if any(card.rank is Rank.ACE for card in state.my_player.hole_cards):
        return Action.raise_by(state.my_player.chips_in_stack)  # More than we have left after calling, which puts us all in

    if to_call == 0:
        return Action.check()

    return Action.fold()
