class Player:

    def __init__(self):
        pass


    def __repr__(self):
        return "Player()"


    def __eq__(self, other):
        return True if isinstance(other, Player) else NotImplemented


    def __hash__(self):
        return 0
    