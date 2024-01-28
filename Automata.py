# Archivo para definir las clases para los AFN y los AFD


#----------------------------------------
# Clases del AFN
#----------------------------------------
class NFAState:
    def __init__(self, label, is_accepting = False):
        self.label = label
        self.is_accepting = is_accepting
        self.transitions = {}


    def addTransition(self, symbol, target_state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
            self.transitions[symbol].append(target_state)
        
    
class NFA:
    
    def __init__(self, start_state = None, final_state = None):
        self.start_state = start_state
        self.final_state = final_state

    @staticmethod
    def basic(charr):
        start_state =  NFAState(label = 'start')
        final_state = NFAState(label = 'final', is_accepting=True)
        start_state.addTransition(charr, final_state)
        return NFA(start_state, final_state)
    
    @staticmethod
    def epsilon():
        start_state = NFAState(label = 'start')
        final_state = NFAState(label = 'final', is_accepting=True)
        start_state.addTransition('ε', final_state)
        return NFA(start_state, final_state)
    
    @staticmethod
    def concatenate(nfa1, nfa2):
        nfa1.final_state = NFAState(label = 'final', is_accepting=False)
        nfa1.final_state.addTransition('ε', nfa2.start_state)
        return NFA(nfa1.start_state, nfa2.end_state)
    
    @staticmethod
    def union(nfa1, nfa2):
        start_state = NFAState(label='start')
        final_state = NFAState(label='final', is_accepting=True)
        start_state.addTransition('ε', nfa1.start_state)
        start_state.addTransition('ε', nfa2.start_state)
        nfa1.final_state.addTransition('ε', final_state)
        nfa2.final_state.addTransition('ε', final_state)
        return NFA(start_state, final_state)
    
    @staticmethod
    def kleene(nfa):
        start_state = NFAState(label = 'start')
        final_state = NFAState(label = 'final', is_accepting=True)
        start_state.addTransition('ε', nfa.start_state)
        start_state.addTransition('ε', final_state)
        nfa.final_state.addTransition('ε', nfa.start_state)
        nfa.final_state.addTransition('ε', final_state)
        return NFA(start_state, final_state)
    
    def visualize(self):
        pass


#----------------------------------------
# Clases del AFD
#----------------------------------------
class DFAState:
    pass

class  DFA:
    pass