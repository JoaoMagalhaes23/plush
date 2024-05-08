from node import *
from dataclasses import dataclass

@dataclass
class FunctionDeclarationSignature:
    parameters: list[Statement]
    return_type: Type

@dataclass
class FunctionSignature:
    parameters: list[Statement]
    return_type: Type

@dataclass
class MutableVariableDefinition:
    type: Type

@dataclass
class ImmutableVariableDefinition:
    type: Type

@dataclass
class MutableParameterDefinition:
    type: Type

@dataclass
class ImmutableParameterDefinition:
    type: Type

@dataclass
class ReturnStatement:
    function_name: str
    type: Type

class TypeError(Exception):
    pass

context_values = {
    "print_int": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=IntType())], return_type=VoidType()),
    "print_double": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=DoubleType())], return_type=VoidType()),
    "print_string": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=StringType())], return_type=VoidType()),
    "print_char": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=CharType())], return_type=VoidType()),
    "print_bool": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=BooleanType())], return_type=VoidType()),
}

class Context(object):
    def __init__(self):
        self.stack = [context_values]
    def get_mutable_variable_type(self, name: str):
        for scope in self.stack:
            temp = scope.get(name)
            if isinstance(temp, MutableVariableDefinition) or isinstance(temp, MutableParameterDefinition) or isinstance(temp, ReturnStatement):
                return temp.type
            elif isinstance(temp, ImmutableVariableDefinition) or isinstance(temp, ImmutableParameterDefinition):
                raise TypeError(f"Variable {name} is immutable")
        raise TypeError(f"Variable {name} is not in context")
    
    def set_function_signature_in_scope(self, name: str, parameters: list[Statement], return_type: Type):
        scope = self.stack[0]
        scope[name] = FunctionSignature(parameters=parameters, return_type=return_type)
    
    def set_function_declaration_signature_in_scope(self, name: str, parameters: list[Statement], return_type: Type):
        scope = self.stack[0]
        scope[name] = FunctionDeclarationSignature(parameters=parameters, return_type=return_type)
    
    def set_mutable_variable_type(self, name: str, type: Type):
        scope = self.stack[0]
        scope[name] = MutableVariableDefinition(type=type)
    
    def set_immutable_variable_type(self, name: str, type: Type):
        scope = self.stack[0]
        scope[name] = ImmutableVariableDefinition(type=type)
    
    def set_parameters_in_scope(self, parameters: list[Statement]):
        scope = self.stack[0]
        for param in parameters:
            if isinstance(param, MutableParameter):
                scope[param.name] = MutableParameterDefinition(type=param.type)
            else:
                scope[param.name] = ImmutableParameterDefinition(type=param.type)
                
    def set_return_in_scope(self, function_name: str, type: Type):
        scope = self.stack[0]
        scope[function_name] = ReturnStatement(function_name=function_name, type=type)
    
    def get_variable(self, name: str):
        for scope in self.stack:
            temp = scope.get(name)
            if isinstance(temp, MutableVariableDefinition) or isinstance(temp, ImmutableVariableDefinition)  or isinstance(temp, MutableParameterDefinition) or isinstance(temp, ImmutableParameterDefinition):
                return temp.type
        raise TypeError(f"Variable {name} is not in context")
            
    def check_if_function_signature_exists(self, name: str, parameters: list[Statement], return_type: Type):
        scope = self.stack[0]
        temp = scope.get(name)
        if temp is not None:
            if isinstance(temp, FunctionSignature):
                raise TypeError(f"Function {name} already been defined")
            if isinstance(temp, MutableVariableDefinition) or isinstance(temp, ImmutableVariableDefinition):
                raise TypeError(f"The name {name} already been used as a variable")
            if isinstance(temp, FunctionDeclarationSignature):
                if len(temp.parameters) != len(parameters):
                    raise TypeError(f"Function {name} declaration  has {len(temp.parameters)} parameters but it was given {len(parameters)}")
                for i in range(len(parameters)):
                    if temp.parameters[i] != parameters[i]:
                        raise TypeError(f"Function {name} has parameter {temp.parameters[i]} but it was given {parameters[i]}")
                if temp.return_type != return_type:
                    raise TypeError(f"Function {name} declaration has return type {temp.return_type} but it was given {return_type}")
        return temp

    def check_function_call(self, name: str, arguments: list[Expression]):
        for scope in self.stack:
            temp = scope.get(name)
            if isinstance(temp, FunctionSignature) or isinstance(temp, FunctionDeclarationSignature):
                if len(temp.parameters) != len(arguments):
                    raise TypeError(f"Function {name} has {len(temp.parameters)} parameters but it was given {len(arguments)}")
                for i in range(len(arguments)):
                    if temp.parameters[i].type != arguments[i]:
                        raise TypeError(f"Function {name} has parameter {temp.parameters[i].type} but it was given {arguments[i]}")
                return temp.return_type
        raise TypeError(f"Function {name} is not in context or the number of parameters is wrong")   
    
    def has_name_in_current_scope(self, name: str):
        return name in self.stack[0]

    def enter_scope(self):
        self.stack.insert(0, {})

    def exit_scope(self):
        self.stack.pop(0)

