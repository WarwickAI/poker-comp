from card import Card
from player import Player

class MyPlayer(Player):
    def __init__(self, blind: Blind | None = None, has_folded: bool = False, chips_in_stack: int = 0, chips_bet: int = 0, hole_cards: List[Card]):
        super().__init__(blind, has_folded, chips_in_stack, chips_bet)
        
        self.hole_cards = hole_cards

    def __repr__(self):
        return f"""
        MyPlayer(blind={self.blind}, has_folded={self.has_folded}, chips_in_stack={self.chips_in_stack}, chips_bet={self.chips_bet}, hole_cards={self.hole_cards})
        """
