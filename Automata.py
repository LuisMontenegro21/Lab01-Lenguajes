# Archivo para definir las clases para los AFN y los AFD
from graphviz import Digraph
import re


# Funciones para volver el regex a postfix
# Para la presedencia de operadores
precedence = {'|': 1, '.': 2, '*': 3}

# define operadores definidos
def isOperator(token):
        return token in "|.*"

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
# Clases para la gráfica del autómata
#----------------------------------------
class Node:
    # Definición de los nodos del árbol

    def __init__(self, value):
        # El valor del nodo, que representa un carácter de la expresión regular
        self.value = value
        # Referencia al hijo izquierdo (si existe)
        self.left = None
        # Referencia al hijo derecho (si existe)
        self.right = None
        # Lista de nodos siguientes que están conectados con transiciones epsilon
        self.nextC = []

class Grapher(object):
    # Obtener Root
    def build(self, Regex):
        stack = []

        for character in Regex:
            if character not in "*.^":
                # Si el carácter no es un operador (*, | o .), crear un nuevo nodo para él y apilarlo
                newN = Node(character)
                stack.append(newN)

            else:
                if character == "*":
                    # Si es el operador de repetición (*)
                    if len(stack) >= 1:
                        print("Entra 1")
                        nodes = stack.pop()
                        newN = Node(character)
                        # Conectar el nodo de repetición al último nodo apilado
                        newN.nextC.append(nodes)  
                        stack.append(newN)
                    else:
                        raise Exception("Expresión inválida: Falta operando para *")

                else:
                    if character in "|.":
                        # Si es un operador OR (|) o concatenación (.)
                        if len(stack) >= 2:
                            print("Entra 2")
                            newN = Node(character)
                            rightNode = stack.pop()
                            leftNode = stack.pop()
                            # Conectar el nodo de operador al operando izquierdo
                            newN.nextC.append(leftNode)   
                            # Conectar el nodo de operador al operando derecho
                            newN.nextC.append(rightNode)  
                            stack.append(newN)
                        else:
                            raise Exception("Expresión inválida: Faltan operandos para | o .")
        

        if len(stack) == 1:
            # Si solo queda un nodo en la pila, es el árbol de expresión completo
            return stack[0]  
        else:
            # De lo contrario, la expresión es inválida
            return None  




#----------------------------------------
# Clases del AFN
#----------------------------------------

# Clase para el estado del AFN
class NFAState:
    # Se inicia en 1
    count = 1  

    def __init__(self):
        # Asignar un número único de estado basado en el contador
        self.number = NFAState.count
        # Inicializar un diccionario para almacenar las transiciones salientes
        self.changes = {}
        # Inicializar el estado como no final
        self.final = False
        # Incrementar el contador de estados para el próximo estado creado
        NFAState.count += 1  

    def add(self, character, state):
        if character not in self.changes:
            # Crear una lista vacía si el carácter no está en las transiciones
            self.changes[character] = []  
        # Agregar el estado de destino a las transiciones con el carácter dado
        self.changes[character].append(state)  


class NFA:
    @staticmethod
    def getCharacter(character):
        # Crear un AFN con un solo carácter
        start = NFAState()  # Crear un estado inicial
        end = NFAState()    # Crear un estado final
        start.add(character, end)  # Conectar el estado inicial con el final usando el carácter

        return NFA(start, end)  # Devolver el AFN creado

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
        # extrae los parametros de la clase
        num_states = NFAState.count  # numero de estados
        states = [str(i) for i in range(1, num_states + 1)]  # lista de los estados
        num_alphabet = len(self.stateS.get_alphabet())  # numero de alfabetos
        alphabet = list(self.stateS.get_alphabet())  # lista de alfabetos
        start = '1'  # estado inicial
        num_final = 1  # numero de estados finales
        final_states = [str(num_states)]  # lista de estados finales como string
        num_transitions = sum(len(s.changes) for s in NFAState.states)  # numero de transiciones
        transitions = []

        # Iterar para construir la tabla de transiciones
        for state in NFAState.states:
            state_name = str(state.number)
            for character, next_states in state.changes.items():
                for next_state in next_states:
                    next_state_name = str(next_state.number)
                    transitions.append([state_name, character, next_state_name])

        return num_states, states, num_alphabet, alphabet, start, num_final, final_states, num_transitions, transitions



#----------------------------------------
# Clases del AFD
#----------------------------------------
class DFAState:
    pass

class  DFA:
    pass