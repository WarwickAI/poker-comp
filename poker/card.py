class Card:
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __repr__(self):
        return f"Card({self.rank}, {self.suit})"
    
    def __eq__(self, other):
        return self.rank == other.rank && self.suit == other.suit
    
    def __hash__(self):
        return hash((self.rank, self.suit))
