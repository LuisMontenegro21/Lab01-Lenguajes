# Archivo Python que corre o emplea el algoritmo Thompson para generar un AFN (Automata Finito No-Determinista)

from graphviz import Digraph

class State:
    def __init__(self, label=None):
        self.transitions = {}
        self.epsilon_transitions = set()
        self.label = label
        self.is_accepting = False

# diccionario para definir la precedencia de las operaciones
precedence = {'|' : 1, '^' : 2, '*' : 3}

# verificar si el operador está definido o es válido
def isOperator(token):
    return token in "|*^"

# definir la presedencia de los operadores
def hasHigherPrecedence(op1, op2):
    return precedence[op1] > precedence[op2]

