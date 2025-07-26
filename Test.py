from Algorithms.Postfix import expand_replace, infix_to_postfix, shunting_yard
from Automata.DDFA import build_direct_dfa


def main():
    regex:str = input("Input regex: ")
    print(infix_to_postfix(regex))
    print(shunting_yard(expression=['0', '.', '>=', '.', '1']))

    


if __name__ == '__main__':
    main()