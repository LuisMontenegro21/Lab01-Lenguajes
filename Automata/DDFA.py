from Algorithms.Postfix import infix_to_postfix
from Graph.Vizualizer import visualize_automaton
from Automata.Automaton import Automaton
from Automata.Nodes import Node 




class DDFA(Automaton):
    __slots__ = ('followpos_', 'position_map_', 'val_pos', 'regex', 'root', 'initial_state', 'final_state', 'transitions', 'states', 'alphabet')

    def __init__(self) -> None:
        super().__init__() # get Automaton constructor
        self.followpos_: dict[int, set[int]] = {} # to compute followpos after computing firstpos, lastpos, nullable
        self.position_map_: dict[int, str] = {} # map positions to values
        self.val_pos: dict[str, int] = {} # map values to positions
        self.regex:str = None
        self.root:Node = None

    def get_automaton(self) -> 'DDFA':
        return self
    
    def print_automaton(self) -> None:
        print(f"States: {self.states}")
        print(f"Transitions: {self.transitions}")
        print(f"Initial state: {self.initial_state}")
        print(f"Final states: {self.final_states}")
    

    def build_syntax_tree(self, regex:str) -> Node:
        postfix:list[str] = infix_to_postfix(regex)
        stack:list[Node] = []

        for char in postfix:
            
            if char not in self.precedence.keys():
                stack.append(Node(char))

            elif char in {'|', '.'}:
                right = stack.pop()
                left = stack.pop()
                node = Node(char, left, right)
                stack.append(node)

            elif char in {'*', '+', '?'}:
                operand = stack.pop()
                node = Node(char, operand)
                stack.append(node)

        # set root
        self.root = stack.pop() if stack else None
        return self.root
    
    # calls like: assing_position(root, [0])
    def assign_positions(self, node: Node, counter: list[int]) -> None:
        if node is None:
            return
        if node.left:
            self.assign_positions(node.left, counter)
        if node.right:
            self.assign_positions(node.right, counter)
        
        if not node.left and not node.right and node.value != 'ε':
            counter[0] += 1
            node.position = counter[0]
            self.position_map_[node.position] = node.value
            self.val_pos[node.value] = node.position
        
    def print_properties(self, node:Node) -> None:
        '''
        Function used to check the properties being correctly set 
        Use for debugging or whatever
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

    def build(self, regex:str, visualize:bool = False) -> None:
        self.regex = regex + '#' # add end marker character
        self.root = self.build_syntax_tree(regex=self.regex) 
        self.assign_positions(node=self.root, counter=[0]) # assign positions to nodes
        self.nullable_firstpos_lastpos(node=self.root) # compute firstpos, lastpos, nullable
        self.followpos(node=self.root) # compute followpos
        if self.root is None:
            return {}
        
        transitions: dict = {}
        states: set[frozenset[int]] = set()
        unmarked: set[frozenset[int]] = set()
        accepting_states: set[frozenset[int]] = set()
        start: frozenset = frozenset(self.root.firstpos)
        states.add(start)
        unmarked.add(start)
        transitions[start] = {}

        end_marker_pos: int = self.val_pos.get('#', 0) # get end marker position
        
        while unmarked:
            current: frozenset[int] = unmarked.pop()
            symbol_map: dict[str, set[int]] = {}

            for pos in current:
                symbol:str = self.position_map_[pos]
                if symbol == '#': # if symbol is the final one, skip iteration
                    continue
                symbol_map.setdefault(symbol, set()).update(self.followpos_.get(pos, set()))
            
            for symbol, positions in symbol_map.items():
                positions_frozen = frozenset(positions)
                if positions_frozen not in states:
                    states.add(positions_frozen)
                    unmarked.add(positions_frozen)
                    transitions[positions_frozen] = {}
                transitions[current][symbol] = positions_frozen
            
            if end_marker_pos in current:
                accepting_states.add(current)
        
        if visualize:
            # transform frozensets to integers for better visuals (only necessary if visualizing the dfa)
            all_states = list(transitions.keys()) + [v for d in transitions.values() for v in d.values()]
            unique_states = sorted(set(all_states), key=lambda x: sorted(x))
            state_map = {s: i for i, s in enumerate(unique_states)}

            new_transitions: dict = {}
            for src_set, edge_dict in transitions.items():
                src_id = state_map[src_set]
                new_transitions[src_id] = {}
                for symbol, dst_set in edge_dict.items():
                    dst_id = state_map[dst_set]
                    new_transitions[src_id][symbol] = dst_id
            
            # update self's attributes 
            self.final_states = {state_map[s] for s in accepting_states}
            self.states = set(state_map.values())
            self.initial_state = state_map[start]
            self.transitions = new_transitions
        else:
            # update self's attributes (harder to visualize)
            self.final_states = accepting_states
            self.states = states
            self.initial_state = start
            self.transitions = transitions

    def accepts(self, w: str | list) -> bool:
        if isinstance(w, str):
            w: list[str] = list(w) # convert to list if not already
        current: frozenset = self.initial_state
        for chr in w:
            if chr not in self.transitions[current]:
                print(f"Halting on char '{chr}' since no transition was found")
                return False
            current = self.transitions[current][chr]
        return current in self.final_states # check if our current state matches an accepting state





def build_direct_dfa(regex: str, w:str = None, visualize:bool = False) -> None:
    dfa = DDFA() # make instance
    dfa.build(regex=regex, visualize=visualize) # build DFA from a dfa
    dfa.print_automaton()
    if w:
        print(dfa.accepts(w=w))
    if visualize:
        visualize_automaton(automata=dfa.get_automaton())

    