'''
Functions used to perform the Shunting Yard algorithm to transform infix to postfix
Needs some changes like converting symbols to ASCII for easier acceptance
'''

precedence:dict = {'|': 1, '.': 2, '*': 3, '+' : 3, '?' : 3}

ESCAPED_CASES = {
    'd' : list("0123456789"),
    'w' : list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"),
    's' : list(" \t\n\r\f\v"),
}
#TODO fix escaped cases
ESCAPED_LITERALS = {
    's': ' ',       
    't': '\t',     
    'n': '\n',     
    'r': '\r',
    'f': '\f',
    'v': '\v',
}


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


def place_implicit_concat(regex: list[str]) -> list[str]:
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

def expand_replace(regex: str) -> list:
    '''
    Expands ranges like [A-Z] into (A|B|C|D|E|F...|X|Z)
    Also handles escaped cases like \\d, \\w, \\s, etc.
    And appends strings under "" as one character 
    '''
    i: int = 0
    result: list = []
    while i < len(regex):
        # check special chars or strings
        if regex[i] == '"':
            i +=1 
            special_char: str = ""
            while i < len(regex) and regex[i] != '"':
                special_char += regex[i]
                i += 1
            result.append(special_char)
            i+=1
        # check if its a range
        elif regex[i] == '[':
            i += 1
            expanded: list = []
            while i < len(regex) and regex[i] != ']':
                if regex[i] == '\\':
                    if i + 1 < len(regex):
                        esc = regex[i+1] # get the escaped char
                        if esc in ESCAPED_LITERALS:
                            expanded.extend(ESCAPED_LITERALS[esc])
                        elif esc in ESCAPED_CASES:
                            expanded.extend(ESCAPED_CASES[esc])
                        else:
                            expanded.append('\\' + esc)
                        i += 2
                    else:
                        expanded.append('\\')
                        i += 1

                elif i+2 < len(regex) and regex[i+1] == '-':
                    
                    start, end = regex[i], regex[i+2]
                    expanded.extend([chr(c) for c in range(ord(start), ord(end) + 1)]) # append the characters in the ordinary range
                    i += 3

                else:
                    expanded.append(regex[i])
                    i += 1
            # append results as list containing
            result.append('(')
            for j, val in enumerate(expanded):
                if j > 0: # append | after the first element
                    result.append('|')
                result.append(val)
            result.append(')')
            i+=1
        # else, leave it unchanged and just append
        else:
            result.append(regex[i])
            i += 1
    return result

# turn infix to postfix 
def infix_to_postfix(expression: str) -> list[str]:
    # replace tokens and insert implicit concatenation after replacing and expanding expressions
    tokens: list[str] = place_implicit_concat(expand_replace(expression))
    # runs shutting_yard algorithm
    postfix_tokens: list[str] = shunting_yard(tokens)
    return postfix_tokens