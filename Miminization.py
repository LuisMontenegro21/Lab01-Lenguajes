# Archivo para la reducción de un AFD
from graphviz import Digraph


class DFA_min:

    def __init__(self, params):
        self.states = set(params['states'])
        self.transitions = {tuple(transition[:2]): transition[2] for transition in params['transitions']}
        self.start = params['start']
        self.final_states = set(params['final_states'])
        self.alphabet = set(symbol for x , symbol in self.transitions.keys() if symbol is not None)

    
    
    def minimize(self):
        def hopcroft():
            partitions = {frozenset(self.final_states), frozenset(self.states - self.final_states)}
            worklist = {frozenset(self.final_states), frozenset(self.states - self.final_states)}

            while worklist:
                A = worklist.pop()

                for c in self.alphabet:
                    X = set()
                    for from_state, symbol in self.transitions:
                        if symbol == c and self.transitions[(from_state, symbol)] in A:
                            X.add(from_state)

                    if X:
                        new_partitions = set()
                        for Y in list(partitions):
                            intersect = X.intersection(Y)
                            difference = Y - X
                            if intersect and difference:
                                #new_partitions.remove(Y)
                                new_partitions.add(frozenset(intersect))
                                new_partitions.add(frozenset(difference))
                                if Y in worklist:
                                    worklist.remove(Y)
                                #worklist.add(frozenset(intersect))
                                #worklist.add(frozenset(difference))
                                worklist.update([frozenset(intersect), frozenset(difference)])
                            else: 
                                new_partitions.add(Y)
                        partitions = new_partitions

            # Construir la nueva tabla de transiciones
            new_transitions = {}
            state_representatives = {}
            for state_set in partitions:
                representative = next(iter(state_set), None)
                if representative is None:  # Saltárselo en caso esté vacío
                    continue
                state_representatives[representative] = state_set
                for state in state_set:
                    for symbol in self.alphabet:
                        if (state, symbol) in self.transitions:
                            to_state = self.transitions[(state, symbol)]
                            for to_state_set in partitions:
                                if to_state in to_state_set:
                                    new_transitions[(representative, symbol)] = next(iter(to_state_set))
                                    break

            # Determinar los nuevos estados inicial y finales
            new_start_state = None
            new_final_states = set()
            for state_set in partitions:
                if not state_set:  # Check to prevent attempting to get a representative from an empty set
                    continue
                if self.start in state_set:
                    new_start_state = next(iter(state_set))
                if self.final_states.intersection(state_set):
                    new_final_states.add(next(iter(state_set)))


            return {
                'states': list(state_representatives.keys()),
                'transitions': new_transitions,
                'start': new_start_state,
                'final_states': list(new_final_states)
            }
        return hopcroft()
    

    def visualize(self):
        dot = Digraph()

        # Añadir estados
        for state in self.states:
            if state in self.final_states:
                # Marcar los estados finales 
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)

        # Marcar el estado inicial
        dot.node('', shape='none')  
        dot.edge('', self.start, label='start')

        # Añadir transiciones
        for (from_state, symbol), to_state in self.transitions.items():
            dot.edge(from_state, to_state, label=symbol)

        # Graficar 
        dot.render(format='pdf', view=True, cleanup=True)

        
    def isAcceptingMin(self, dfa_min, w):
        current_state = dfa_min['start']

        for character in w:
            next_state = None
            for (from_state, symbol), to_state in dfa_min['transitions'].items():
                if from_state == current_state and symbol == character:
                    next_state = to_state
                    break
        
        if next_state is None:
            return 'No'
        
        current_state = next_state

        return 'Sí' if current_state in dfa_min['final_states'] else 'No'
        


def buildUsingMinimization(dfa, w):
    dfa_min = DFA_min(dfa)
    minimized = dfa_min.minimize()
    print("DFA_min: " + dfa_min.isAcceptingMin(minimized,w))
    dfa_min.visualize()
    print(minimized)
    return minimized
