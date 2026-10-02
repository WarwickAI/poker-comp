from enum import Enum

from card import Card


class Blind(Enum):
    SMALL = "small"
    BIG = "big"


class Player: # Players hash and equate by object identity
    def __init__(self, blind: Blind | None = None, has_folded: bool = False, chips_in_stack: int = 0, chips_bet: int = 0):
        if not isinstance(blind, Blind) and not isinstance(blind, None):
            type_name = type(blind).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected 'blind' to be a Blind or a None, but it was {article} {type_name}")
        
        self.blind = blind

        if not isinstance(has_folded, bool):
            type_name = type(has_folded).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected 'has_folded' to be a bool, but it was {article} {type_name}")

        self.has_folded = has_folded
        
        if not isinstance(chips_in_stack, int):
            type_name = type(chips_in_stack).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected 'chips_in_stack' to be an int, but it was {article} {type_name}")

        if chips_in_stack < 0:
            raise ValueError(f"Expected at least 0 chips in the stack, but there were {chips_in_stack}")
        
        self.chips_in_stack = chips_in_stack

        if not isinstance(chips_bet, int):
            type_name = type(chips_bet).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected 'chips_bet' to be an int, but it was {article} {type_name}")

        if chips_bet < 0:
            raise ValueError(f"Expected at least 0 chips bet, but there were {chips_bet}")
        
        self.chips_bet = chips_bet

    def __repr__(self):
        return f"Player(blind={self.blind}, has_folded={self.has_folded}, chips_in_stack={self.chips_in_stack}, chips_bet={self.chips_bet})"


class MyPlayer(Player): # MyPlayers are only constructed when myAI is called which requires that the player can act
    def __init__(self, *, blind: Blind | None = None, chips_in_stack: int = 0, chips_bet: int = 0, hole_cards: List[Card]):
        super().__init__(blind, False, chips_in_stack, chips_bet) # has_folded is False as the player can act
        
        if not isinstance(hole_cards, list):
            type_name = type(hole_cards).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected 'hole_cards' to be a list, but it was {article} {type_name}")

        for card in hole_cards:
            if not isinstance(card, Card):
                type_name = type(card).__name__
                article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
                raise TypeError(f"Expected 'hole_cards' to be a List of Cards, but {card} is {article} {type_name}")

        hole_card_count = len(hole_cards)
        if hole_card_count != 2:
            raise ValueError(f"Expected 2 hole cards, but got {hole_card_count}")

        if hole_cards[0] == hole_cards[1]:
            raise ValueError(f"Expected the hole cards to be different, but got {hole_cards[0]} twice")
        
        self.hole_cards = hole_cards

    def __repr__(self):
        return f"MyPlayer(blind={self.blind}, chips_in_stack={self.chips_in_stack}, chips_bet={self.chips_bet}, hole_cards={self.hole_cards})"
