# --------------------------------------------------------
# Automaton class to define general properties and classes
# used among all other automata types
# ---------------------------------------------------------
from typing import Optional

class PNode:

    '''
    Base parent class for a Node
    '''
    __slots__ = ('value', 'left', 'right') # use slots to avoid __dict__ being generated. New class attributes become dynamically immutable

    def __init__(self, value: Optional[str], left: Optional['PNode'] = None, right: Optional['PNode'] = None) -> None:
        self.value = value
        self.left: PNode = left
        self.right: PNode = right
    
    def as_string(self) -> None:
        raise NotImplementedError()


class Automaton:
    def __init__(self)->None:
        self.precedence: dict[int, str]  = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3} # keep track of operator precedence 
        self.states: list[frozenset[int]] = []
        self.accepting_states: set[frozenset[int]] = set()
        self.start: frozenset = frozenset()
        self.dfa: dict = {}

    def get_automata(self) -> None:
        raise NotImplementedError()
    
    def print_automata(self) -> None:
        raise NotImplementedError()
    
    def accepts(self) -> None:
        raise NotImplementedError(f"Please implement this method on your class")

    def build(self) -> None:
        raise NotImplementedError(f"Please implement this method on your class")
    