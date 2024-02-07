# Para el empleo del método de construcción con subconjuntos
from DFAautomata import *

def buildUsingSubset(nfa):
    print(nfa.getNFAParams())
    dfa = DFA(nfa.getNFAParams())
    print(dfa.constructDFA())

    return dfa
    

def isAcceptedSubset(dfa):
    # modificar este pseudocodigo
    s = dfa.start
    c = nextChar()
    while (c not in dfa.final_states):
        s = move(s,c)
        c = nextChar()
