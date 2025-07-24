# --------------------------------------------------------
# Automaton class to define general properties and classes
# used among all other automata types
# ---------------------------------------------------------

class Automaton:
    def __init__(self)->None:
        self.precedence: dict[int, str]  = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3} # keep track of operator precedence 
        self.states: set[int] = set()
        self.final_states: set[int] = set()
        self.initial_state: int = int
        self.transitions: dict[str, dict[str, int]] = {}

    def get_automaton(self) -> None:
        raise NotImplementedError()
    
    def print_automaton(self) -> None:
        raise NotImplementedError()
    
    def accepts(self) -> None:
        raise NotImplementedError(f"Please implement this method on your class")

    def build(self) -> None:
        raise NotImplementedError(f"Please implement this method on your class")

    def get_name(self) -> str:
        return f"{self.__class__.__qualname__}"
    