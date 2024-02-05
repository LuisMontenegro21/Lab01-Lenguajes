# Archivo para la reducción de un AFD
from graphviz import Digraph
import re 

class DFA_min:

    def __init__(self, states, num_states, num_alphabet, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.num_states = num_states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.num_alphabet = num_alphabet

        self.states_dict = dict()
        for i in range (self.num_states):
            self.states_dict[self.states[i]] = i
        self.alphabet_dict = dict()
        for i in range (self.num_alphabet):
            self.alphabet_dict[self.alphabet[i]] = i
    
    
    def minimize(self):
        def hopcroft():
            dfa_min =  Digraph()
            accepting_states = self.accept_states
            non_accepting_states = set(self.states) - accepting_states
            equivalence_classes = [accepting_states, non_accepting_states]

            
            worklist = [accepting_states, non_accepting_states]

            while worklist:
                P = worklist.pop()
                for symbol in self.alphabet:
                    
                    state_map = {}
                    for state in P:
                        next_state = self.transitions.get((state, symbol), None)
                        if next_state is not None:
                            if next_state in state_map:
                                state_map[next_state].append(state)
                            else:
                                state_map[next_state] = [state]

                    
                    new_equivalence_classes = list(state_map.values())
                    for new_class in new_equivalence_classes:
                        if len(new_class) > 1:
                            equivalence_classes.remove(P)
                            equivalence_classes.extend(new_equivalence_classes)
                            worklist.extend(new_equivalence_classes)
                            break

            
            simplified_states = [i for i, eq_class in enumerate(equivalence_classes)]
            simplified_transitions = {}
            simplified_start_state = simplified_states[equivalence_classes.index(set([self.start_state]))]
            simplified_accept_states = {i for i, eq_class in enumerate(equivalence_classes) if any(state in accepting_states for state in eq_class)}

            for i, eq_class in enumerate(equivalence_classes):
                for state in eq_class:
                    for symbol in self.alphabet:
                        next_state = self.transitions.get((state, symbol), None)
                        if next_state is not None:
                            simplified_transitions[(i, symbol)] = simplified_states[equivalence_classes.index(set([next_state]))]

            for state in self.states:
                dfa_min.node(state)
            for (source, symbol), target in self.transitions.items():
                dfa_min.edge(source,target,label = symbol)
            dfa_min.render('minimized dfa', view = True)
            return DFA_min(simplified_states, len(simplified_states), self.num_alphabet, self.alphabet, simplified_transitions, simplified_start_state, simplified_accept_states)

        return hopcroft()