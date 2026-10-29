from poker.action import Action
from poker.card import Rank
from poker.game_state import GameState


# Phil Hellmuth's six tiers of starting hands, from his book Play Poker Like the Pros, as Wikipedia's "Texas hold 'em starting
# hands" lists them, strongest first. A hand ending in "s" has both cards of the same suit, and one without it has two different suits.
TIERS = [
    {"AA", "KK", "AKs", "QQ", "AK"},
    {"JJ", "TT", "99"},
    {"88", "77", "AQs", "AQ"},
    {"66", "55", "44", "33", "22", "AJs", "ATs", "A9s", "A8s"},
    {"A7s", "A6s", "A5s", "A4s", "A3s", "A2s", "KQs", "KQ"},
    {"QJs", "JTs", "T9s", "98s", "87s", "76s", "65s"},
]

LETTERS = dict(zip(Rank, "23456789TJQKA"))  # Rank lists the ranks from lowest to highest


def hand(state: GameState) -> str:
    # Our two cards written like the tiers, such as "AKs", "AK" or "QQ"
    high, low = sorted(state.my_player.hole_cards, key=lambda card: list(Rank).index(card.rank), reverse=True)
    suited = high.suit is low.suit and high.rank is not low.rank
    return LETTERS[high.rank] + LETTERS[low.rank] + ("s" if suited else "")


def myAI(state: GameState) -> Action:
    # Goes all in with a hand in the top three of Phil Hellmuth's six tiers, or any hand with fewer than 10 big blinds, and otherwise checks or folds
    # With fewer than 10 big blinds, waiting lets the blinds eat our chips, so any two cards are worth going all in with
    big_blinds = (state.my_player.chips_in_stack + state.my_player.chips_bet) / state.big_blind

    if big_blinds < 10 or any(hand(state) in tier for tier in TIERS[:3]):
        return Action.raise_by(10 ** 9)  # More than anyone has, which puts us all in

    to_call = max(player.chips_bet for player in state.players) - state.my_player.chips_bet
    return Action.check() if to_call == 0 else Action.fold()
