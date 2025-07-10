
class NFAState:
    '''
    Assigns a NFAState to create small NFA
    '''
    _count: int = 1 
    def __init__(self):
        # assign a unique number
        self.number: int = NFAState._count
        # start a dictionary to add transitions
        self.transitions:dict[str, list[NFAState]] = {}
        # set final state as false
        self.final: bool = False
        # increase count 
        NFAState._count += 1  
        

    def add(self, character: str, state: 'NFAState'):
        # append the final state to the transitions given a character
        self.transitions.setdefault(character, []).append(state)  



class NFA:
    start_state:int = 0
    final_states:set = set()
    alphabet:set = set()

    @staticmethod
    def create_character(character: str) -> 'NFA':
        '''
        Create a single character NFA 
        '''
        start = NFAState()  # create initial state
        end = NFAState()    # create final state
        start.add(character, end)  # connect final and initial states using char

        return NFA(start, end)  # return NFA

    def __init__(self, start:NFAState=None, end:NFAState=None) -> None:
        '''
        Builds a NFA
        '''
        self.stateS = start or NFAState() # create a default state if not given
        self.stateE = end or NFAState()  # create a default state if not given
        self.stateE.final = True  # mark final state 
        self.final_states.add(self.stateE) # add to final states

    def connect(self, nfaN: 'NFA', character:str=None) -> None:
        '''Connect a NFA with another using character'''
        self.stateE.add(character, nfaN.stateS)  # Conectar el estado final de este AFN con el estado inicial del otro
    

    
    
    