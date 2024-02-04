# Para el empleo del método de construcción con subconjuntos
from DFAautomata import *

def buildUsingSubset(nfa):
    dfa = DFA(*nfa.toNFAParams())
    dfa.graphing(nfa)
    return dfa
    