def verify(ctx: Context, ast: ProgramNode):
    for stmt in ast.statements:
        verifyStatement(ctx=ctx, stmt=stmt)

def verifyStatement(ctx: Context, stmt: Statement):
    if isinstance(stmt, ImmutableVariable):
        return verifyImmutableVariable(ctx=ctx, node=stmt)
    elif isinstance(stmt, MutableVariable):
        return verifyMutableVariable(ctx=ctx, node=stmt)
    elif isinstance(stmt, Assign):
        return verifyAssign(ctx=ctx, node=stmt)
    elif isinstance(stmt, Function):
        return verifyFunction(ctx=ctx, node=stmt)
    elif isinstance(stmt, Block):
        return verifyBlock(ctx=ctx, node=stmt)
    elif isinstance(stmt, If):
        return verifyIf(ctx=ctx, node=stmt)
    elif isinstance(stmt, While):
        return verifyWhile(ctx=ctx, node=stmt)
    elif isinstance(stmt, FunctionCall):
        return verifyFunctionCall(ctx=ctx, node=stmt)

def verifyExpression(ctx: Context, expression: Expression, type: Type=None):
    if isinstance(expression, IntLiteral):
        return verifyIntLiteral(node=expression, type=type)
    elif isinstance(expression, BooleanLiteral):
        return verifyBooleanLiteral(node=expression, type=type)
    elif isinstance(expression, DoubleLiteral):
        return verifyDoubleLiteral(node=expression, type=type)
    elif isinstance(expression, StringLiteral):
        return verifyStringLiteral(node=expression, type=type)
    elif isinstance(expression, CharLiteral):
        return verifyCharLiteral(node=expression, type=type)
    elif isinstance(expression, FloatLiteral):
        return verifyFloatLiteral(node=expression, type=type)
    elif isinstance(expression, ArrayLiteral):
        return verifyArrayLiteral(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, BinaryOp):
        return verifyBinaryOp(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, NotOp):
        return verifyNotOp(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, UnaryOp):
        return verifyUnaryOp(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, Group):
        return verifyGroup(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, Identifier):
        return verifyIdentifier(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, FunctionCall):
        return verifyFunctionCall(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, AccessArray):
        return verifyAccessArray(ctx=ctx, node=expression, type=type)
    
def verifyProgramNode(ctx: Context, node: ProgramNode):
    for stmt in node.children:
        verifyStatement(ctx = ctx, stmt = stmt)

def verifyImmutableVariable(ctx: Context, node: ImmutableVariable):
    if ctx.has_name_in_current_scope(name=node.name):
        raise TypeError(f"{node.name} already been declared")
    verifyExpression(ctx=ctx, expression=node.expression, type=node.type)
    ctx.set_immutable_variable_type(name=node.name, type=node.type)

def verifyMutableVariable(ctx: Context, node: MutableVariable):
    if ctx.has_name_in_current_scope(name=node.name):
        raise TypeError(f"{node.name} already been declared")
    verifyExpression(ctx=ctx, expression=node.expression, type=node.type)
    ctx.set_mutable_variable_type(name=node.name, type=node.type)

def verifyAssign(ctx: Context, node: Assign):
    type = ctx.get_mutable_variable_type(name=node.name)
    verifyExpression(ctx=ctx, expression=node.expression, type=type)
    node.type = type

def verifyFunction(ctx: Context, node: Function):
    seen = set()
    if(any(i.name in seen or seen.add(i.name) for i in node.parameters)):
        raise TypeError(f"Function {node.name} has repeated parameters")
    ctx_func = ctx.check_if_function_signature_exists(name=node.name, parameters=node.parameters, return_type=node.return_type)
    if node.block is not None:
        ctx.set_function_signature_in_scope(name=node.name, parameters=node.parameters, return_type=node.return_type)
        ctx.enter_scope()
        ctx.set_parameters_in_scope(parameters=node.parameters)
        ctx.set_return_in_scope(function_name=node.name, type=node.return_type)
        verifyStatement(ctx=ctx, stmt=node.block)
        ctx.exit_scope()
    else:
        if isinstance(ctx_func, FunctionDeclarationSignature):
            raise TypeError(f"Function {node.name} already been declared")
        ctx.set_function_declaration_signature_in_scope(name=node.name, parameters=node.parameters, return_type=node.return_type)

def verifyBlock(ctx: Context, node: Block):
    ctx.enter_scope()
    for stmt in node.statements:
        verifyStatement(ctx=ctx, stmt=stmt)
    ctx.exit_scope()

def verifyIf(ctx: Context, node: If):
    verifyExpression(ctx=ctx, expression=node.condition, type=BooleanType())
    verifyStatement(ctx=ctx, stmt=node.b1)
    if node.b2 is not None:
        verifyStatement(ctx=ctx, stmt=node.b2)

def verifyWhile(ctx: Context, node: While):
    verifyExpression(ctx=ctx, expression=node.condition, type=BooleanType())
    verifyStatement(ctx=ctx, stmt=node.block)

