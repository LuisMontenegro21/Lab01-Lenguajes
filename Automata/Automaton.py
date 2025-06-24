from typing import Optional

class Node:
    '''
    Base parent class for a Node
    '''
    def __init__(self, value, left: Optional['Node'] = None, right: Optional['Node'] = None) -> None:
        self.value = value
        self.left: Node = left
        self.right: Node = right


class Automaton:
    def __init__(self)->None:
        self.precedence: dict[int, str]  = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3} # keep track of operator precedence 

