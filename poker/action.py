from enum import Enum


class Action:
    class Kind(Enum):
        CHECK = "check"
        CALL = "call"
        RAISE = "raise"
        FOLD = "fold"

    def __init__(self, kind: Action.Kind, amount: int | None = None):
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

    def __repr__(self):
        match self.kind:
            case self.Kind.CHECK:
                return "Action.check()"
            
            case self.Kind.CALL:
                return "Action.call()"
            
            case self.Kind.RAISE:
                return f"Action.raise_by({self.amount})"
            
            case self.Kind.FOLD:
                return "Action.fold()"

    def __eq__(self, other):
        return self.kind == other.kind and self.amount == other.amount if isinstance(other, Action) else NotImplemented

    def __hash__(self):
        return hash((self.kind, self.amount))
