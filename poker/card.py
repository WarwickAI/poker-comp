from rank import Rank
from suit import Suit

class Card:
    
    def __init__(self, rank: Rank, suit: Suit):
        if not isinstance(rank, Rank):
            raise TypeError(f"Expected rank to be a Rank, but it was a {type(rank).__name__}")
        if not isinstance(suit, Suit):
            raise TypeError(f"Expected suit to be a Suit, but it was a {type(suit).__name__}")
        self.rank = rank
        self.suit = suit
    
    def __repr__(self):
        return f"Card({self.rank}, {self.suit})"
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit if isinstance(other, Card) else NotImplemented
    
    def __hash__(self):
        return hash((self.rank, self.suit))
