from typing import Optional

class PNode:
    '''
    Base parent class for a Node
    '''
    __slots__ = ('value', 'left', 'right') # use slots to avoid __dict__ being generated. New class attributes become dynamically immutable

    def __init__(self, value: Optional[str], left: Optional['PNode'] = None, right: Optional['PNode'] = None) -> None:
        self.value = value
        self.left: PNode = left
        self.right: PNode = right
    
    def as_string(self) -> str:
        print(f"Node: {self.value}")


class Node(PNode):
    '''
    Node used for the Direct DFA
    '''
    __slots__ = PNode.__slots__  + ('nullable', 'firstpos', 'lastpos', 'position') # inherit slots from parent class, make it faster due to making class immutable

    def __init__(self, value: str, left:Optional['Node']=None, right:Optional['Node']=None) -> None:  
        super().__init__(value=value, left=left,right=right) # gather upper constructor
        self.nullable: bool = False
        self.firstpos: set[int] = set()
        self.lastpos: set[int] = set()
        self.position: int = 0

    def as_string(self) -> str:
        '''Represents node as a string'''
        return f"Node: {self.value} Position: {self.position} Firstpos: {self.firstpos} Lastpos: {self.lastpos} Nullable: {self.nullable}"
    

class LitNode(PNode):
    __slots__ = PNode.__slots__ + ('value',)
    def __init__(self, value: str):
        self.value = value
    
    def as_string(self) -> str:
        return self.value
    
class BinaryNode(PNode):
    __slots__ = PNode.__slots__ + ('operator','left', 'right')
    def __init__(self, operator:str, left:PNode, right:PNode):
        self.operator = operator
        self.left = left
        self.right = right
    
    def as_string(self) -> str:
        return f"({self.left.as_string()}{self.operator}{self.right.as_string()})"

class UnaryNode(PNode):
    __slots__ = PNode.__slots__ + ('operator','child')
    def __init__(self, operator: str, child:PNode):
        self.operator = operator
        self.child = child
    
    def as_string(self) -> str:
        return f"({self.child.as_string()})"
