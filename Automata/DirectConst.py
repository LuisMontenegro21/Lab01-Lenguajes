from Algorithms.Postfix import infix_to_postfix
from Automata.Automaton import Automaton
from typing import Optional

class Node:
    def __init__(self, value: str, left:Optional['Node']=None, right:Optional['Node']=None) -> None:
        self.value = value
        self.left: Node = left
        self.right: Node = right    
        self.nullable: bool = False
        self.firstpos: set[int] = set()
        self.lastpos: set[int] = set()
        self.position: int = 0

    def as_string(self) -> str:
        '''Represents node as a string'''
        return f"Node: {self.value} Position: {self.position} Firstpos: {self.firstpos} Lastpos: {self.lastpos} Nullable: {self.nullable}"

class DirectDFA(Automaton):

    def __init__(self, regex:str) -> None:
        super().__init__() # get Automaton constructor
        self.regex: str = regex
        self.followpos_: dict[int, set[int]] = {} # to compute followpos after computing firstpos, lastpos, nullable
        self.position_map_: dict[int, str] = {} # map positions to values
        self.val_pos: dict[str, int] = {} # map values to positions

    def build_syntax_tree(self) -> list[Node]:
        self.regex += '#'
        postfix:list[str] = infix_to_postfix(self.regex)
        stack:list[Node] = []

        for char in postfix:
            
            if char not in self.precedence.keys():
                stack.append(Node(char))
            if char in {'*', '+', '?'}:
                operand = stack.pop()
                node = Node(char, operand)
                stack.append(node)
            if char in {'|', '.'}:
                right = stack.pop()
                left = stack.pop()
                node = Node(char, left, right)
                stack.append(node)
        # return root
        if stack:
            return stack.pop()
        else:
            return None
    
    # calls like: assing_position(root, [0])
    def assign_positions(self, node: Node, counter: list[int], result:dict[int, str]) -> None:
        if node is None:
            return
        if node.left:
            self.assign_positions(node.left, counter, result)
        if node.right:
            self.assign_positions(node.right, counter, result)
        
        if not node.left and not node.right and node.value != 'ε':
            counter[0] += 1
            node.position = counter[0]
            result[node.position] = node.value
            self.val_pos[node.value] = node.position
        
    def print_properties(self, node:Node) -> None:
        '''
        Function used to check the properties being correctly set 
        '''
        if node is None:
            return
        if node.left:
            self.print_properties(node.left)
        if node.right:
            self.print_properties(node.right)
        print(node.as_string())

        

    def nullable_firstpos_lastpos(self, node: Node) -> None:
        '''
        Compute all 3: nullable, firstpos, lastpos
        '''
        if node is None:
            return 
        if node.left:
            self.nullable_firstpos_lastpos(node.left)
        if node.right:
            self.nullable_firstpos_lastpos(node.right)
        
        if not node.left and not node.right:
            node.nullable = False if node.value != 'ε' else True
            if node.position:
                node.firstpos = {node.position}
                node.lastpos = {node.position}
            return
        
        match node.value:
            case '|':
                node.nullable = node.left.nullable or node.right.nullable
                node.firstpos = node.left.firstpos | node.right.firstpos
                node.lastpos = node.left.lastpos | node.right.firstpos
            case '.':
                node.nullable = node.left.nullable and node.right.nullable
                node.firstpos = (node.left.firstpos if not node.left.nullable else node.left.firstpos | node.right.firstpos)
                node.lastpos = (node.right.lastpos if not node.right.nullable else node.left.lastpos | node.right.lastpos)
            case '*':
                node.nullable = True
                node.firstpos = node.left.firstpos
                node.lastpos = node.left.lastpos
            case '?':
                node.nullable = True
                node.firstpos = node.left.firstpos
                node.lastpos = node.left.lastpos
            case '+':
                node.nullable = node.left.nullable # only false if epsilon not allowed
                node.firstpos = node.left.firstpos
                node.lastpos = node.left.lastpos
  

    def followpos(self, node: Node) -> None:
        if node is None:
            return
        if node.left:
            self.followpos(node.left)
        if node.right:
            self.followpos(node.right)
        
        if node.value == '.':
            for i in node.left.lastpos:
                self.followpos_.setdefault(i, set()).update(node.right.firstpos)
        
        if node.value in {'*', '+'}:
            for i in node.lastpos:
                self.followpos_.setdefault(i, set()).update(node.firstpos)

    
    def build_dfa(self, root: Node, followpos: dict[int, set[int]], pos_to_symbol: dict[int, str]) -> dict:
        if root is None:
            return {}
        
        dfa: dict = {}
        states: list[frozenset[int]] = []
        unmarked: list[frozenset[int]] = []
        accepting_states: set[frozenset[int]] = set()
        start: frozenset = frozenset(root.firstpos)
        states.append(start)
        unmarked.append(start)
        dfa[start] = {}

        end_marker_pos: int = self.val_pos.get('#', 0)
        
        while unmarked:
            current: frozenset[int] = unmarked.pop()
            symbol_map: dict[str, set[int]] = {}

            for pos in current:
                symbol:str = pos_to_symbol[pos]
                if symbol == '#':
                    continue
                symbol_map.setdefault(symbol, set()).update(followpos.get(pos, set()))
            
            for symbol, positions in symbol_map.items():
                positions_frozen = frozenset(positions)
                if positions_frozen not in states:
                    states.append(positions_frozen)
                    unmarked.append(positions_frozen)
                    dfa[positions_frozen] = {}
                dfa[current][symbol] = positions_frozen
            
            if end_marker_pos in current:
                accepting_states.add(current)
        
        print(f"states: {states}")
        print(f"accepting states: {accepting_states}")
        return dfa
    
    def run_dfa(self, w: str) -> bool:
        w_list: list[str] = list(w) # convert to list




# TODO change passing arguments to just leave the logic within the dfa to speeds things up
def build_direct_dfa(regex: str):
    dfa = DirectDFA(regex=regex) # make instance
    root: Node = dfa.build_syntax_tree() # gather root of tree
    dfa.assign_positions(node=root, counter=[0], result=dfa.position_map_) # assign positions to nodes
    dfa.nullable_firstpos_lastpos(node=root) # compute firstpos, lastpos, nullable
    dfa.print_properties(node=root) # print properties to make sure they're correct
    dfa.followpos(node=root) # compute followpos
    print(f"Followpos: {dfa.followpos_}") # print followpos

    dfa_dict = dfa.build_dfa(root=root, followpos=dfa.followpos_, pos_to_symbol=dfa.position_map_) # build DFA
    print(f"DFA: {dfa_dict}") # print it