#Archivo Python cuya función es concretar la ejecución del programa

from Subset import NFAtoDFASubset
from DirectConst import NFAtoDFADirect
from Miminization import minimizeDFA

def main():
    print("+---------------------------------+")
    print("+EXPRESIONES REGULARES A AUTÓMATAS+")
    print("+---------------------------------+")
    print("\nIngrese la expresión regular: ")

    regex = str(input())    

    # convertir el regex a un AFN con Thompson
    nfa = regexToNFA(regex)

    # convertir el AFN a un AFD con subset
    dfa_subset = NFAtoDFASubset(nfa)

    # convertir el AFN a un AFD con const direct
    dfa_direct = NFAtoDFADirect(nfa)

    # minimizar el AFD 
    dfa_min = minimizeDFA(dfa_subset)

    print("\nIngrese la cadena w: ")
    w = str(input())
 

if __name__ == "__main__":
    main()