class State:

    def __init__(self):
        pass


    def __repr__(self):
        return "State()"


    def __eq__(self, other):
        return True if isinstance(other, State) else NotImplemented

    
    def __hash__(self):
        return 0
