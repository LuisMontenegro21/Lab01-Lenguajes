# Para el empleo del método de construcción con subconjuntos
from DFAautomata import *

def buildUsingSubset(nfa, w):
    # para construir utilizando el subset y probarlo
    dfa = DFA(nfa.getNFAParams())
    construct = dfa.subsetConstr()
    dfa.visualize(construct)
    print("AFD-subconjunto: " + dfa.isAccepted(construct,w))
    return dfa
    


    
