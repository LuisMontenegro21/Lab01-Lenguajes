from collections import defaultdict
from Automata.Automaton import Automaton


class NFAState:
    # starts with 1
    count: int = 1  
    # holds lists of NFA states
    states:list['NFAState'] = []

    def __init__(self):
        # assign a unique number
        self.number: int = NFAState.count
        # start a dictionary to add transitions
        self.transitions:dict[str, list] = {}
        # set final state as false
        self.final: bool = False
        # increase count and append for each new state created
        NFAState.count += 1  
        NFAState.states.append(self)

    def add(self, character: str, state: 'NFAState'):
        if character not in self.transitions.keys():
            # create an empty list if the character is not in the transitions
            self.transitions[character] = []  
        # append the final state to the transitions given a character
        self.transitions[character].append(state)  



class NFA:
    start_state:int = 0
    final_states:list = []

    @staticmethod
    def create_character(character: str) -> 'NFA':
        '''
        Create a single character NFA 
        '''
        start = NFAState()  # create initial state
        end = NFAState()    # create final state
        start.add(character, end)  # connect final and initial states using char

        return NFA(start, end)  # return NFA

    def __init__(self, start:'NFA'=None, end:'NFA'=None) -> None:
        '''
        Builds a NFA
        '''
        self.stateS = start if start is not None else self.stateS = NFAState() # create a default state if not given
        self.stateE = end if end is not None else self.stateE = NFAState()  # create a default state if not given
        self.stateE.final = True  # Marcar el estado final como final

    def conection(self, nfaN: NFAState, character:str=None) -> None:
        '''Connect a NFA with another using character'''
        self.stateE.add(character, nfaN.stateS)  # Conectar el estado final de este AFN con el estado inicial del otro

    
    
    