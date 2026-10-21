from poker.action import Action
from poker.game_state import GameState


def myAI(state: GameState) -> Action:
    # Goes all in when its two cards are a pair, and otherwise checks or folds
    card, other_card = state.my_player.hole_cards
    to_call = max(player.chips_bet for player in state.players) - state.my_player.chips_bet

    if card.rank == other_card.rank:
        return Action.raise_by(state.my_player.chips_in_stack)  # More than we have left after calling, which puts us all in

    if to_call == 0:
        return Action.check()

    return Action.fold()
