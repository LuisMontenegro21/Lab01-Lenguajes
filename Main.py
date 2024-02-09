#Archivo Python cuya función es concretar la ejecución del programa
from Thompson import buildUsingThompson
from Subset import buildUsingSubset
from DirectConst import buildUsingDirectConstr
from Miminization import buildUsingMinimization


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
    nfa = buildUsingThompson(regex,w)
    
    # Para graficar y testear el algoritmo de subconjuntos para AFD
    dfa = buildUsingSubset(nfa,w)

    dfa_min = buildUsingMinimization(dfa)
    
    #dfa_dir = buildUsingDirectConstr(w)

    # Para graficar y testear el AFD minimizado
    dfa_min = None 

if __name__ == "__main__":
    main()