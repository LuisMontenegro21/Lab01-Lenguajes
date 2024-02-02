#Archivo Python cuya función es concretar la ejecución del programa
from Thompson import buildUsingThompson, runNFA
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
    nfa = buildUsingThompson(regex)
    print("\nIngrese una cadena w: ")
    w = str(input())

    result = runNFA(nfa, w)


    print("\nIngrese la cadena w: ")
    w = str(input())
 

if __name__ == "__main__":
    main()