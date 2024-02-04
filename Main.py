#Archivo Python cuya función es concretar la ejecución del programa
from Thompson import buildUsingThompson, runNFA


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
    print("AFN: " + str(runNFA(nfa, w)))

    # Para graficar y testear el algoritmo de subconjuntos para AFD
    


if __name__ == "__main__":
    main()