# Archivo Python que corre o emplea el algoritmo Thompson para generar un AFN (Automata Finito No-Determinista)
from Automata.NFA import NFAState, NFA
from Automata.Automaton import PNode, Automaton


class LitNode(PNode):
    __slots__ = PNode.__slots__ + ('value')
    def __init__(self, value: str):
        self.value = value
    
    def as_string(self) -> str:
        return self.value

class ConcatNode(PNode):
    __slots__ = PNode.__slots__ + ('left', 'right')
    def __init__(self, left:PNode, right:PNode):
        self.left = left
        self.right = right
    
    def as_string(self) -> str:
        return f"({self.left.as_string()}.{self.right.as_string()})"

class UniNode(PNode):
    __slots__ = PNode.__slots__ + ('left', 'right')
    def __init__(self, left:PNode, right:PNode):
        self.left = left
        self.right = right
    
    def as_string(self) -> str:
        return f"({self.left.as_string()}|{self.right.as_string()})"

class StarNode(PNode):
    __slots__ = PNode.__slots__ + ('child')
    def __init__(self, child:PNode):
        self.child = child
    
    def as_string(self) -> str:
        return f"({self.child.as_string()})*"
    
class PlusNode(PNode):
    __slots__ = PNode.__slots__ + ('child')
    def __init__(self, child:PNode):
        self.child = child
    
    def as_string(self):
        return f"({self.child.as_string()})"

class OptiNode(PNode):
    __slots__ = PNode.__slots__ + ('child')
    def __init__(self, child:PNode):
        self.child = child
    
    def as_string(self):
        return f"({self.child.as_string()})"


class NFABuilder(Automaton):

    def __init__(self):
        self.nfa: NFA = None
    

    def thompson(self, node: PNode) -> NFA:
        '''Implement Thomson's algorithm '''
        if isinstance(node, LitNode):
            return NFA.create_character(node.value)  
        
        if isinstance(node, ConcatNode):
            nfaL = self.thompson(node.left)
            nfaR = self.thompson(node.right)
            nfaL.conection(nfaR)
            return NFA(nfaL.stateS, nfaR.stateE)
        
        if isinstance(node, UniNode):
            nfaL = self.thompson(node.left)
            nfaR = self.thompson(node.right)
            start = NFAState()
            end = NFAState()
            start.add(None, nfaL.stateS)
            start.add(None, nfaR.stateS)
            nfaL.stateE.add(None, end)
            nfaR.stateE.add(None, end)
            return NFA(start, end)

        if isinstance(node, StarNode):
            nfaExp: NFA = self.thompson(node.child)
            start = NFAState()
            end = NFAState()
            start.add(None, nfaExp.stateS)
            start.add(None, end)
            nfaExp.stateE.add(None, nfaExp.stateS)
            nfaExp.stateE.add(None, end)  
            return NFA(start, end)
            
        if isinstance(node, PlusNode):
            nfaExpr = self.thompson(node.child)
            start = NFAState()
            end = NFAState()
            start.add(None, nfaExpr.stateS)
            nfaExpr.stateE.add(None, nfaExpr.stateS)
            nfaExpr.stateE.add(None, end)
            return NFA(start, end)
        
        if isinstance(node, OptiNode):
            nfaExpr = self.thompson(node.child)
            start = NFAState()
            end = NFAState()
            start.add(None, nfaExpr.stateS)
            nfaExpr.stateE.add(None, end)
            start.add(None, end)
            return NFA(start, end)

    def accepts(self, afnValue) -> bool:
        # Conjunto de estados actuales, inicializado con el estado inicial del AFN
        thisSs = set([self.nfa.stateS])  
        # Calcular cierre epsilon de los estados iniciales
        thisSs = self.put_epsilon(thisSs)  

        for character in afnValue:
            nextSs = set()
            for state in thisSs:
                if character in state.transitions:
                    for nextS in state.transitions[character]:
                        nextSs.add(nextS)
            # Calcular cierre epsilon de los nuevos estados alcanzados
            nextSs = self.put_epsilon(nextSs)
            # Actualizar los estados actuales
            thisSs = nextSs  

        for state in thisSs:
            return state.final
    

    def put_epsilon(self, states):
        # Inicializar una pila con los estados iniciales
        stack: list[NFAState] = list(states)
        # Crear un conjunto con los estados iniciales
        putEpsilon = set(states)

        while stack:
            # Tomar un estado de la pila
            state: NFAState = stack.pop()
            if (None) in state.transitions:
                # Si el estado tiene una transición epsilon (None), explorarlas
                for nextS in state.transitions[None]:
                    if nextS not in putEpsilon:
                        # Si el estado siguiente no está en el conjunto de cierre epsilon, agregarlo
                        putEpsilon.add(nextS)
                        # Agregar el estado siguiente a la pila para explorar sus transiciones epsilon
                        stack.append(nextS)
        # Devolver el conjunto resultante de estados con cierre epsilon
        return putEpsilon

    def build(self, root:PNode):
        return self.thompson(root)
    
    def print_automata(self):
        pass
    
    def get_automata(self) -> NFA:
        return self.nfa


# para construir utilizando thompson
def buildUsingThompson(regex: str, w:str):

    raise NotImplementedError()