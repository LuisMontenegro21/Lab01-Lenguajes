from Automata.DFA import DFA

class MinDFA(DFA):
    __slots__ = DFA.__slots__ + ('unreachable_states',)
    def __init__(self) -> None:
        super().__init__()
        self.unreachable_states: set = set()

    def build(self) -> None:
        '''
        Uses Hopcrofts algorithm 
        '''
        P:set = {self.final_states, self.states - self.final_states}
        W:set = {self.final_states, self.states - self.final_states}
        
        while W:
            A = W.pop() # choose and remove a set A from W
            for char in self.alphabet:
                X:set = {s for s in self.states if self.transitions.get(s, {}).get(char) in A } # transitions on c that lead to a state in A
                for Y in P:
                    intrsct: set = X & Y
                    diffrnc: set = Y - X
                    if len(intrsct) > 0 and len(diffrnc) > 0:
                        if Y in W:
                            P.remove(Y) # change Y for X & Y and Y - X
                            P.add(intrsct)
                            P.add(diffrnc)
                        else:
                            if len(intrsct) <= len(diffrnc):
                                W.add(intrsct)
                            else:
                                W.add(diffrnc)


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

    def print_automata(self) -> None:
        pass

def build_min_dfa(dfa: DFA) -> MinDFA:
    pass