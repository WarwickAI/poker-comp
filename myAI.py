from poker.action import Action
from poker.game_state import GameState


def myAI(state: GameState) -> Action:
    for player in state.players:
        if isinstance(player, MyPlayer):
            return Action.check() if player.chips_bet == max(player.chips_bet for player in state.players) else Action.fold()
