from Automata.DDFA import build_direct_dfa
from Automata.DFA import build_dfa
from Automata.NFABuilder import build_nfa
from Automata.MinDFA import build_min_dfa
from Graph.Vizualizer import visualize_automaton


def main() -> None:
    regex:str = input("Input regex: ")
    w:str = input("Input chain: ")
    # build_direct_dfa(regex=regex, w=w)
    nfa = build_nfa(regex=regex, w=w)
    dfa = build_dfa(nfa=nfa, w=w)
    min_dfa = build_min_dfa(dfa=dfa, w=w)

    
if __name__ == "__main__":
    main()