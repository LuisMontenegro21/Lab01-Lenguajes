# Archivo Python que corre o emplea el algoritmo Thompson para generar un AFN (Automata Finito No-Determinista)
from Automata.NFA import NFAState, NFA
from Automata.Automaton import Automaton
from Automata.Nodes import PNode, LitNode, BinaryNode, UnaryNode
from Algorithms.Tree import build_syntax_tree

EPSILON = None # defines Epsilon

class NFABuilder(Automaton):

    def __init__(self):
        self.nfa: NFA = NFA() # holds final dfa
        
    
    def thompson(self, node: PNode) -> NFA:
        '''Implement Thomson's algorithm '''

        if isinstance(node, LitNode):
            self.nfa.alphabet.add(node.value)
            return NFA.create_character(node.value)  
        
        elif isinstance(node, BinaryNode) and node.operator == '.':
            nfaL = self.thompson(node.left)
            nfaR = self.thompson(node.right)
            nfaL.connect(nfaR)
            return NFA(nfaL.stateS, nfaR.stateE)
        
        elif isinstance(node, BinaryNode) and node.operator == '|':
            nfaL = self.thompson(node.left)
            nfaR = self.thompson(node.right)
            start = NFAState()
            end = NFAState()
            start.add(EPSILON, nfaL.stateS)
            start.add(EPSILON, nfaR.stateS)
            nfaL.stateE.add(EPSILON, end)
            nfaR.stateE.add(EPSILON, end)
            return NFA(start, end)

        elif isinstance(node, UnaryNode) and node.operator == '*':
            nfaExp: NFA = self.thompson(node.child)
            start = NFAState()
            end = NFAState()
            start.add(EPSILON, nfaExp.stateS)
            start.add(EPSILON, end)
            nfaExp.stateE.add(EPSILON, nfaExp.stateS)
            nfaExp.stateE.add(EPSILON, end)  
            return NFA(start, end)
            

        elif isinstance(node, UnaryNode) and node.operator == '+':
            nfaExpr = self.thompson(node.child)
            start = NFAState()
            end = NFAState()
            start.add(EPSILON, nfaExpr.stateS)
            nfaExpr.stateE.add(EPSILON, nfaExpr.stateS)
            nfaExpr.stateE.add(EPSILON, end)
            return NFA(start, end)
        
        elif isinstance(node, UnaryNode) and node.operator == '?':
            nfaExpr = self.thompson(node.child)
            start = NFAState()
            end = NFAState()
            start.add(EPSILON, nfaExpr.stateS)
            nfaExpr.stateE.add(EPSILON, end)
            start.add(EPSILON, end)
            return NFA(start, end)
        else:
            raise TypeError(f"Unknown type: {type(node).__name__}")

    def epsilon_closure(self, states: set['NFAState']) -> set['NFAState']:
        '''
        Computes epsilon closure for a set of states. 
        '''
        stack = list(states)
        closure = set(states)
        while stack:
            state: NFAState = stack.pop()
            for next_state in state.transitions.get(None, []): # None is epsilon in this case
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def move(self, states: set['NFAState'], symbol:str) -> set['NFAState']:
        '''
        Get reachable states given a symbol
        '''
        result = set()
        for state in states:
            for next_state in state.transitions.get(symbol, []):
                result.add(next_state)
        return result


    def accepts(self, w: str) -> bool:
        '''
        Checks if a string is accepted or not by the NFA
        '''
        # starts with closure of the first states
        current_states: set[NFAState] = self.epsilon_closure(states={self.nfa.stateS}) 
        # checks symbol for symbol if there is a transition for it
        for symbol in w:
            next_states: set[NFAState] = self.move(current_states, symbol)
            current_states: set[NFAState] = self.epsilon_closure(next_states)
        # check if any of the current_states yields a final state
        return any(state.final for state in current_states)


    def build(self, regex:str):
        root: PNode = build_syntax_tree(regex=regex) # build a tree and get the root
        self.nfa = self.thompson(node=root) # TODO check this assignment if it is not giving overhead 
        # print(f"Alphabet: {self.nfa.alphabet}")
    
    
    def print_automaton(self):
        print(f"Final states: {self.nfa.final_states}")
        print(f"Starting state: {self.nfa.start_state}")
        print(f"Alphabet: {self.nfa.alphabet}")

    def get_automaton(self) -> NFA:
        return self.nfa




# para construir utilizando thompson
def build_nfa(regex: str, w:str) -> NFA:
    nfa_builder = NFABuilder()
    nfa_builder.build(regex=regex)
    print(nfa_builder.accepts(w=w)) 
    return nfa_builder.get_automaton()