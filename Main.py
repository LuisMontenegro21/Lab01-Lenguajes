#Archivo Python cuya función es concretar la ejecución del programa
from Thompson import buildUsingThompson, runNFA


def main():
    print("+---------------------------------+")
    print("+EXPRESIONES REGULARES A AUTÓMATAS+")
    print("+---------------------------------+")


    print("\nIngrese la expresión regular: ")
    regex = str(input())  
    nfa = buildUsingThompson(regex)
    print("\nIngrese una cadena w: ")
    w = str(input())
    #print(runNFA(nfa, w))
if __name__ == "__main__":
    main()