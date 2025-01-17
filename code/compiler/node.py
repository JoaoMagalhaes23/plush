from dataclasses import dataclass, asdict

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
    imports: list[Statement] = None
    statements: list[Statement] = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class ImportStatement(Statement):
    file_name: str = None
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.file_name}"

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
    variable: str = None
    expression: Expression = None
    type: Type = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.variable}"

@dataclass 
class AssignArray(Statement):
    _array: Expression = None
    expression: Expression = None
    type: Type = None

    def __str__(self):
        return f"{self.__class__.__name__}"

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
    expression : Expression = None

    def __str__(self):
        return f"{self.__class__.__name__ }-> {self.name}"

@dataclass
class ImmutableParameter(Statement):
    name: str
    type: Type
    expression : Expression = None

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
    b1: Block = None
    b2: Block = None

    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class While(Statement):
    condition: Expression = None
    block: Block = None

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
class Identifier(Expression):
    id: str
    type: Type = None
    
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.id}"

@dataclass
class FunctionCall(Expression):
    name: str
    arguments: list[Expression] = None
    type: Type = None

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.name}"

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
    size: int = None
    def __str__(self):
        return f"{self.__class__.__name__}"

@dataclass
class AccessArray(Expression):
    array: str
    indexes: list[Expression] = None
    type: Type = None
    array_type: Type = None
    assigned: bool = False
    def __str__(self):
        return f"{self.__class__.__name__} -> {self.array}"

@dataclass
class IntType(Type):
    name: str = "int"
    def __str__(self):
        return self.__class__.__name__
    
@dataclass
class StringType(Type):
    name: str = "string"
    def __str__(self):
        return self.__class__.__name__

@dataclass
class BooleanType(Type):
    name: str = "boolean"
    def __str__(self):
        return self.__class__.__name__

@dataclass
class CharType(Type):
    name: str = "char"
    def __str__(self):
        return self.__class__.__name__

@dataclass
class FloatType(Type):
    name: str = "float"
    def __str__(self):
        return self.__class__.__name__

@dataclass
class VoidType(Type):
    name: str = "void"
    def __str__(self):
        return self.__class__.__name__

@dataclass
class ArrayType(Type):
    name: str = "array"
    subtype: Type = None
    size: int = None
    def __str__(self):
        return f"{self.__class__.__name__}"


def print_ast(node, indent=0):
    if isinstance(node, ProgramNode):
        print('\t' * indent + str(node))
        if node.imports:
            for child in node.imports:
                print_ast(child, indent + 1)
        if node.statements:
            for child in node.statements:
                print_ast(child, indent + 1)
    elif isinstance(node, Statement):
        print('\t' * indent + str(node))
        if hasattr(node, 'expression') and node.expression:
            print_ast(node.expression, indent + 1)
        if hasattr(node, 'type') and node.type:
            print_ast(node.type, indent + 1)
        if hasattr(node, '_array') and node._array:
            print_ast(node._array, indent + 1)
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
        if hasattr(node, 'size') and node.size:
            print('\t' * indent + "size " +  str(node.size))
            
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
        if hasattr(node, 'size') and node.size:
            print('\t' * indent + "size " + str(node.size))
    else:
        print(f"node {str(node)} not found")

def ast_to_json_file(ast, directory):
    import json
    import os
    output_file_path = os.path.join(directory, "ast.json")
    dict_ast = asdict(ast)
    with open(output_file_path, "w") as f:
        json.dump(dict_ast, f, indent=4)