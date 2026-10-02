from enum import Enum

class Blind(Enum):
    SMALL = "small"
    BIG = "big"

class Player:
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
