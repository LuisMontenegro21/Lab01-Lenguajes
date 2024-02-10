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
            # se divide en dos sets, uno con los estados finales y el otro con los estados no finales
            partitions = {frozenset(self.final_states), frozenset(self.states - self.final_states)}
            # con este se va a trabajar
            worklist = list(partitions.copy())

            # vamos examinando los estados en conjunto
            while worklist:
                A = worklist.pop(0)

                # Para cada símbolo del alfabeto, se crea un conjunto X que tiene todas las transiciones con el símbolo c
                # En resumen, X es el conjunto de estados con los que se puede llegar a A con c
                for c in self.alphabet:
                    X = set()
                    for from_state, symbol in self.transitions:
                        if symbol == c and self.transitions[(from_state, symbol)] in A:
                            X.add(from_state)
                    # si X no está vacío se itera sobre la copia de las particiones
                    if X:
                        for Y in partitions.copy():
                            # para cada partición se calcula la intersección 
                            intersect = X.intersection(Y)
                            difference = Y - X
                             # si ambos no están vacíos se reemplaza Y por dos nuevas particiones
                            if intersect and difference:
                                partitions.remove(Y)
                                partitions.add(frozenset(intersect))
                                partitions.add(frozenset(difference))
                                # si Y está en el worklist se quita
                                if Y in worklist:
                                    worklist.remove(Y)
                                # se agregan las particiones hechas 
                                worklist.extend([frozenset(intersect), frozenset(difference)])
                           

            # Construir la nueva tabla de transiciones
            new_transitions = {}
            # se mapea cada estado a su partición 
            state_representatives = {next(iter(state_set), None): state_set for state_set in partitions}
            # Iterar sobre las transiciones originales para así construir las nuevas
            for from_state, symbol in self.transitions:
                for representative, partition in state_representatives.items():
                    # si el estado que viene está en la partición
                    if from_state in partition:
                        # el estado al que va se le asigna el estado de donde viene con el símbolo
                        to_state = self.transitions[(from_state, symbol)]
                        # se mapea el estado 
                        to_state_rep = next((rep for rep, part in state_representatives.items() if to_state in part), None)
                        # se chequea si no es none
                        if to_state_rep is not None:
                            new_transitions[(representative, symbol)] = to_state_rep
                        break

            # Determinar los nuevos estados inicial y finales
            new_start_state = next((rep for rep, part in state_representatives.items() if self.start in part), None)
            new_final_states = {rep for rep, part in state_representatives.items() if part.intersection(self.final_states)}
            


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
        # se itera para cada transición 
        for character in w:
            next_state = dfa_min['transitions'].get((current_state, character))
            
            # si el siguiente estado es None, no es aceptado
            if next_state is None:
                return 'No'
        
            current_state = next_state
        # si el estado final al que se llega es aceptado
        return 'Sí' if current_state in dfa_min['final_states'] else 'No'
        


def buildUsingMinimization(dfa, w):
    dfa_min = DFA_min(dfa)
    minimized = dfa_min.minimize()
    print("AFD-min: " + dfa_min.isAcceptingMin(minimized,w))
    dfa_min.visualize()
    #print(minimized)
    return minimized
