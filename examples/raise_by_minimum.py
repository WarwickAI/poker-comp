from poker.action import Action
from poker.game_state import GameState


def myAI(state: GameState) -> Action:
    # Raises by the smallest amount allowed every time
    return Action.raise_by(state.minimum_raise)  # With fewer chips than that, this puts us all in
