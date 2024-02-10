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

    #TODO fix DFA_min 
    dfa_min = buildUsingMinimization(dfa, w)
    
    #TODO fix direct construct
    #dfa_dir = buildUsingDirectConstr(regex)

if __name__ == "__main__":
    main()