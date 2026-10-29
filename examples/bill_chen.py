from poker.action import Action
from poker.card import Rank
from poker.game_state import GameState


# Bill Chen's formula, which scores two cards, as Wikipedia's "Texas hold 'em starting hands" gives it. A pair of aces scores
# 20, the most, and seven and two of different suits scores -1.5, the least.
POINTS = {Rank.ACE: 10, Rank.KING: 8, Rank.QUEEN: 7, Rank.JACK: 6}  # Every other card is worth half of its number
GAP_PENALTIES = {0: 0, 1: 1, 2: 2, 3: 4}  # Points taken off for the ranks between the two cards, and 5 for any more


def chen_score(state: GameState) -> float:
    high, low = sorted(state.my_player.hole_cards, key=lambda card: list(Rank).index(card.rank), reverse=True)
    points = lambda card: POINTS.get(card.rank, (list(Rank).index(card.rank) + 2) / 2)

    if high.rank is low.rank:
        return 6 if high.rank is Rank.FIVE else max(points(high) * 2, 5)  # A pair is worth double, and at least 5

    gap = list(Rank).index(high.rank) - list(Rank).index(low.rank) - 1
    score = points(high) - GAP_PENALTIES.get(gap, 5)

    if high.suit is low.suit:
        score += 2

    if gap <= 1 and list(Rank).index(high.rank) < list(Rank).index(Rank.QUEEN):
        score += 1  # Close together, below a queen, so it can make the higher straights

    return score


def myAI(state: GameState) -> Action:
    # Goes all in with a Chen score of at least 9, or any hand with fewer than 10 big blinds, and otherwise checks or folds
    # With fewer than 10 big blinds, waiting lets the blinds eat our chips, so any two cards are worth going all in with
    big_blinds = (state.my_player.chips_in_stack + state.my_player.chips_bet) / state.big_blind

    if big_blinds < 10 or chen_score(state) >= 9:
        return Action.raise_by(10 ** 9)  # More than anyone has, which puts us all in

    to_call = max(player.chips_bet for player in state.players) - state.my_player.chips_bet
    return Action.check() if to_call == 0 else Action.fold()
