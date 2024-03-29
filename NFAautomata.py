# Archivo para definir las clases para el AFN
from graphviz import Digraph



#----------------------------------------
# Clases del AFN
#----------------------------------------

# Clase para el estado del AFN
class NFAState:
    # Se inicia en 1
    count = 1  

    states = []

    def __init__(self):
        # Asignar un número único de estado basado en el contador
        self.number = NFAState.count
        # Inicializar un diccionario para almacenar las transiciones salientes
        self.changes = {}
        # Inicializar el estado como no final
        self.final = False
        # Incrementar el contador de estados para el próximo estado creado
        NFAState.count += 1  
        NFAState.states.append(self)


    def add(self, character, state):
        if character not in self.changes:
            # Crear una lista vacía si el carácter no está en las transiciones
            self.changes[character] = []  
        # Agregar el estado de destino a las transiciones con el carácter dado
        self.changes[character].append(state)  

    def get_alphabet(self):
        alphabet = [i for i in self.changes.keys() if i is not None]
        print(f"State {self.number} alphabet: {alphabet}")
        return alphabet


class NFA:
    start_state = 0
    final_state = []


    @staticmethod
    def getCharacter(character):
        # Crear un AFN con un solo carácter
        start = NFAState()  # Crear un estado inicial
        end = NFAState()    # Crear un estado final
        start.add(character, end)  # Conectar el estado inicial con el final usando el carácter

        return NFA(start, end)  # Devolver el AFN creado
    
    def getStates(self):
        return NFAState.states
    
    def getTransitions(self):
        num_states = NFAState.count  # Numero de estados
        transitions = []

        # Iterar para construir las transiciones
        for state in NFAState.states:
            state_name = str(state.number)
            for character, next_states in state.changes.items():
                for next_state in next_states:
                    next_state_name = str(next_state.number)
                    transitions.append([state_name, character, next_state_name])

        return transitions
    
    def setStartingState(self, state):
        self.start_state = state

    def setFinalState(self, state):
        if state not in self.final_state:
            self.final_state.append(state)

    def getStartingState(self):
        return self.start_state

    def getFinalState(self):
        return self.final_state

    def __init__(self, start=None, end=None):
        # Constructor de la clase Afn para crear un AFN
        if start:
            self.stateS = start
        else:
            self.stateS = NFAState()  # Crear un estado inicial por defecto si no se proporciona uno

        if end:
            self.stateE = end
        else:
            self.stateE = NFAState()  # Crear un estado final por defecto si no se proporciona uno
        self.stateE.final = True  # Marcar el estado final como final

    def conection(self, nfaN, character=None):
        # Conectar este AFN con otro AFN usando un carácter
        self.stateE.add(character, nfaN.stateS)  # Conectar el estado final de este AFN con el estado inicial del otro

    def diagram(self):
        # Visualizar el AFN usando graphviz
        dot = Digraph()
        NewS = [self.stateS]  # Lista de estados nuevos a explorar
        pastS = set()  # Conjunto de estados ya explorados

        while NewS:
            thisS = NewS.pop()  # Tomar un estado de la lista de estados nuevos
            for character, nextSs in thisS.changes.items():
                for nextS in nextSs:
                    # Agregar nodos al gráfico para estado inicial
                    if thisS == self.stateS:
                        dot.node(str(id(thisS)), label="Start", shape="circle")
                        self.setStartingState(thisS.number)
                    else:
                        dot.node(str(id(thisS)), label=str(thisS.number), shape="circle")
                    # Agregar nodo si el estado es final
                    if nextS.final and nextS == self.stateE:
                        dot.node(str(id(nextS)), label="Final", shape="doublecircle")
                        self.setFinalState(nextS.number)
                    else:
                        dot.node(str(id(nextS)), label=str(nextS.number), shape="circle")

                    # Agregar bordes al gráfico
                    if character:
                        dot.edge(str(id(thisS)), str(id(nextS)), label=character)
                    else:
                        dot.edge(str(id(thisS)), str(id(nextS)), label="ε")

                    if nextS not in pastS:
                        NewS.append(nextS)  # Agregar estados no explorados a la lista

            pastS.add(thisS)  # Marcar este estado como explorado
        # Devolver el gráfico del AFN
        return dot  
    
    def getNFAParams(self):
        num_states = NFAState.count  # Número de estados
        states = [str(i) for i in range(1, num_states + 1)]  # Lista de los identificadores de los estados
        alphabet_set = set()  # set de alfabeto

        transitions = []

        # Iterar para construir y obtener el alfabeto y transiciones
        for state in NFAState.states:
            state_name = str(state.number)
            for character, next_states in state.changes.items():
                
                for next_state in next_states:
                    transitions.append([state_name, character, str(next_state.number)])

                if character != 'ε' and character is not None:  
                    alphabet_set.add(character)
                

        alphabet = sorted(alphabet_set)  # Lista sorteada del alfabeto

        start = self.getStartingState()
        final_states = self.getFinalState()
        num_transitions = len(transitions)  # Número de transiciones

        # Retornar un diccionario
        return {
            #'num_states': num_states, #int
            'states': states, #str
            #'num_alphabet': len(alphabet), 
            'alphabet': alphabet + [None], #str
            'start': str(start), #str 
            #'num_final': len(final_states),
            'final_states': [str(i) for i in final_states], #str
            #'num_transitions': num_transitions,
            'transitions': transitions #str
        }





