#Archivo Python cuya función es concretar la ejecución del programa
from Automata.Thompson import buildUsingThompson
from Automata.DirectConst import build_direct_dfa



def main() -> None:
    
    print("+---------------------------------+")
    print("+EXPRESIONES REGULARES A AUTÓMATAS+")
    print("+---------------------------------+")

    # Para los inputs
    print("\nIngrese la expresión regular: ")
    regex:str = str(input())  
    print("\nIngrese una cadena w: ")
    w:str = str(input())

    # Para graficar y testear el algoritmo de Thompson para AFN
    #nfa = buildUsingThompson(regex,w)
    
    # Para graficar y testear el algoritmo de subconjuntos para AFD
    #dfa = buildUsingSubset(nfa,w)

    #TODO fix DFA_min 
    #dfa_min = buildUsingMinimization(dfa, w)
    
    #TODO fix direct construct
    dfa_dir = build_direct_dfa(regex)

if __name__ == "__main__":
    main()