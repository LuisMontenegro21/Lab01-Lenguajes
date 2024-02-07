
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
        
        self.start = str(self.start)
        self.final_states = set(map(str, self.final_states))
        
        # Empezar la cerradura épsilon con el estado inicial
        initial_closure = self.epsilonClosure({self.start})
        dfa_states = {frozenset(initial_closure): 'q0'}  # MMapear los estados del AFN a AFD
        worklist = [frozenset(initial_closure)]  # estados a ser procesados
        dfa_transitions = []
        dfa_final_states = set()


        state_name_mapping = {'q0': frozenset(initial_closure)}
        counter = 1

        while worklist:
            current = worklist.pop(0)
            for symbol in self.alphabet:
                if symbol != 'ε': 
                    # Moverse en los estados y aplicar la cerradura epsilon
                    next_state = frozenset(self.epsilonClosure(self.move(current, symbol)))

                    if next_state not in state_name_mapping.values():
                        # nuevo estado del AFD descubierto
                        state_name_mapping[f'q{counter}'] = next_state
                        dfa_states[next_state] = f'q{counter}'
                        counter += 1
                        worklist.append(next_state)

                    from_state = [name for name, states in state_name_mapping.items() if states == current][0]
                    to_state = [name for name, states in state_name_mapping.items() if states == next_state][0]
                    dfa_transitions.append((from_state, symbol, to_state))
                
   

                    # When checking for final states in the DFA construction loop
                    if next_state & self.final_states:
                        dfa_final_states.add(to_state)


        
        return {
            'states': list(dfa_states.values()),
            'transitions': dfa_transitions,
            'start': dfa_states[frozenset(initial_closure)],
            'final_states': list(dfa_final_states),
        }

    

    


