# Para el empleo del método de construcción con subconjuntos
from DFAautomata import *

def buildUsingSubset(nfa):
    #print(*nfa.toNFAParams())
    dfa = DFA(*nfa.toNFAParams())
    dfa.subsetConstruction(nfa.toNFAParams())
    return dfa
    

def isAcceptedSubset(dfa):
    # modificar este pseudocodigo
    s = dfa.start
    c = nextChar()
    while (c not in dfa.final_states):
        s = move(s,c)
        c = nextChar()
