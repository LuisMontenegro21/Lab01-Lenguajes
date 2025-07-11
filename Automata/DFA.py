from Automata.NFA import NFA, NFAState
from Automata.Automaton import Automaton
from collections import defaultdict

class DFAState:
    __slots__ = ('id', 'final', 'transitions', 'label')
    def __init__(self, id: int, final:bool = False) -> None:
        self.id = id
        self.final = final
        self.transitions = defaultdict(set)
        self.label: str = f"q{id}"
    
    def add_transition(self, symbol: str, target: 'DFAState') -> None:
        self.transitions[symbol].add(target)

    def get_state_as_string(self) -> str:
        return f"State({self.id})"
    
class DFA(Automaton):
    # tomar los parametros para construir el DFA con el método de subconjuntos
    __slots__ = ('initial_state', 'states', 'transitions', 'final_states')

    def __init__(self):
        self.initial_state: int = 0
        self.states: set = set()
        self.transitions: dict[str, set[frozenset]] = {} # a dictionary mapping the character to the set of reachable states
        self.final_states: set = set()


    def epsilon_closure(self, state: set[NFAState]) -> set[NFAState]:
        '''
        Makes Epsilon Transition
        '''
        closure:set = set(state)
        stack:list = list(state)
        while stack:
            state = stack.pop()
            for next_state in state.transitions.get(None, []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure
 
    def move(self, states:set[NFAState], symbol: str) -> set[NFAState]:
        '''
        Checks which states are reachable from current one
        '''
        result = set()
        for state in states:
            for next_state in state.transitions.get(symbol, []):
                    result.add(next_state)
        return result


    def build(self, nfa: NFA) -> None:
        '''
        Builds a DFA from a NFA object
        '''
        initial_closure: set[NFAState] = self.epsilon_closure(state={nfa.stateS})
        unmarked_states:list[frozenset] = [frozenset(initial_closure)]
        dfa_states:list[frozenset] = [frozenset(initial_closure)]
        dfa_transitions: dict[str, set] = {}
        state_map: dict[frozenset, str] = {frozenset(initial_closure): 0}  # Mapear los frozensets a identificadores de strings
        state_count: int = 1
        states:set = set()

        while unmarked_states:
            current_frozenset: frozenset = unmarked_states.pop(0) # pop first state
            current_state: int = state_map[current_frozenset]

            for symbol in nfa.alphabet:
                if symbol is None:
                    continue
                # se mueve al siguiente estado si no es epsilon
                move_result: set = self.move(current_frozenset, symbol)
                if not move_result: # in case None, skip
                    continue
                
                # closure_result: frozenset = frozenset().union(*[self.epsilon_closure({s}) for s in move_result])
                closure_result = frozenset(self.epsilon_closure(move_result))
                # if not yet present on states, add it
                if closure_result not in dfa_states:
                    state_map[closure_result] = state_count
                    state_count += 1
                    dfa_states.append(closure_result)
                    unmarked_states.append(closure_result)

                # append transitions
                dfa_transitions.setdefault(current_state, set()).add((symbol, state_map[closure_result]))
  

        # se agrega los estados finales en los sets donde se hallen los estados de intersección de los finales del nfa y los estados del dfa
        nfa_final = nfa.stateE 
        final_states = [state_map[state] for state in dfa_states if nfa_final in state]
        self.states = list(state_map.values()) # change this
        self.transitions = dfa_transitions
        self.initial_state = 0 
        self.final_states = final_states
        
    
    def accepts(self, w:str) -> None:
        print(self.states)
        print(self.transitions)
        print(self.initial_state)
        print(self.final_states)
        current_state = initial_state
        for char in w:
            if char not in current_state.transitons:
                return False
            next_states = current_state.transitions[char]
            current_state = next(iter(next_states))
        
        return current_state.final
    

        

    def print_automata(self):
        pass
    
    def get_automata(self):
        return self
        
def build_dfa(nfa: NFA, w: str) -> None:
    dfa = DFA()
    dfa.build(nfa=nfa)
    dfa.accepts(w=w)

