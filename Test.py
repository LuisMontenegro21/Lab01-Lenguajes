from Algorithms.Postfix import infix_to_postfix
from Automata.DirectConst import DirectDFA, build_direct_dfa


def main():
    regex:str = input("Input regex: ")
    print(f"Original: {regex}")
    print(f"Postfix: {infix_to_postfix(regex)}")

    build_direct_dfa(regex=regex)



if __name__ == '__main__':
    main()