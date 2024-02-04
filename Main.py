#Archivo Python cuya función es concretar la ejecución del programa
from Thompson import buildUsingThompson


def main():
    print("+---------------------------------+")
    print("+EXPRESIONES REGULARES A AUTÓMATAS+")
    print("+---------------------------------+")


    print("\nIngrese la expresión regular: ")
    regex = str(input())  

    print("\nIngrese una cadena w: ")
    w = str(input())

if __name__ == "__main__":
    main()