from Algorithms.Postfix import expand_replace, infix_to_postfix
from Automata.DDFA import build_direct_dfa 
from Automata.NFABuilder import build_nfa


def main():
    regex:str = input("Input regex: ")
    #print(infix_to_postfix(regex))
    w:str = input(f"Ingrese una cadena para probar: ")
    build_direct_dfa(regex=regex, w=w)
    build_nfa(regex=regex, w=w)
    


if __name__ == '__main__':
    main()