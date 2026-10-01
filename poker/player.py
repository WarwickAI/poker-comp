class Player:

    def __init__(
        self,
        chips: int,
        is_small_blind: bool,
        is_big_blind: bool,
        has_folded: bool,
        chips_bet: int
    ):
        if not isinstance(chips, int):
            type_name = type(chips).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected chips to be an int, but it was {article} {type_name}")

        if chips < 0:
            raise ValueError(f"Expected chips to be at least 0, but it was {chips}")
        
        if not isinstance(is_small_blind, bool):
            type_name = type(is_small_blind).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected is_small_blind to be a bool, but it was {article} {type_name}")
        
        if not isinstance(is_big_blind, bool):
            type_name = type(is_big_blind).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected is_big_blind to be a bool, but it was {article} {type_name}")

        if is_small_blind and is_big_blind:
            raise ValueError("Expected at most one of is_small_blind and is_big_blind to be True")

        if not isinstance(has_folded, bool):
            type_name = type(has_folded).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected has_folded to be a bool, but it was {article} {type_name}")

        if not isinstance(chips_bet, int):
            type_name = type(chips_bet).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected chips_bet to be an int, but it was {article} {type_name}")

        if chips_bet < 0:
            raise ValueError(f"Expected chips_bet to be at least 0, but it was {chips_bet}")

        self.chips = chips
        self.is_small_blind = is_small_blind
        self.is_big_blind = is_big_blind
        self.has_folded = has_folded
        self.chips_bet = chips_bet


    def __repr__(self):
        return f"Player({self.chips}, {self.is_small_blind}, {self.is_big_blind}, {self.has_folded}, {self.chips_bet})"


    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented

        if self.chips != other.chips:
            return False

        if self.is_small_blind != other.is_small_blind:
            return False

        if self.is_big_blind != other.is_big_blind:
            return False

        if self.has_folded != other.has_folded:
            return False

        if self.chips_bet != other.chips_bet:
            return False

        return True


    def __hash__(self):
        return hash((self.chips, self.is_small_blind, self.is_big_blind, self.has_folded, self.chips_bet))
    