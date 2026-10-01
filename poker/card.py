from rank import Rank
from suit import Suit

class Card:
    def __init__(self, rank: Rank, suit: Suit):
        if not isinstance(rank, Rank):
            type_name = type(rank).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected rank to be a Rank, but it was {article} {type_name}")
            
        self.rank = rank
        
        if not isinstance(suit, Suit):
            type_name = type(suit).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected suit to be a Suit, but it was {article} {type_name}")
        
        self.suit = suit
    
    def __repr__(self):
        return f"Card({self.rank}, {self.suit})"
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit if isinstance(other, Card) else NotImplemented

    def __hash__(self):
        return hash((self.rank, self.suit))
