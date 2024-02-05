# Archivo para definir las clases para el AFN
from graphviz import Digraph


# Funciones para volver el regex a postfix
# Para la presedencia de operadores
precedence = {'|': 1, '.': 2, '*': 3, '+' : 3, '?' : 3}

# define operadores definidos
def isOperator(token):
        return token in "|.*+?"

#define la presedencia de los operadores
def hasHigherPrecedence(op1, op2):
        return precedence[op1] > precedence[op2]

#emplea el algo ritmo shunting yard
def shuntingYard(expression):
        output = []
        operator_stack = []

        # se recorre la expresión
        for token in expression:
            # si el token se encuentra 0-9 o a-z se manda a la cola
            if token.isalnum():  
                output.append(token)
            elif isOperator(token):
                while (operator_stack and isOperator(operator_stack[-1]) and hasHigherPrecedence(operator_stack[-1], token)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':  
                operator_stack.append(token)
            elif token == ')':  
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()

        while operator_stack:
            output.append(operator_stack.pop())

        return output

# convertir el la expression a postfix para el AFN
def infixToPostfix(expression):
    # reemplaza los espacios y ve los tokens o caracteres y los guarda en tokens
    expression = expression.replace(" ", "")
    tokens = [c for c in expression]

    # ejecuta el algoritmo shuntingYard y finalmente une la nueva expresión ya con los tokens en forma postfix
    postfix_tokens = shuntingYard(tokens)
    postfix_expression = "".join(postfix_tokens)
    
    return postfix_expression







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
                    # Agregar nodos al gráfico
                    if thisS == self.stateS:
                        dot.node(str(id(thisS)), label=f"Inicio", shape="circle")
                    else:
                        dot.node(str(id(thisS)), label=str(thisS.number), shape="circle")

                    if nextS.final and nextS == self.stateE:
                        dot.node(str(id(nextS)), label=f"Final", shape="doublecircle")
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
    
    def toNFAParams(self):
        num_states = NFAState.count  # Numero de estados
        states = [str(i) for i in range(1, num_states + 1)]  # Lista de estados
        alphabet_set = set()  # Set del alfabeto

        transitions = []

        # Iterar para construir las transiciones y tomar el alfabeto
        for state in NFAState.states:
            state_name = str(state.number)
            for character, next_states in state.changes.items():
                for next_state in next_states:
                    next_state_name = str(next_state.number)
                    transitions.append([state_name, character, next_state_name])

                    # Añadir los caracteres al alfabeto, exceptuando None (epsilom)
                    if character is not None:
                        alphabet_set.add(character)

        # Convertir el alfabeto a una lista sorteada
        alphabet = sorted(list(alphabet_set))

        start = '1'  # Estado inicial
        num_final = 1  # Numero de estados finales (arreglar para que puedan ser varios)
        final_states = [str(num_states)]  # Lista de estados finales como strings
        num_transitions = len(transitions)  # Numero de transiciones

        return num_states, states, len(alphabet), alphabet, start, num_final, final_states, num_transitions, transitions




