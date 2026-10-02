from poker.action import Action
from poker.game_state import GameState


def myAI(state: GameState) -> Action:
    return Action.fold()
