# Archivo Python que corre o emplea el algoritmo Thompson para generar un AFN (Automata Finito No-Determinista)
from graphviz import Digraph
from Automata import NFA
import re 


def regexToNFA(regex):
    stack = []
    for symbol in regex:
        if symbol.isalpha():
            stack.append(NFA.basic(symbol))
        elif symbol == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(NFA.union(nfa1, nfa2))
        elif symbol == '*':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(NFA.concatenate(nfa1,nfa2))
    
    return stack.pop()

def isAcceptingNFA(w):
    pass
