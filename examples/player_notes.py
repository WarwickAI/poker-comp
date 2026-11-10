from collections import Counter, defaultdict

from poker.action import Action
from poker.card import Card, Rank
from poker.game_state import GameState, HandRecord
from poker.player import Blind


# Shows what an AI can learn about the other players from the hand history. The bot's process lives for the whole
# tournament, so these notes, kept by each player's id (the same all tournament, even at another table), last between hands.
notes: defaultdict[int | None, Counter] = defaultdict(Counter)
shown: defaultdict[int | None, list[tuple[bool, set[Card]]]] = defaultdict(list)  # Hands shown down, and whether they raised preflop
last_hand = 0  # The number of the last hand we were told about, so this one is last_hand + 1


def learn(record: HandRecord):
    # previous_hands has every hand at our table since our last turn, so each hand is learned from exactly once
    global last_hand
    last_hand = record.number

    for player in record.players:
        mine = [action for action in record.actions if action.id == player.id]
        preflop = [action.kind for action in mine if action.street == 0]
        note = notes[player.id]
        note["hands"] += 1
        note["vpip"] += Action.Kind.CALL in preflop or Action.Kind.RAISE in preflop  # Put chips in by choice
        note["pfr"] += Action.Kind.RAISE in preflop
        note["raises"] += sum(action.kind is Action.Kind.RAISE for action in mine if action.street > 0)
        note["calls"] += sum(action.kind is Action.Kind.CALL for action in mine if action.street > 0)
        note["won"] += player.id in record.won  # Hands they won chips in, whether at a showdown or not

        if player.id in record.shown:  # Hands which lost can be mucked, so this is never every hand they played
            shown[player.id].append((Action.Kind.RAISE in preflop, record.shown[player.id]))


def rate(id: int | None, stat: str, prior: float) -> float:
    # The share of hands with this stat, starting from a guess, so that a few hands don't decide it
    return (notes[id][stat] + prior * 5) / (notes[id]["hands"] + 5)


def good(cards: set[Card]) -> bool:
    high, low = sorted((list(Rank).index(card.rank) for card in cards), reverse=True)
    return high == low or low >= list(Rank).index(Rank.TEN)  # A pair, or two cards ten or higher


def bluffs(id: int | None) -> int:
    # The hands they showed down after raising preflop which weren't good: a player who does this raises with anything
    return sum(raised and not good(cards) for raised, cards in shown[id])


def button(state: GameState):
    # Not given, as it can be worked out: players are in seat order, so it's the player before the small blind (or the small blind heads-up)
    small = next(index for index, player in enumerate(state.players) if player.blind is Blind.SMALL)
    return state.players[small] if len(state.players) == 2 else state.players[small - 1]


def myAI(state: GameState) -> Action:
    for record in state.previous_hands:
        learn(record)

    me = state.my_player
    to_call = max(player.chips_bet for player in state.players) - me.chips_bet
    left = me.chips_in_stack - to_call
    raises = [action for action in state.history if action.kind is Action.Kind.RAISE]  # This hand's, in order
    board = {card.rank for card in state.community_cards}
    paired = any(card.rank in board for card in me.hole_cards) or len({card.rank for card in me.hole_cards}) == 1

    def bet(chips: int) -> Action:
        return Action.raise_by(min(max(chips, state.min_raise), left)) if left > 0 else Action.call()

    if not state.community_cards:
        if raises:
            raiser = raises[-1].id
            # Someone who rarely raises has a strong hand when they re-raise, but a player caught raising rubbish could have anything
            tight = rate(raiser, "pfr", 0.15) < 0.1 and bluffs(raiser) == 0
            if good(me.hole_cards) and not (tight and len(raises) > 1):
                return Action.call()
            return Action.check() if to_call == 0 else Action.fold()

        if good(me.hole_cards):
            return bet(3 * state.big_blind)

        # Nobody has raised: on the button, steal the blinds from players who rarely put chips in
        blinds = [player for player in state.players if player.blind is not None and player is not me]
        if button(state) is me and all(rate(player.id, "vpip", 0.3) < 0.25 for player in blinds):
            return bet(3 * state.big_blind)

        return Action.check() if to_call == 0 else Action.fold()

    if paired:
        return bet(state.chips_in_pot // 2)

    # A bet from a player who raises after the flop twice as often as they call is often a bluff, so call it while it's small
    bettor = notes[raises[-1].id] if raises and raises[-1].street == len(state.community_cards) - 2 else Counter()
    if to_call and bettor["raises"] + 1 > 2 * (bettor["calls"] + 1) and to_call * 3 <= state.chips_in_pot:
        return Action.call()

    return Action.check() if to_call == 0 else Action.fold()