def verifyBinaryOp(ctx: Context, node: BinaryOp, type: Type):
    first_type = verifyExpression(ctx=ctx, expression=node.left_expression)
    verifyExpression(ctx=ctx, expression=node.right_expression, type=first_type)
    node.type = type
    operation = node.op
    if operation in ['+', '-', '*', '/', '^', '%']:
        if not isinstance(type, IntType) and not isinstance(type, FloatType) and not isinstance(type, DoubleType):
            raise TypeError(f"Operation {operation} can only be applied to numeric types")
    elif operation in ['&&', '||']:
        if not isinstance(type, BooleanType):
            raise TypeError(f"Operation {operation} can only be applied to boolean types")

def verifyNotOp(ctx: Context, node: NotOp, type: Type = None):
    if type is not None:
        verifyExpression(ctx=ctx, expression=node.expression, type=type)
    else:
        type = verifyExpression(ctx=ctx, expression=node.expression)
        if not isinstance(type, BooleanType):
            raise TypeError(f"Unary operation can only be applied to boolean types")
        node.type = type
        return type

def verifyUnaryOp(ctx: Context, node: UnaryOp, type: Type = None):
    if type is not None:
        if isinstance(type, ArrayType) or isinstance(type, StringType) or isinstance(type, CharType) or isinstance(type, BooleanType):
            raise TypeError(f"Unary operation can only be applied to numeric types")
        verifyExpression(ctx=ctx, expression=node.expression, type=type)
        node.type = type
    else:
        type = verifyExpression(ctx=ctx, expression=node.expression)
        if isinstance(type, ArrayType) or isinstance(type, StringType) or isinstance(type, CharType) or isinstance(type, BooleanType):
            raise TypeError(f"Unary operation can only be applied to numeric types")
        node.type = type
        return type

def verifyGroup(ctx: Context, node: Group, type: Type = None):
    if type is not None:
        verifyExpression(ctx=ctx, expression=node.expression, type=type)
        node.type = type
    else:
        node.type = verifyExpression(ctx=ctx, expression=node.expression)
        return node.type

def verifyIdentifier(ctx: Context, node: Identifier, type: Type = None):
    id_type = ctx.get_variable(name=node.id)
    node.type = id_type
    if type is not None:
        if id_type != type:
            raise TypeError(f"The variable {node.id} is not of type {type}")
    else:
        return id_type

def verifyFunctionCall(ctx: Context, node: FunctionCall, type: Type = None):
    arguments=[]
    for arg in node.arguments:
        arguments.append(verifyExpression(ctx=ctx, expression=arg))
    return_type = ctx.check_function_call(name=node.name, arguments=arguments)
    node.type = return_type
    if type is not None:
        if return_type != type:
            raise TypeError(f"The function {node.name} returns {return_type} but it was expected {type}")
    else:
        return return_type

def verifyAccessArray(ctx: Context, node: AccessArray, type: Type):
    array_type = ctx.get_variable(name=node.array)
    if not isinstance(array_type, ArrayType):
        raise TypeError(f"The variable {node.array} is not an array")
    for _ in node.indexes:
        try:
            array_type=array_type.subtype
        except AttributeError:
            raise TypeError(f"Its impossible to do that many indexes in array {node.array}")
    if array_type != type:
        raise TypeError(f"The type given is not the same as the result of indexing the array")

## Verify Literal Types

def verifyArrayLiteral(ctx: Context, node: ArrayLiteral, type: Type):
    if not isinstance(type, ArrayType):
        raise TypeError(f"It was needed a {type} but it was given ArrayType")
    if node.elements is not None:
        for element in node.elements:
            verifyExpression(ctx=ctx, expression=element, type=type.subtype)
    node.type = ArrayType()
    return type

def verifyIntLiteral(node: Expression, type: Type = None):
    if type is not None and not isinstance(type, IntType):
        raise TypeError(f"It was needed a {type} but it was given IntType")
    node.type = IntType()
    return IntType()

def verifyBooleanLiteral(node: Expression, type: Type = None):
    if type is not None and not isinstance(type, BooleanType):
        raise TypeError(f"It was needed a {type} but it was given BooleanType")
    node.type = BooleanType()
    return BooleanType()

def verifyDoubleLiteral(node: Expression, type: Type = None):
    if type is not None and not isinstance(type, DoubleType):
        raise TypeError(f"It was needed a {type} but it was given DoubleType")
    node.type = DoubleType()
    return DoubleType()

def verifyStringLiteral(node: Expression, type: Type = None):
    if not isinstance(type, StringType):
        raise TypeError(f"It was needed a {type} but it was given StringType")
    node.type = StringType()
    return StringType()

def verifyCharLiteral(node: Expression, type: Type = None):
    if type is not None and not isinstance(type, CharType):
        raise TypeError(f"It was needed a {type} but it was given CharType")
    node.type = CharType()
    return CharType()

def verifyFloatLiteral(node: Expression, type: Type = None):
    if type is not None and not isinstance(type, FloatType):
        raise TypeError(f"It was needed a {type} but it was given FloatType")
    node.type = FloatType()
    return FloatType()