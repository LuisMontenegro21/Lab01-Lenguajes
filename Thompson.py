# Archivo Python que corre o emplea el algoritmo Thompson para generar un AFN (Automata Finito No-Determinista)
from Automata import NFAState, NFA, infixToPostfix
from Root import *



# Función que implementa el algoritmo de Thompson para construir un AFN a partir de un árbol de expresión regular
def thompson(node):
    if not node.nextC:
        # Si el nodo es una hoja, crea un AFN con un carácter
        return NFA.getCharacter(node.value)  

    if node.value == "*":
        NFATemp = thompson(node.nextC[0])
        start = NFAState()
        end = NFAState()
        # Conexión con transición epsilon desde el nuevo estado inicial al inicio del sub-AFN
        start.add(None, NFATemp.stateS)
        # Conexión con transición epsilon desde el nuevo estado inicial al nuevo estado final
        start.add(None, end)
        # Conexión con transición epsilon desde el estado final del sub-AFN al inicio del sub-AFN
        NFATemp.stateE.add(None, NFATemp.stateS)
        # Conexión con transición epsilon desde el estado final del sub-AFN al nuevo estado final
        NFATemp.stateE.add(None, end)  

        return NFA(start, end)

    if node.value == "|":
        # Construir el AFN para la parte izquierda de la expresión
        nfaL = thompson(node.nextC[0])
        # Construir el AFN para la parte derecha de la expresión
        nfaR = thompson(node.nextC[1])
        start = NFAState()
        end = NFAState()
        # Conexión con transición epsilon desde el nuevo estado inicial al inicio del AFN izquierdo
        start.add(None, nfaL.stateS)
        # Conexión con transición epsilon desde el nuevo estado inicial al inicio del AFN derecho
        start.add(None, nfaR.stateS)
        # Conexión con transición epsilon desde el estado final del AFN izquierdo al nuevo estado final
        nfaL.stateE.add(None, end)
        # Conexión con transición epsilon desde el estado final del AFN derecho al nuevo estado final
        nfaR.stateE.add(None, end)

        return NFA(start, end)

    if node.value == ".":
        # Construir el AFN para la parte izquierda de la expresión
        nfaL = thompson(node.nextC[0])
        # Construir el AFN para la parte derecha de la expresión
        nfaR = thompson(node.nextC[1])
        # Conectar el estado final del AFN izquierdo con el estado inicial del AFN derecho
        nfaL.conection(nfaR)

        return NFA(nfaL.stateS, nfaR.stateE)
    
# Función para calcular el cierre epsilon de un conjunto de estados
def putEpsilon(states):
    # Inicializar una pila con los estados iniciales
    stack = list(states)
    # Crear un conjunto con los estados iniciales
    putEpsilon = set(states)

    while stack:
        # Tomar un estado de la pila
        state = stack.pop()
        if (None) in state.changes:
            # Si el estado tiene una transición epsilon (None), explorarlas
            for nextS in state.changes[None]:
                if nextS not in putEpsilon:
                    # Si el estado siguiente no está en el conjunto de cierre epsilon, agregarlo
                    putEpsilon.add(nextS)
                    # Agregar el estado siguiente a la pila para explorar sus transiciones epsilon
                    stack.append(nextS)
    # Devolver el conjunto resultante de estados con cierre epsilon
    return putEpsilon

# Función para simular un AFN en un input dado
def runNFA(nfa, afnValue):
    # Conjunto de estados actuales, inicializado con el estado inicial del AFN
    thisSs = set([nfa.stateS])  
    # Calcular cierre epsilon de los estados iniciales
    thisSs = putEpsilon(thisSs)  

    for character in afnValue:
        nextSs = set()
        for state in thisSs:
            if character in state.changes:
                for nextS in state.changes[character]:
                    nextSs.add(nextS)
        # Calcular cierre epsilon de los nuevos estados alcanzados
        nextSs = putEpsilon(nextSs)
        # Actualizar los estados actuales
        thisSs = nextSs  

    for state in thisSs:
        if state.final:
            # Si al menos uno de los estados actuales es final, la cadena es aceptada
            return True  
    # Si ninguno de los estados actuales es final, la cadena es rechazada
    return False  


def buildUsingThompson(regex):
    grapher = Grapher()
    postfix_regex = infixToPostfix(regex)
    root = grapher.build(postfix_regex)
    NFAState.count = 1
    nfa = thompson(root)
    visual_nfa = nfa.diagram()
    visual_nfa.render(f'AFN', view = True, cleanup=True)
