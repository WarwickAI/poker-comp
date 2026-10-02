from player import Player
from card import Card


class GameState:

    def __init__(self, players: list[Player], community_cards: list[Card], chips_in_pot: int):
        if not isinstance(players, list[Player]):
            type_name = type(players).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected players to be a list, but it was {article} {type_name}")

        if len(players) < 2:
            raise ValueError(f"Expected players to have a length of at least 2, but it had a length of {len(players)}")

        if not isinstance(community_cards, list[Card]):
            type_name = type(community_cards).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected community_cards to be a list, but it was {article} {type_name}")

        if len(community_cards) not in [0, 3, 4, 5]:
            raise ValueError(f"Expected community_cards to have a length of 0, 3, 4, or 5, but it had a length of {len(community_cards)}")
        
        if not isinstance(chips_in_pot, int):
            type_name = type(chips_in_pot).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected chips_in_pot to be an int, but it was {article} {type_name}")

        if chips_in_pot <= 0:
            raise ValueError(f"Expected chips_in_pot to be greater than 0, but it was {chips_in_pot}")

        self.chips_in_pot = chips_in_pot
        self.community_cards = community_cards
        self.players = players


    def __repr__(self):
        return f"State({self.players}, {self.community_cards}, {self.chips_in_pot})"


    def __eq__(self, other):
        if not isinstance(other, GameState):
            return NotImplemented

        if self.players != other.players:
                    return False

        if self.community_cards != other.community_cards:
                    return False

        if self.chips_in_pot != other.chips_in_pot:
            return False

        return True


    def __hash__(self):
        return hash((tuple(self.players), self.chips_in_pot, tuple(self.community_cards)))
    