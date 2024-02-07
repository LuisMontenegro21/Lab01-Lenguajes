
#----------------------------------------
# Clases del AFD
#----------------------------------------

# Archivo para la conversión del AFN a un AFD mediante construcción de subconjuntos
from graphviz import Digraph


class DFA:
    # tomar los parametros para construir el DFA con el método de subconjuntos
    def __init__(self, params):
        self.num_states = params['num_states']
        self.states = params['states']
        self.num_alphabet = params['num_alphabet']
        self.alphabet = params['alphabet']
        self.start = params['start']
        self.num_final = params['num_final']
        self.final_states = params['final_states']
        self.num_transitions = params['num_transitions']
        self.transitions = params['transitions']

    # para realizar la transición épsilon  
    def epsilonClosure(self, states):
        # crear la cerradura y el stack
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            # para cada transicion se ve si tiene epsilon como siguiente
            for transition in self.transitions:
                if transition[0] == state and transition[1] == 'ε':
                    next_state = transition[2]
                    
                    # si el estado aún no está, agregarlo
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure
    
    # para encontrar a qué estados se puede acceder desde el estado actual
    def move(self, states, symbol):
        next_states = set()
        for transition in self.transitions:
            if transition[0] in states and transition[1] == symbol:
                next_states.add(transition[2])
        # retorna un conjunto de estados accesibles desde el estado actual
        return next_states

    def constructDFA(self):
        
        # Initialize with the epsilon closure of the NFA's start state
        initial_state = self.epsilonClosure({self.start})
        dfa_states = {frozenset(initial_state): 'q0'}  # Maps sets of NFA states to DFA state names
        worklist = [initial_state]  # States to be processed
        dfa_transitions = []
        dfa_final_states = set()

        while worklist:
            current = worklist.pop()
            for symbol in self.alphabet:
                if symbol != 'ε': 
                    # Moverse en los estados y aplicar la cerradura epsilon
                    next = self.epsilonClosure(self.move(current, symbol))
                    if not frozenset(next) in dfa_states:
                        # New DFA state discovered
                        dfa_states[frozenset(next)] = f'q{len(dfa_states)}'
                        worklist.append(next)
                    # Record the transition
                    dfa_transitions.append((dfa_states[frozenset(current)], symbol, dfa_states[frozenset(next)]))
                    # Check if any of the NFA final states are in the new DFA state
                    if any(state in self.final_states for state in next):
                        dfa_final_states.add(dfa_states[frozenset(next)])

        
        return {
            'states': list(dfa_states.values()),
            'transitions': dfa_transitions,
            'start': dfa_states[frozenset(initial_state)],
            'final_states': list(dfa_final_states),
        }

    

    


