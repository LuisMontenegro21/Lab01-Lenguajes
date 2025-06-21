'''
Functions used to perform the Shunting Yard algorithm
'''

precedence:dict = {'|': 1, '.': 2, '*': 3, '+' : 3, '?' : 3}

def is_operator(token: str) -> bool:
    # check if the operator keys are here
    return token in precedence.keys()


def has_higher_precedence(op1: str, op2: str) -> bool:
    # checks if the precedence of the operator on the right is bigger than the one on the left
    return precedence[op1] > precedence[op2]

def is_token(chr: str) -> bool:
    return not is_operator(chr) and chr not in {'(', ')'}


def shunting_yard(expression: list[str]) -> list[str]:
    '''
    Uses Shunting-Yard algorithm
    '''
    output: list[str] = []
    operator_stack: list[str] = []

    for token in expression:
        # if token is not an operator, and not a parenthesis
        #if token.isalnum():  
        if is_token(token):
            output.append(token)
        # if the token is operator
        elif is_operator(token):
            # check if the token 
            while (operator_stack and is_operator(operator_stack[-1]) and has_higher_precedence(operator_stack[-1], token)):
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

def place_implicit_concat(regex: str) -> list[str]:
    '''
    Place implicit symbol '.' for concatenation to simplify token handling
    '''
    tokens: list[str] = []
    prev: str | None = None
    left_side: set = {')', '*', '+', '?'}
    right_side: set = {'('}
    for char in regex:
        token = char
        # check if prev is None before using isalnum()
        if prev is not None:
            left_cond:bool = (is_token(prev) or (prev in left_side))
            right_cond:bool = (is_token(token) or (token in right_side))
            # if it satisfies both conditions, append a concatenation
            if left_cond and right_cond:
                tokens.append('.')
        # else leave it unchanged
        tokens.append(token)
        # update previous to current
        prev = token
    return tokens

# turn infix to postfix 
def infix_to_postfix(expression: str) -> str:
    # replace tokens and insert implicit concatenation
    tokens: list[str] = place_implicit_concat(expression)
    # runs shutting_yard algorithm
    postfix_tokens: list[str] = shunting_yard(tokens)
    postfix_expression:str = "".join(postfix_tokens)
    return postfix_expression