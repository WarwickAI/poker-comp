from poker.action import Action
from poker.game_state import GameState


def myAI(state: GameState) -> Action:
    # Raises by the size of the pot every time
    to_call = max(player.chips_bet for player in state.players) - state.my_player.chips_bet
    pot_after_calling = state.chips_in_pot + to_call
    return Action.raise_by(max(pot_after_calling, state.minimum_raise))  # More than we have puts us all in
