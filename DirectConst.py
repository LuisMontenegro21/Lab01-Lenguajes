# archivo dedicado a la construcción directa del autómata
from Postfix import shuntingYard

class Node:
    # clase para definir los nodos del arbol 
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right    
        # propiedades para firstpos, nullable, lastpos
        self.nullable = False
        self.firstpost = set()
        self.lastpost = set()
        self.position = 0


class Direct:

    def __init__(self, regex):
        self.regex = regex
        self.node_counter = 0
        self.precedence = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3}

    # para construir el arbol sintactico
    def buildSyntaxTree(self):
        # Utilizar el algoritmo shunting yard para volverlo postfix
        postfix = shuntingYard(self.regex)
        stack = []
        for char in postfix:
            # verificar si el caracter es [a-z] , [0-9]
            if char.isalnum():
                stack.append(Node(char))
            else:
                # si el caracter tiene precedencia 3
                if char in {'*', '+', '?'}:
                    operand = stack.pop()
                    node = Node(char, operand)
                else:
                    right = stack.pop()
                    left = stack.pop()
                    node = Node(char, left, right)
                stack.append(node)
        return stack.pop()

    # volver el arbol sintactico a un diccionario 
    def syntaxTreeToDict(self, node = None):
        if node is None:
            node = self.buildSyntaxTree()
        tree_dict = {"value": node.value}
        if node.left:
            tree_dict['left'] = self.syntaxTreeToDict(node.left)
        if node.right:
            tree_dict['right'] = self.syntaxTreeToDict(node.right)
        
        return tree_dict
    
    def computeNullable(self, node):
        # Computar si es nullable el nodo
        if node['value'] in ['*', '?', 'ε']:  # Kleene star, ?  y epsilon siempre son nullable
            return True
        elif node['value'] == '|':
            return self.computeNullable(node['left']) or self.computeNullable(node['right'])
        elif node['value'] == '.':
            return self.computeNullable(node['left']) and self.computeNullable(node['right'])
        else:  
            return False  # No es nullable a menos que sea épsilon

    def computeFirstpos(self, node):
        # Computa los firstpos de cada nodo
        if 'position' in node:  
            return {node['position']}
        elif node['value'] == '|':
            return self.computeFirstpos(node['left']) | self.computeFirstpos(node['right'])
        elif node['value'] == '.':
            if self.computeNullable(node['left']):
                return self.computeFirstpos(node['left']) | self.computeFirstpos(node['right'])
            else:
                return self.computeFirstpos(node['left'])
        elif node['value'] == '*':
            return self.computeFirstpos(node['left'])
        else:  # Otros operadores
            return set()

    def computeLastpos(self, node):
        # Computa el lastpos de cada hoja
        if 'position' in node:  
            return {node['position']}
        elif node['value'] == '|':
            return self.computeLastpos(node['left']) | self.computeLastpos(node['right'])
        elif node['value'] == '.':
            if self.computeNullable(node['right']):
                return self.computeLastpos(node['left']) | self.computeLastpos(node['right'])
            else:
                return self.computeLastpos(node['right'])
        elif node['value'] == '*':
            return self.computeLastpos(node['left'])
        else:  # Otros casos de operadores 
            return set()

    def enhance(self, node):

        if node is not None:
            node['nullable'] = self.computeNullable(node)
            if 'left' in node:
                self.enhance(node['left'])
            if 'right' in node:
                self.enhance(node['right'])
            node['firstpos'] = self.computeFirstpos(node)
            node['lastpos'] = self.computeLastpos(node)


def buildUsingDirectConstr(w):
    dfa = Direct(w)
    syntax = dfa.syntaxTreeToDict()
    dfa.enhance(syntax)
    #print(dfa.computeNullable(syntax))
    #print(dfa.computeFirstpos(syntax))
    #print(dfa.computeLastpos(syntax))
    #print(syntax)