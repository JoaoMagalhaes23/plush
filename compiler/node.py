from dataclasses import dataclass

@dataclass
class Node:
    def __str__(self):
        return self.__class__.__name__

@dataclass
class Type(Node):
    pass

@dataclass
class Statement(Node):
    pass

@dataclass
class Expression(Node):
    pass

@dataclass
class ProgramNode(Node):
    statements: list[Statement] = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class ImmutableVariable(Statement):
    name: str
    type: Type = None
    expression: Expression = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.name}"

@dataclass
class MutableVariable(Statement):
    name: str
    type: Type = None
    expression: Expression = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.name}"

@dataclass
class Assign(Statement):
    name: str
    expression: Expression = None
    type: Type = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.name}"

@dataclass
class Function(Statement):
    name: str
    parameters: list[Statement] = None
    return_type: Type = None
    block: Statement = None
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.name}"

@dataclass
class MutableParameter(Statement):
    name: str
    type: Type

    def __str__(self):
        return f"{self.__class__.__name__ }-> {self.name}"

@dataclass
class ImmutableParameter(Statement):
    name: str
    type: Type

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.name}"

@dataclass
class Block(Statement):
    statements: list[Statement] = None

    def __str__(self):
        return f"{self.__class__.__name__}"
    
@dataclass
class If(Statement):
    condition: Expression = None
    b1: Statement = None
    b2: Statement = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class While(Statement):
    condition: Expression = None
    block: Statement = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class BinaryOp(Expression):
    op: str
    left_expression: Expression = None
    right_expression: Expression = None
    type: Type = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.op}"
    
@dataclass
class Group(Expression):
    expression: Expression = None
    type: Type = None
    def __str__(self):
        return f"{self.__class__.__name__}"
    
@dataclass
class UnaryOp(Expression):
    expression: Expression = None
    type: Type = None
    def __str__(self):
        return f"{self.__class__.__name__}"
    
@dataclass
class NotOp(Expression):
    expression: Expression = None
    type: Type = None
    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class IntType(Type):
    def __str__(self):
        return self.__class__.__name__

@dataclass
class DoubleType(Type):
    def __str__(self):
        return self.__class__.__name__
    
@dataclass
class StringType(Type):
    def __str__(self):
        return self.__class__.__name__

@dataclass
class BooleanType(Type):
    def __str__(self):
        return self.__class__.__name__

@dataclass
class CharType(Type):
    def __str__(self):
        return self.__class__.__name__

@dataclass
class FloatType(Type):
    def __str__(self):
        return self.__class__.__name__

@dataclass
class VoidType(Type):
    def __str__(self):
        return self.__class__.__name__

@dataclass
class ArrayType(Type):
    subtype: Type = None
    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class StringLiteral(Expression):
    value: str
    type: Type = None
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"

@dataclass
class IntLiteral(Expression):
    value: int
    type: Type = None
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"

@dataclass
class DoubleLiteral(Expression):
    value: float
    type: Type = None
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"

@dataclass
class BooleanLiteral(Expression):
    value: bool
    type: Type = None
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"

@dataclass
class CharLiteral(Expression):
    value: str
    type: Type = None
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"

@dataclass
class FloatLiteral(Expression):
    value: float
    type: Type = None
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.value}"

@dataclass
class ArrayLiteral(Expression):
    elements: list[Expression] = None
    type: Type = None
    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class Identifier(Expression):
    id: str
    type: Type = None
    
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.id}"
    
@dataclass
class AccessArray(Expression):
    array: str
    indexes: list[Expression] = None
    type: Type = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.array}"

@dataclass
class FunctionCall(Expression):
    name: str
    arguments: list[Expression] = None
    type: Type = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.name}"

def print_ast(node, indent=0):
    if isinstance(node, ProgramNode):
        print('\t' * indent + str(node))
        if node.statements:
            for child in node.statements:
                print_ast(child, indent + 1)
    elif isinstance(node, Statement):
        print('\t' * indent + str(node))
        if hasattr(node, 'expression') and node.expression:
            print_ast(node.expression, indent + 1)
        if hasattr(node, 'type') and node.type:
            print_ast(node.type, indent + 1)
        if hasattr(node, 'parameters') and node.parameters:
            for parameter in node.parameters:
                print_ast(parameter, indent + 1)
        if hasattr(node, 'return_type') and node.return_type:
            print_ast(node.return_type, indent + 1)
        if hasattr(node, 'block') and node.block:
            print_ast(node.block, indent + 1)
        if hasattr(node, 'statements') and node.statements:
            for statement in node.statements:
                print_ast(statement, indent + 1)
        if hasattr(node, 'condition') and node.condition:
            print_ast(node.condition, indent + 1)
        if hasattr(node, 'b1') and node.b1:
            print_ast(node.b1, indent + 1)
        if hasattr(node, 'b2') and node.b2:
            print_ast(node.b2, indent + 1)
    elif isinstance(node, Type):
        print('\t' * indent + str(node))
        if hasattr(node, 'subtype') and node.subtype:
            print_ast(node.subtype, indent + 1)
    elif isinstance(node, Expression):
        print('\t' * indent + str(node))
        if hasattr(node, 'elements'):
            if node.elements is not None:
                for element in node.elements:
                    print_ast(element, indent + 1)
        if hasattr(node, 'expression') and node.expression:
            print_ast(node.expression, indent + 1)
        if hasattr(node, 'left_expression') and node.left_expression:
            print_ast(node.left_expression, indent + 1)
        if hasattr(node, 'right_expression') and node.right_expression:
            print_ast(node.right_expression, indent + 1)	
        if hasattr(node, 'type') and node.type:
            print_ast(node.type, indent + 1)
        if hasattr(node, 'indexes') and node.indexes:
            for index in node.indexes:
                print_ast(index, indent + 1)
        if hasattr(node, 'arguments') and node.arguments:
            for argument in node.arguments:
                print_ast(argument, indent + 1)
    else:
        print(f"node {str(node)} not found")