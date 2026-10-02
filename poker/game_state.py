from player import Player
from card import Card


class GameState:
    def __init__(self, *, my_player: Player, players: list[Player], chips_in_pot: int = 0, community_cards: list[Card] = []):
        if not isinstance(my_player, Player):
            type_name = type(my_player).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected 'my_player' to be a Player, but it is {article} {type_name}")
            
        if not isinstance(players, list):
            type_name = type(players).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected 'players' to be a list, but it is {article} {type_name}")

        for player in players:
            if not isinstance(player, Player):
                type_name = type(player).__name__
                article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
                raise TypeError(f"Expected 'players' to be a list of Players, but {player} is {article} {type_name}")
            
        if not isinstance(chips_in_pot, int):
            type_name = type(chips_in_pot).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected 'chips_in_pot' to be an int, but it is {article} {type_name}")

        if chips_in_pot < 0:
            raise ValueError(f"Expected at least 0 chips in the pot, but got {chips_in_pot}")
            
        if not isinstance(community_cards, list):
            type_name = type(community_cards).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected 'community_cards' to be a list, but it is {article} {type_name}")

        for card in community_cards:
            if not isinstance(card, Card):
                type_name = type(card).__name__
                article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
                raise TypeError(f"Expected 'community_cards' to be a list of Cards, but {card} is {article} {type_name}")

        if chips_in_pot and not community_cards:
            raise ValueError("Expected the pot to be empty if there are no community cards")

        self.my_player = my_player
        self.players = players
        self.chips_in_pot = chips_in_pot
        self.community_cards = community_cards


    def __repr__(self):
        return f"GameState(my_player={self.my_player}, players={self.players}, chips_in_pot={self.chips_in_pot}, community_cards={self.community_cards})"


    def __eq__(self, other):
        if not isinstance(other, GameState):
            return NotImplemented

        if self.my_player != other.my_player:
            return False

        if self.players != other.players:
            return False

        if self.chips_in_pot != other.chips_in_pot:
            return False

        if self.community_cards != other.community_cards:
            return False

        return True


    def __hash__(self):
        return hash((self.my_player, tuple(self.players), self.chips_in_pot, tuple(self.community_cards)))
