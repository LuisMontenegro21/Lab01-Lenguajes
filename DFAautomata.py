# Referencias: Compilers: Principles, Techniques, and Tools (Pearson Education, Inc) 1986

#----------------------------------------
# Clases del AFD
#----------------------------------------

# Archivo para la conversión del AFN a un AFD mediante construcción de subconjuntos
from graphviz import Digraph


class DFA:
    # tomar los parametros para construir el DFA con el método de subconjuntos
    def __init__(self, params):
        #self.num_states = params['num_states']
        self.nfa_states = params['states']
        #self.num_alphabet = params['num_alphabet']
        self.nfa_alphabet = params['alphabet']
        self.nfa_start = params['start']
        #self.num_final = params['num_final']
        self.nfa_final_states = params['final_states']
        #self.num_transitions = params['num_transitions']
        self.nfa_transitions = params['transitions']

    # para realizar la transición épsilon  
    def epsilonClosure(self, state, transitions):
        closure = {state}
        stack = [state]
        while stack:
            t = stack.pop()
            for from_state, symbol, to_state in transitions:
                if from_state == t and symbol == None and to_state not in closure:
                    closure.add(to_state)
                    stack.append(to_state)
        return closure
    
    # para encontrar a qué estados se puede acceder desde el estado actual 
    # empleado para la transición en el método de subconjuntos
    def move(self, states, symbol, transitions):
        result = set()
        for state in states:
            for from_state, input_symbol, to_state in transitions:
                if from_state in states and input_symbol == symbol:
                    result.add(to_state)
        return result

    # para la construccion del subset 
    def subsetConstr(self):
        # Se comienza con la cerradura inicial del estado inicial y las transiciones asociadas
        initial_closure = self.epsilonClosure(self.nfa_start, self.nfa_transitions)
        unmarked_states = [frozenset(initial_closure)]
        dfa_states = [initial_closure]
        dfa_transitions = []
        state_map = {frozenset(initial_closure): str(len(dfa_states))}  # Mapear los frozensets a identificadores de strings

        while unmarked_states:
            current_frozenset = unmarked_states.pop(0)  # Se va chequeando en fila para mantener orden
            current_state = state_map[current_frozenset]

            for symbol in filter(lambda x: x is not None, self.nfa_alphabet):  # Se excluye lo que es epsilon
                move_result = self.move(current_frozenset, symbol, self.nfa_transitions)
                if not move_result:
                    continue
                # se da un resultado de la cerradura para cada recorrido
                closure_result = frozenset().union(*[self.epsilonClosure(s, self.nfa_transitions) for s in move_result])
                
                # si el resultado de la cerradura aún no está en los estados del AFN, se agrega
                if closure_result not in dfa_states:
                    dfa_states.append(closure_result)
                    unmarked_states.append(closure_result)
                    state_map[closure_result] = str(len(dfa_states))  # NNuevo identificador de estado

                # se asigna que el estado de donde viene es el actual
                from_state = current_state
                # se asigna al estado al que va el resultado de la cerradura épsilon mapeada
                to_state = state_map[closure_result]
                # se agrega las transiciones con el formado ['from', 'symbol', 'to_state'], de donde viene y el símbolo con el que va al siguiente
                dfa_transitions.append([from_state, symbol, to_state])

        # se agrega los estados finales en los sets donde se hallen los estados de intersección de los finales del nfa y los estados del dfa
        final_states = [state_map[frozenset(state)] for state in dfa_states if set(state).intersection(set(self.nfa_final_states))]

        return {
            'states': [state_map[frozenset(state)] for state in dfa_states],
            'transitions': dfa_transitions,
            'start': state_map[frozenset(initial_closure)],
            'final_states': final_states
        }
    
    def isAccepted(self, dfa, string):

        # Empezar en el estado inicial
        current_state = dfa['start']
        
        # Definir una función para moverse al siguiente estado dependiendo del caracter 
        def move(current_state, character):
            for transition in dfa['transitions']:
                if transition[0] == current_state and transition[1] == character:
                    return transition[2]
            return None  # Return None if there is no valid transition
        
        # Iterar sobre los caracteres de la cadena
        for character in string:
            next_state = move(current_state, character)
            if next_state is None:
                return "No"  # Si no existe una transición válida a un siguiente estado, retornar que no
            current_state = next_state
        
        # Chequear si al final el estado en el que estamos es de aceptación (final)
        if current_state in dfa['final_states']:
            return "Sí"
        else:
            return "No"

    # para visualizar el AFD
    def visualize(self, dfa):
        dot = Digraph()
        
        # Añadir estados
        for state in dfa['states']:
            if state in dfa['final_states']:
                # Marcar los estados finales con un circulo doble
                dot.node(state, state, shape='doublecircle')
            else:
                dot.node(state, state)
        
        # Darle nombre a los estados
        dot.node('', label = '' , shape='none')
        dot.edge('', dfa['start'])
        
        # Add transitions
        for from_state, symbol, to_state in dfa['transitions']:
            dot.edge(from_state, to_state, label=symbol)
        
        # renderizar
        dot.render('dfa.pdf', view=True, cleanup=True)

        



        


