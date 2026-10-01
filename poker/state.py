class State:

    def __init__(self, chips_in_pot: int):
        if not isinstance(chips_in_pot, int):
            type_name = type(chips_in_pot).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected chips_in_pot to be an int, but it was {article} {type_name}")

        if chips_in_pot <= 0:
            raise ValueError(f"Expected chips_in_pot to be greater than 0, but it was {chips_in_pot}")

        self.chips_in_pot = chips_in_pot


    def __repr__(self):
        return f"State({self.chips_in_pot})"


    def __eq__(self, other):
        return self.chips_in_pot == other.chips_in_pot if isinstance(other, State) else NotImplemented

    
    def __hash__(self):
        return hash((self.chips_in_pot))
