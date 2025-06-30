from Automata.Nodes import UnaryNode, BinaryNode, LitNode
from Algorithms.Postfix import infix_to_postfix, precedence


def build_syntax_tree(regex:str) -> UnaryNode | BinaryNode | LitNode | None:
    '''
    Builds a syntax tree 
    '''
    postfix:list[str] = infix_to_postfix(expression=regex)
    stack:list[UnaryNode | BinaryNode | LitNode] = []

    for char in postfix:
        if char not in precedence.keys():
            stack.append(LitNode(char))
        elif char in {'.', '|'}:
            right = stack.pop()
            left = stack.pop()
            node = BinaryNode(char, left, right)
            stack.append(node)
        elif char in {'*', '+', '?'}:
            operand = stack.pop()
            node = UnaryNode(char, operand)
            stack.append(node)


    return stack.pop() if stack else None # return tree root 

    