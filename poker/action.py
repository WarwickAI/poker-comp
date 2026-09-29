from enum import Enum

class Action:
    
    class Kind(Enum):
        CHECK
        CALL
        RAISE
        FOLD

    def __init__(self, kind: Action.Kind, amount: int | None = None):
        if not isinstance(kind, Action.Kind):
            raise TypeError(f"Expected kind to be an Action.Kind, but it was a {type(kind).__name__}")
        if kind is Action.Kind.RAISE:
            if not isinstance(amount, int):
                raise TypeError(f"Expected amount to be an int, but it was a {type(amount).__name__}")
            if amount <= 0:
                raise ValueError(f"Expected amount to be strictly positive, but it was {amount}")
        elif amount is not None:
            raise TypeError(f"Expected no amount, but got {amount}")
        self.kind = kind
        self.amount = amount

    @staticmethod
    def check() -> Action:
        return Action(Action.Kind.CHECK)

    @staticmethod
    def call() -> Action:
        return Action(Action.Kind.CALL)

    @staticmethod
    def raise_by(amount: int) -> Action:
        return Action(Action.Kind.RAISE, amount)

    @staticmethod
    def fold() -> Action:
        return Action(Action.Kind.FOLD)
