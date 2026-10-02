from card import Card
from player import Player

class MyPlayer(Player):
    def __init__(self, blind: Blind | None = None, has_folded: bool = False, chips_in_stack: int = 0, chips_bet: int = 0, hole_cards: List[Card]):
        super().__init__(blind, has_folded, chips_in_stack, chips_bet)
        
        if not isinstance(hole_cards, List):
            type_name = type(hole_cards).__name__
            article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
            raise TypeError(f"Expected hole_cards to be a List, but it was {article} {type_name}")

        for card in hole_cards:
            if not isinstance(card, Card):
                type_name = type(card).__name__
                article = "an" if type_name.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')) else "a"
                raise TypeError(f"Expected hole_cards to be a List of Cards, but {card} is {article} {type_name}")

        hole_card_count = len(hole_cards)
        if hole_card_count != 2:
            raise ValueError(f"Expected 2 hole_cards, but got {hole_cards_count}")

        if hole_cards[0] == hole_cards[1]:
            raise ValueError(f"Expected the hole cards to be different, but got {hole_cards[0]} twice")
        
        self.hole_cards = hole_cards

    def __repr__(self):
        return f"""
        MyPlayer(blind={self.blind}, has_folded={self.has_folded}, chips_in_stack={self.chips_in_stack}, chips_bet={self.chips_bet}, hole_cards={self.hole_cards})
        """
