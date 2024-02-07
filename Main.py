#Archivo Python cuya función es concretar la ejecución del programa
from Thompson import buildUsingThompson, runNFA
from Subset import buildUsingSubset
from Miminization import DFA_min


def main():
    
    print("+---------------------------------+")
    print("+EXPRESIONES REGULARES A AUTÓMATAS+")
    print("+---------------------------------+")

    # Para los inputs
    print("\nIngrese la expresión regular: ")
    regex = str(input())  
    print("\nIngrese una cadena w: ")
    w = str(input())

    # Para graficar y testear el algoritmo de Thompson para AFN
    nfa = buildUsingThompson(regex)
    print("AFN-ε: " + str(runNFA(nfa, w)))

    # Para graficar y testear el algoritmo de subconjuntos para AFD
    dfa = buildUsingSubset(nfa)
    

    # Para graficar y testear el AFD minimizado 

if __name__ == "__main__":
    main()