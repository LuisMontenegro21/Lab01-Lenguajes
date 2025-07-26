from Automata.DDFA import build_direct_dfa
from Automata.DFA import build_dfa
from Automata.NFABuilder import build_nfa
from Automata.MinDFA import build_min_dfa



def main() -> None:
    regex:str = input("Input regex: ")
    w:str = input("Input chain: ")
    
    build_direct_dfa(regex=regex, w=w, visualize=False)
    nfa = build_nfa(regex=regex, w=w)
    dfa = build_dfa(nfa=nfa, w=w, visualize=False) # fix Epsilon bug
    min_dfa = build_min_dfa(dfa=dfa, w=w, visualize=False)

    
if __name__ == "__main__":
    main()