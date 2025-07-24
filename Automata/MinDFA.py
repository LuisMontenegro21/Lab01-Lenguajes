from Automata.DFA import DFA
from Graph.Vizualizer import visualize_automaton

class MinDFA(DFA):
    __slots__ = DFA.__slots__ + ('unreachable_states', 'reverse_transitions')
    def __init__(self) -> None:
        super().__init__()
        self.unreachable_states: set = set()
        self.reverse_transitions: dict = {}
    
    #TODO fix this, it does not work 100%
    def build(self, dfa: DFA) -> None:
        '''
        Uses Hopcrofts algorithm and then builds the minimized automaton
        '''
        self.create_reverse_transitions(transitions=dfa.transitions, alphabet=dfa.alphabet) 

        # Start the Hopcroft Algorithm
        P:set[frozenset] = {frozenset(dfa.final_states), frozenset(dfa.states - dfa.final_states)}
        W:set = P.copy()
        
        while W:
            A:set = W.pop() # choose and remove a set A from W
            for char in dfa.alphabet:

                X:set = set() 
                for state in A: # check transitions on c that lead to a state in A
                    preds: set = self.reverse_transitions.get(char, {}).get(state, set())
                    X.update(preds)
                new_P: set = set()

                for Y in P:

                    intrsct: frozenset = frozenset(X & Y)
                    diffrnc: frozenset = frozenset(Y - X)
                    # new_P.remove(Y)
                    if intrsct and diffrnc:
                        new_P.add(intrsct)
                        new_P.add(diffrnc)

                    if len(intrsct) > 0 and len(diffrnc) > 0:

                        if Y in W:
                            W.remove(Y) # change Y for X & Y and Y - X
                            W.add(intrsct)
                            W.add(diffrnc)
                        else:
                            if len(intrsct) <= len(diffrnc):
                                W.add(intrsct)
                            else:
                                W.add(diffrnc)
                    else:
                        new_P.add(Y) # leave Y on P
            P = new_P
           
        # Finish the hopcroft algorithm

        # build the automaton's new transitions and states
        minimized_states:list = list(P)
        minimized_transitions:dict = {}
        minimized_final_states: set = set()
        state_map: dict = {s: i for i, group in enumerate(minimized_states) for s in group}


        for i, group in enumerate(minimized_states):
            minimized_transitions[i] = {}

            symbol_targets = {}

            for state in group:
                for symbol in dfa.alphabet:
                    target = dfa.transitions.get(state, {}).get(symbol)
                    if target is not None:
                        
                        symbol_targets.setdefault(symbol, set()).add(state_map[target])

            for symbol, targets in symbol_targets.items():
                minimized_transitions[i][symbol] = next(iter(targets))


            if group & dfa.final_states:
                minimized_final_states.add(i)

        self.states = set(range(len(minimized_states)))
        self.transitions = minimized_transitions
        self.final_states = minimized_final_states
        self.initial_state = state_map[self.initial_state]


    def set_reachable_states(self) -> None:
        reachable_states:set = {self.initial_state}
        new_states:set = {self.initial_state}

        while new_states: 
            temp: set = set()
            for q in new_states:
                for char in self.alphabet:
                    temp = temp | set(self.transitions[q].get(char))
            new_states = temp - reachable_states
            reachable_states = reachable_states | new_states
        
        self.unreachable_states = self.states - reachable_states
    
    def create_reverse_transitions(self, transitions: dict, alphabet: set) -> None:
        '''Gives a reverse transition dictionary to map transitions in reverse'''
        reverse_transitions: dict = {
            char: {} for char in alphabet
        }
        for src, transition in transitions.items():
            for char, dst in transition.items():
                reverse_transitions.setdefault(char, {}).setdefault(dst, set()).add(src)
        
        self.reverse_transitions = reverse_transitions

    def accepts(self, w: str) -> bool:
        state: int = self.initial_state
        for char in w:
            if char not in self.transitions.get(state, 0):
                print(f"Halting on char '{char}' since no transition was found")
                return False
            state = self.transitions[state].get(char)
        return state in self.final_states

    def get_automaton(self) -> 'MinDFA':
        return self

    def print_automaton(self) -> None:
        print(f"States : {self.states}")
        print(f"Transitions : {self.transitions}")
        print(f"Initial state : {self.initial_state}")
        print(f"Final state : {self.final_states}")

def build_min_dfa(dfa: DFA, w:str=None, visualize:bool=False) -> MinDFA:
    min_dfa = MinDFA()
    min_dfa.build(dfa=dfa)
    min_dfa.print_automaton()
    if w:
        print(min_dfa.accepts(w=w))
    if visualize:
        visualize_automaton(min_dfa.get_automaton())
    return min_dfa.get_automaton()