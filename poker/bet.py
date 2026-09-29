from enum import Enum

class Action:
    
    class Kind(Enum):
        CHECK
        CALL
        RAISE
        FOLD

    def __init__(self, kind, amount = None):
        self.kind = kind
        self.amount = amount

    @staticmethod
    def check():
        return Action(Action.Kind.CHECK)

    @staticmethod
    def call():
        return Action(Action.Kind.CALL)

    @staticmethod
    def raise_by(amount):
        return Action(Action.Kind.RAISE, amount)

    @staticmethod
    def fold():
        return Action(Action.Kind.FOLD)
