#----------------------------------------
# Clases para la gráfica del autómata
#----------------------------------------
class Node:
    # Definición de los nodos del árbol

    def __init__(self, value):
        # El valor del nodo, que representa un carácter de la expresión regular
        self.value = value
        # Referencia al hijo izquierdo (si existe)
        self.left = None
        # Referencia al hijo derecho (si existe)
        self.right = None
        # Lista de nodos siguientes que están conectados con transiciones epsilon
        self.nextC = []

class Grapher(object):
    # Obtener Root
    def build(self, Regex):
        stack = []

        for character in Regex:
            if character not in "*.^":
                # Si el carácter no es un operador (*, | o .), crear un nuevo nodo para él y apilarlo
                newN = Node(character)
                stack.append(newN)

            else:
                if character == "*":
                    # Si es el operador de repetición (*)
                    if len(stack) >= 1:
                        
                        nodes = stack.pop()
                        newN = Node(character)
                        # Conectar el nodo de repetición al último nodo apilado
                        newN.nextC.append(nodes)  
                        stack.append(newN)
                    else:
                        raise Exception("Expresión inválida: Falta operando para *")

                else:
                    if character in "|.":
                        # Si es un operador OR (|) o concatenación (.)
                        if len(stack) >= 2:
                            
                            newN = Node(character)
                            rightNode = stack.pop()
                            leftNode = stack.pop()
                            # Conectar el nodo de operador al operando izquierdo
                            newN.nextC.append(leftNode)   
                            # Conectar el nodo de operador al operando derecho
                            newN.nextC.append(rightNode)  
                            stack.append(newN)
                        else:
                            raise Exception("Expresión inválida: Faltan operandos para | o .")
        

        if len(stack) == 1:
            # Si solo queda un nodo en la pila, es el árbol de expresión completo
            return stack[0]  
        else:
            # De lo contrario, la expresión es inválida
            return None  
        
