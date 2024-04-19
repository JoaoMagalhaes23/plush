from dataclasses import dataclass

@dataclass
class Node:
    def __str__(self):
        return self.__class__.__name__


@dataclass
class ProgramNode(Node):
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class TopLevelDeclarations(Node):
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class ImmutableVariable(Node):
    name: str
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.name}"


@dataclass
class MutableVariable(Node):
    name: str
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.name}"

@dataclass
class Assign(Node):
    name: str
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.name}"

@dataclass
class Function(Node):
    name: str
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.name}"

@dataclass
class ParameterList(Node):
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class Parameter(Node):
    type: str
    name: str
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.type} {self.name}"

@dataclass
class Block(Node):
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class Return(Node):
    function_name: str
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.function_name}"

@dataclass
class If(Node):
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class ElseIf(Node):
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class Else(Node):
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class While(Node):
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class BinaryOp(Node):
    op: str
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.op}"
    
@dataclass
class Group(Node):
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__}"
    
@dataclass
class UnaryOp(Node):
    op: str
    children: list = None
    
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.op}"

@dataclass
class IntType(Node):
    def __str__(self):
        return self.__class__.__name__

@dataclass
class DoubleType(Node):
    def __str__(self):
        return self.__class__.__name__
    
@dataclass
class StringType(Node):
    def __str__(self):
        return self.__class__.__name__

@dataclass
class BooleanType(Node):
    def __str__(self):
        return self.__class__.__name__

@dataclass
class CharType(Node):
    def __str__(self):
        return self.__class__.__name__

@dataclass
class FloatType(Node):
    def __str__(self):
        return self.__class__.__name__

@dataclass
class VoidType(Node):
    def __str__(self):
        return self.__class__.__name__

@dataclass
class ArrayType(Node):
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__}"


@dataclass
class StringLiteral(Node):
    value: str

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"

@dataclass
class IntLiteral(Node):
    value: int

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"

@dataclass
class DoubleLiteral(Node):
    value: float

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"

@dataclass
class BooleanLiteral(Node):
    value: bool

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"

@dataclass
class CharLiteral(Node):
    value: str

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"

@dataclass
class FloatLiteral(Node):
    value: float

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"

@dataclass
class ArrayElement(Node):
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class Identifier(Node):
    value: str
    
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"
    
@dataclass
class Index(Node):
    array: str
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.array}"

@dataclass
class FunctionCall(Node):
    name: str
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.name}"

@dataclass
class ArgumentsList(Node):
    children: list = None

    def __str__(self):
        return f"{self.__class__.__name__}"

def print_ast(node, indent=0):
    if isinstance(node, Node):
        print('\t' * indent + str(node))
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                print_ast(child, indent + 1)
    else:
        print('\t' * indent + str(node))