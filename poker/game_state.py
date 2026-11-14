from __future__ import annotations
from .action import Action
from .player import Player, MyPlayer
from .card import Card


class HandAction:
    # Something a player chose to do in a hand: on which street (0 preflop, 1 the flop, 2 the turn, 3 the river), what they did,
    # the chips they had bet on that street after it, and whether it put them all in. Blinds and antes aren't actions, and a
    # mistake, or a raise nobody could call, is the check, fold or call it was played as.
    def __init__(self, *, id: int | None, street: int, kind: Action.Kind, chips_bet: int, all_in: bool = False):
        self.id = id
        self.street = street
        self.kind = kind
        self.chips_bet = chips_bet
        self.all_in = all_in

    def __repr__(self):
        return f"HandAction(id={self.id}, street={self.street}, kind={self.kind}, chips_bet={self.chips_bet}, all_in={self.all_in})"

    def __eq__(self, other):
        return (self.id, self.street, self.kind, self.chips_bet, self.all_in) == (other.id, other.street, other.kind, other.chips_bet, other.all_in) if isinstance(other, HandAction) else NotImplemented

    def __hash__(self):
        return hash((self.id, self.street, self.kind, self.chips_bet, self.all_in))


class HandRecord:
    # A finished hand, as everyone at the table saw it. `players` are those dealt in, in seat order, as they ended the hand:
    # `chips_in_stack` after it and `chips_bet` all they put in during it, ante included. `board` is in the order it was dealt.
    # `shown` has the hole cards of everyone who showed at the showdown, by id: as in a casino, once someone is all in every
    # hand is shown, and otherwise the last to bet or raise on the river shows first (the first player after the button if
    # nobody did), then each player round the table shows only if they can beat or tie the best hand shown so far, and the
    # rest muck. Nobody shows when everyone else folded. `won` is what each player won from the pot, by id.
    def __init__(self, *, number: int, small_blind: int, big_blind: int, ante: int, players: list[Player], board: list[Card], actions: list[HandAction], shown: dict[int | None, set[Card]], won: dict[int | None, int]):
        self.number = number
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.ante = ante
        self.players = players
        self.board = board
        self.actions = actions
        self.shown = shown
        self.won = won

    def __repr__(self):
        return f"HandRecord(number={self.number}, players={self.players}, board={self.board}, actions={self.actions}, shown={self.shown}, won={self.won})"

    def __eq__(self, other):
        if not isinstance(other, HandRecord):
            return NotImplemented

        return vars(self) == vars(other)


class GameState:
    # Besides the table as it is now: `history` is this hand's actions so far, in order, and `previous_hands` the hands at
    # your table which have finished since your last turn (usually just the last one, but more if you had no turn in some,
    # and from your old table if you were moved). Anything a bot can work out from the rest is left out: the button is the
    # player before the small blind (or the small blind, heads-up), and this hand's number is one more than the last record's.
    # As at a real table, nothing is given about the rest of the tournament.
    def __init__(self, *, my_player: MyPlayer, players: list[Player], chips_in_pot: int = 0, community_cards: set[Card] | None = None, small_blind: int = 0, big_blind: int = 0, min_raise: int | None = None, ante: int = 0,
                 history: list[HandAction] | None = None, previous_hands: list[HandRecord] | None = None):
        self.my_player = my_player
        self.players = players
        self.chips_in_pot = chips_in_pot
        self.community_cards = community_cards if community_cards is not None else set()  # A new set each time, so states never share one
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.min_raise = big_blind if min_raise is None else min_raise
        self.ante = ante
        self.history = history if history is not None else []
        self.previous_hands = previous_hands if previous_hands is not None else []


    def __repr__(self):
        return f"GameState(my_player={self.my_player}, players={self.players}, chips_in_pot={self.chips_in_pot}, community_cards={self.community_cards}, min_raise={self.min_raise}, history={self.history})"


    def __eq__(self, other):
        if not isinstance(other, GameState):
            return NotImplemented

        if self.my_player != other.my_player:
            return False

        if self.players != other.players:
            return False

        if self.chips_in_pot != other.chips_in_pot:
            return False

        if self.community_cards != other.community_cards:
            return False

        if self.small_blind != other.small_blind:
            return False

        if self.big_blind != other.big_blind:
            return False

        if self.min_raise != other.min_raise:
            return False

        if self.ante != other.ante:
            return False

        if self.history != other.history or self.previous_hands != other.previous_hands:
            return False

        return True


    def __hash__(self):
        # previous_hands is left out, which is allowed: equal states still hash the same
        return hash((self.my_player, tuple(self.players), self.chips_in_pot, frozenset(self.community_cards), self.small_blind, self.big_blind, self.min_raise, self.ante,
                     tuple(self.history)))
