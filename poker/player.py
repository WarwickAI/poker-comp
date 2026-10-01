class Player:

    def __init__(self, is_small_blind: bool, is_big_blind: bool):
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
        
        self.is_small_blind = is_small_blind
        self.is_big_blind = is_big_blind


    def __repr__(self):
        return f"Player({self.is_small_blind}, {self.is_big_blind})"


    def __eq__(self, other):
        if isinstance(other, Player):
            return self.is_small_blind == other.is_small_blind and self.is_big_blind == other.is_big_blind
        return NotImplemented


    def __hash__(self):
        return hash((self.is_small_blind, self.is_big_blind))
    