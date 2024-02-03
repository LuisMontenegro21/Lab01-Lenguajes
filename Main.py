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
    print("\nIngrese una cadena w: ")
    w = str(input())
    # convertir el regex a un AFN con Thompson
    buildUsingThompson(regex)



    if runNFA(w):
        print("Cadena aceptada")
    else:
        print("Cadena rechazada")

    


    print("\nIngrese la cadena w: ")
    w = str(input())
 

if __name__ == "__main__":
    main()