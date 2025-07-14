from Automata.DFA import DFA

class MinDFA(DFA):
    __slots__ = DFA.__slots__ + ('unreachable_states',)
    def __init__(self) -> None:
        super().__init__()
        self.unreachable_states: set = set()

    def build(self, dfa: DFA) -> None:
        '''
        Uses Hopcrofts algorithm and then builds the minimized automaton
        '''

        # Start the Hopcroft Algorithm
        P:set = {frozenset(dfa.final_states), frozenset(dfa.states - dfa.final_states)}
        W:set = P.copy()
        
        while W:
            A:set = W.pop() # choose and remove a set A from W
            for char in dfa.alphabet:
                X:set = {s for s in self.states if dfa.transitions.get(s).get(char) in A } # transitions on c that lead to a state in A
  
                for Y in P:

                    intrsct: frozenset = frozenset(X & Y)
                    diffrnc: frozenset = frozenset(Y - X)
                    if len(intrsct) > 0 and len(diffrnc) > 0:

                        if Y in W:
                            W.remove(Y) # change Y for X & Y and Y - X
                            # W.update([intrsct, diffrnc])
                            W.add(intrsct)
                            W.add(diffrnc)
                        else:
                            if len(intrsct) <= len(diffrnc):
                                W.add(intrsct)
                            else:
                                W.add(diffrnc)
           
        # Finish the hopcroft algorithm

        # build the automaton's new transitions and states
        minimized_states: list = list(P)
        minimized_transitions:dict = {}
        minimized_final_states: set = set()
        state_map: dict = {s: i for i, group in enumerate(minimized_states) for s in group}
        print(f"State Map: {state_map}")
        print(f"alphabet: {dfa.alphabet}")
        print(f"P: {P}")
        for group in minimized_states:
            rep = next(iter(group))
            src = state_map[rep]
            minimized_transitions[src] = {}
            for symbol in dfa.alphabet:
                target = dfa.transitions.get(rep, {}).get(symbol)
                if target is not None:
                    dst = state_map[target]
                    minimized_transitions[src][symbol] = dst
            if group & dfa.final_states:
                minimized_final_states.add(src)
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

    def accepts(self) -> None:
        pass

    def get_automaton(self) -> 'MinDFA':
        return self

    def print_automaton(self) -> None:
        print(f"States : {self.states}")
        print(f"Transitions : {self.transitions}")
        print(f"Initial state : {self.initial_state}")
        print(f"Final state : {self.final_states}")

def build_min_dfa(dfa: DFA) -> MinDFA:
    min_dfa = MinDFA()
    min_dfa.build(dfa=dfa)
    min_dfa.print_automaton()