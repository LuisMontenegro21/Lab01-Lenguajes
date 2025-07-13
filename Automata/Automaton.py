# --------------------------------------------------------
# Automaton class to define general properties and classes
# used among all other automata types
# ---------------------------------------------------------

class Automaton:
    def __init__(self)->None:
        self.precedence: dict[int, str]  = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3} # keep track of operator precedence 
        self.states: list[frozenset[int]] = []
        self.accepting_states: set[frozenset[int]] = set()
        self.start: frozenset = frozenset()
        self.dfa: dict = {}

    def get_automaton(self) -> None:
        raise NotImplementedError()
    
    def print_automaton(self) -> None:
        raise NotImplementedError()
    
    def accepts(self) -> None:
        raise NotImplementedError(f"Please implement this method on your class")

    def build(self) -> None:
        raise NotImplementedError(f"Please implement this method on your class")
    