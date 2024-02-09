# archivo dedicado a la construcción directa del autómata

class Node:
    # clase para definir los nodos
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right    



    def __repr__(self):
        return '<Node {}>'.format(self.value)


class Direct:

    def __init__(self, regex):
        self.regex = regex
        self.index = 0

    # para ir avanzando sobre la cadena uno por uno para recuperar los caracteres que va leyendo
    def nextToken(self):
        if self.index < len(self.regex):
            token = self.regex[self.index]
            self.index += 1
            return token
        return None
    
    # Para manejar los operadores de misma precedencia +*?
    def handleOperator(self, node, operator):
        if operator == '*':
            return Node('*', node)
        elif operator == '+': 
            # por equivalencia r+ = r.r*
            return Node('.', node, Node('*', node))
        elif operator == '?':
            # por equivalencia r? = r|ε
            return Node('|', node, Node('ε'))
        
        return node
    # método para representar * + ? (ya que tienen precedencia equivalente)
    def parseFactor(self):
        token = self.nextToken()
        if token == '(':
            node = self.parseExpression()
            self.index += 1 
            if self.index < len(self.regex) and self.regex[self.index] in ('*', '+', '?'):
                operator = self.nextToken()
                node = self.handleOperator(node, operator)
            return node
        elif token and token != ')':
            if self.index < len(self.regex) and self.regex[self.index] in ('*', '+', '?'):
                operator = self.nextToken()
                return self.handleOperator(Node(token), operator)
            return Node(token)
        return None
    
    # empleado para representar la concatenación
    def parseTerm(self):
        node = self.parseFactor()
        while self.index < len(self.regex) and self.regex[self.index] not in ('|', ')'):
            next_node = self.parseFactor()
            node = Node('.', node, next_node) if node else next_node
        return node

    # empleado para manejar las operaciones de alternación '|'
    def parseExpression(self):
        nodes = [self.parseTerm()]
        while self.index < len(self.regex) and self.regex[self.index] == '|':
            self.index += 1  
            nodes.append(self.parseTerm())
        
        if len(nodes) > 1:
            root = nodes[0]
            for node in nodes[1:]:
                root = Node('|', root, node)
            return root
        return nodes[0]

    # para construir el syntax tree 
    def syntaxTree(self):
        return self.parseExpression()



def buildUsingDirectConstr(w):
    dfa = Direct(w)
    syntax = dfa.syntaxTree()
    print(syntax)