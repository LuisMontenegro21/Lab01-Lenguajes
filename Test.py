from Algorithms.Postfix import expand_replace, infix_to_postfix
from Automata.DDFA import build_direct_dfa 
from Automata.NFABuilder import build_nfa
from Automata.DFA import build_dfa
from Automata.MinDFA import build_min_dfa


def main():
    regex:str = input("Input regex: ")
    w:str = input(f"Ingrese una cadena para probar: ")
    # build_direct_dfa(regex=regex, w=w)
    nfa = build_nfa(regex=regex, w=w)
    dfa = build_dfa(nfa=nfa, w=w)
    min_dfa = build_min_dfa(dfa=dfa)

    


if __name__ == '__main__':
    main()