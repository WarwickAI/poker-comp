from poker.action import Action
from poker.game_state import GameState


def myAI(state: GameState) -> Action:
    # Goes all in every time
    return Action.raise_by(state.my_player.chips_in_stack)  # More than we have left after calling, which puts us all in
