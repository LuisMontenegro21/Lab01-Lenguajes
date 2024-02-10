# Funciones para volver el regex a postfix
# Para la presedencia de operadores
precedence = {'|': 1, '.': 2, '*': 3, '+' : 3, '?' : 3}

# define operadores definidos
def isOperator(token):
        return token in "|.*+?"

#define la presedencia de los operadores
def hasHigherPrecedence(op1, op2):
        return precedence[op1] > precedence[op2]

#emplea el algo ritmo shunting yard
def shuntingYard(expression):
        output = []
        operator_stack = []

        # se recorre la expresión
        for token in expression:
            # si el token se encuentra 0-9 o a-z se manda a la cola (no se considera otros símbolos)
            if token.isalnum():  
                output.append(token)
            elif isOperator(token):
                while (operator_stack and isOperator(operator_stack[-1]) and hasHigherPrecedence(operator_stack[-1], token)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':  
                operator_stack.append(token)
            elif token == ')':  
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()

        while operator_stack:
            output.append(operator_stack.pop())

        return output

# convertir el la expression a postfix para el AFN
def infixToPostfix(expression):
    # reemplaza los espacios y ve los tokens o caracteres y los guarda en tokens
    expression = expression.replace(" ", "")
    tokens = [c for c in expression]

    # ejecuta el algoritmo shuntingYard y finalmente une la nueva expresión ya con los tokens en forma postfix
    postfix_tokens = shuntingYard(tokens)
    postfix_expression = "".join(postfix_tokens)
    
    return postfix_expression