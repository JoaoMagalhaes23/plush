from node import ProgramNode, Statement, Type, Expression, MutableVariable, AssignArray, ImmutableVariable, Assign, Function, MutableParameter, ImmutableParameter, Block, If, While, BinaryOp, Group, UnaryOp, NotOp, IntType, StringType, BooleanType, CharType, FloatType, VoidType, ArrayType, IntLiteral, StringLiteral, BooleanLiteral, CharLiteral, FloatLiteral, Identifier, AccessArray, ArrayLiteral, FunctionCall
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
    "print_float": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=FloatType())], return_type=VoidType()),
    "print_string": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=StringType())], return_type=VoidType()),
    "print_char": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=CharType())], return_type=VoidType()),
    "print_boolean": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=BooleanType())], return_type=VoidType()),
    "print_int_array": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=ArrayType(subtype=IntType())), ImmutableParameter(name="y", type=IntType())], return_type=VoidType()),
    "print_2d_int_array": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=ArrayType(subtype=ArrayType(subtype=IntType()))), ImmutableParameter(name="y", type=IntType()), ImmutableParameter(name="z", type=IntType())], return_type=VoidType()),
    "concatenate_strings": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=StringType()), MutableParameter(name="y", type=StringType())], return_type=StringType()),
    "int_to_string": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=IntType())], return_type=StringType()),
    "print_string_array": FunctionDeclarationSignature(parameters=[MutableParameter(name="x", type=ArrayType(subtype=StringType())), ImmutableParameter(name="y", type=IntType())], return_type=VoidType()),
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
                return temp
        raise TypeError(f"Variable {name} is not in context")
            
    def check_if_function_signature_exists(self, name: str, parameters: list[Statement], return_type: Type, has_block: bool):
        scope = self.stack[0]
        func_in_scope= scope.get(name)
        if func_in_scope is not None:
            if isinstance(func_in_scope, FunctionSignature):
                raise TypeError(f"Function {name} already been defined")
            if isinstance(func_in_scope, MutableVariableDefinition) or isinstance(func_in_scope, ImmutableVariableDefinition):
                raise TypeError(f"The name {name} already been used as a variable")
            if isinstance(func_in_scope, FunctionDeclarationSignature):
                if len(func_in_scope.parameters) != len(parameters):
                    raise TypeError(f"Function {name} declaration  has {len(func_in_scope.parameters)} parameters but it was given {len(parameters)}")
                for i in range(len(parameters)):
                    if func_in_scope.parameters[i] != parameters[i]:
                        raise TypeError(f"Function {name} has parameter {func_in_scope.parameters[i]} but it was given {parameters[i]}")
                if func_in_scope.return_type != return_type:
                    raise TypeError(f"Function {name} declaration has return type {func_in_scope.return_type} but it was given {return_type}")
                self.set_function_signature_in_scope(name=name, parameters=parameters, return_type=return_type)
        else:
            if has_block:
                self.set_function_signature_in_scope(name=name, parameters=parameters, return_type=return_type)
            else:
                self.set_function_declaration_signature_in_scope(name=name, parameters=parameters, return_type=return_type)
    
    def get_function_signature(self, name: str):
        scope = self.stack[::-1][0]
        temp = scope.get(name)
        if temp is None:
            raise TypeError(f"Function {name} is not defined")
        if isinstance(temp, ImmutableVariableDefinition) or isinstance(temp, MutableVariableDefinition):
            raise TypeError(f"{name} is not a function")
        return temp
    
    def has_name_in_current_scope(self, name: str):
        return name in self.stack[0]

    def enter_scope(self):
        self.stack.insert(0, {})

    def exit_scope(self):
        self.stack.pop(0)

def verify(ctx: Context, ast: ProgramNode):
    for stmt in ast.statements:
        if isinstance(stmt, Function):    
            seen = set()
            if(any(i.name in seen or seen.add(i.name) for i in stmt.parameters)):
                raise TypeError(f"Function {stmt.name} has repeated parameters")
            ctx.check_if_function_signature_exists(name=stmt.name, parameters=stmt.parameters, return_type=stmt.return_type, has_block=stmt.block is not None) 
    for stmt in ast.statements:
        verify_statement(ctx=ctx, stmt=stmt)

def verify_statement(ctx: Context, stmt: Statement):
    if isinstance(stmt, ImmutableVariable):
        return verify_immutable_variable(ctx=ctx, node=stmt)
    elif isinstance(stmt, MutableVariable):
        return verify_mutable_variable(ctx=ctx, node=stmt)
    elif isinstance(stmt, Assign):
        return verify_assign(ctx=ctx, node=stmt)
    elif isinstance(stmt, Function):
        return verify_function(ctx=ctx, node=stmt)
    elif isinstance(stmt, Block):
        return verify_block(ctx=ctx, node=stmt)
    elif isinstance(stmt, If):
        return verify_if(ctx=ctx, node=stmt)
    elif isinstance(stmt, While):
        return verify_while(ctx=ctx, node=stmt)
    elif isinstance(stmt, FunctionCall):
        return verify_function_call(ctx=ctx, node=stmt)
    elif isinstance(stmt, AssignArray):
        return verify_assign_array(ctx=ctx, node=stmt)

def verify_expression(ctx: Context, expression: Expression, type: Type=None):
    if isinstance(expression, IntLiteral):
        return verify_int_literal(node=expression, type=type)
    elif isinstance(expression, BooleanLiteral):
        return verify_boolean_literal(node=expression, type=type)
    elif isinstance(expression, StringLiteral):
        return verify_string_literal(node=expression, type=type)
    elif isinstance(expression, CharLiteral):
        return verify_char_literal(node=expression, type=type)
    elif isinstance(expression, FloatLiteral):
        return verify_float_literal(node=expression, type=type)
    elif isinstance(expression, ArrayLiteral):
        return verify_array_literal(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, BinaryOp):
        return verify_binary_op(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, NotOp):
        return verify_not_op(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, UnaryOp):
        return verify_unary_op(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, Group):
        return verify_group(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, Identifier):
        return verify_identifier(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, FunctionCall):
        return verify_function_call(ctx=ctx, node=expression, type=type)
    elif isinstance(expression, AccessArray):
        return verify_access_array(ctx=ctx, node=expression, _type=type)

def verify_immutable_variable(ctx: Context, node: ImmutableVariable):
    if ctx.has_name_in_current_scope(name=node.name):
        raise TypeError(f"{node.name} already been declared")
    verify_expression(ctx=ctx, expression=node.expression, type=node.type)
    ctx.set_immutable_variable_type(name=node.name, type=node.type)

def verify_mutable_variable(ctx: Context, node: MutableVariable):
    if ctx.has_name_in_current_scope(name=node.name):
        raise TypeError(f"{node.name} already been declared")
    verify_expression(ctx=ctx, expression=node.expression, type=node.type)
    ctx.set_mutable_variable_type(name=node.name, type=node.type)

def verify_assign(ctx: Context, node: Assign):
    _type = ctx.get_mutable_variable_type(name=node.variable)
    verify_expression(ctx=ctx, expression=node.expression, type=_type)
    node.type = _type

def verify_assign_array(ctx: Context, node: AssignArray):
    verify_expression(ctx=ctx, expression=node._array, type=node.type)
    node._array.assigned = True
    verify_expression(ctx=ctx, expression=node.expression, type=node._array.type)
    node.type = node._array.type

def verify_function(ctx: Context, node: Function):
    ctx.enter_scope()
    ctx.set_parameters_in_scope(parameters=node.parameters)
    ctx.set_return_in_scope(function_name=node.name, type=node.return_type)
    verify_statement(ctx=ctx, stmt=node.block)
    ctx.exit_scope()

def verify_block(ctx: Context, node: Block):
    ctx.enter_scope()
    for stmt in node.statements:
        verify_statement(ctx=ctx, stmt=stmt)
    ctx.exit_scope()

def verify_if(ctx: Context, node: If):
    verify_expression(ctx=ctx, expression=node.condition, type=BooleanType())
    verify_statement(ctx=ctx, stmt=node.b1)
    if node.b2 is not None:
        verify_statement(ctx=ctx, stmt=node.b2)

def verify_while(ctx: Context, node: While):
    verify_expression(ctx=ctx, expression=node.condition, type=BooleanType())
    verify_statement(ctx=ctx, stmt=node.block)

def verify_binary_op(ctx: Context, node: BinaryOp, type: Type):
    verify_expression(ctx=ctx, expression=node.left_expression)
    first_type = node.left_expression.type
    verify_expression(ctx=ctx, expression=node.right_expression, type=first_type)
    operation = node.op
    if type is not None:
        node.type = first_type
        if operation in ['+', '-', '*', '/', '^', '%'] and not (isinstance(type, IntType) or isinstance(type, FloatType)):
            raise TypeError(f"Operation {operation} can only be applied to numeric types")
        elif operation in ['&&', '||'] and not isinstance(type, BooleanType):
            raise TypeError(f"Operation {operation} can only be applied to boolean types")
        elif operation in ['>', '>=', '<', '<='] and (isinstance(type, ArrayType) or isinstance(type, StringType) or isinstance(type, CharType)):
            raise TypeError(f"Operation {operation} can only be applied to numeric types")
    else:
        if operation in ['+', '-', '*', '/', '^', '%'] and (isinstance(first_type, IntType) or isinstance(first_type, FloatType)):
            node.type = first_type
            return first_type
        elif operation in ['&&', '||'] and isinstance(first_type, BooleanType):
            node.type = first_type
            return first_type
        elif operation in ['>', '>=', '<', '<='] and not (isinstance(first_type, ArrayType) or isinstance(first_type, StringType) or isinstance(first_type, CharType)):
            node.type = BooleanType()
        raise TypeError(f"Operation {operation} can only be applied to numeric types")

def verify_not_op(ctx: Context, node: NotOp, type: Type = None):
    if type is not None:
        verify_expression(ctx=ctx, expression=node.expression, type=type)
        node.type = type
    else:
        verify_expression(ctx=ctx, expression=node.expression)
        _type = node.expression.type
        if not isinstance(_type, BooleanType):
            raise TypeError("Unary operation can only be applied to boolean types")
        node.type = _type

def verify_unary_op(ctx: Context, node: UnaryOp, type: Type = None):
    if type is not None:
        if isinstance(type, ArrayType) or isinstance(type, StringType) or isinstance(type, CharType) or isinstance(type, BooleanType):
            raise TypeError("Unary operation can only be applied to numeric types")
        verify_expression(ctx=ctx, expression=node.expression, type=type)
        node.type = type
    else:
        verify_expression(ctx=ctx, expression=node.expression)
        _type = node.expression.type
        if isinstance(_type, ArrayType) or isinstance(_type, StringType) or isinstance(_type, CharType) or isinstance(_type, BooleanType):
            raise TypeError("Unary operation can only be applied to numeric types")
        node.type = _type

def verify_group(ctx: Context, node: Group, type: Type = None):
    if type is not None:
        verify_expression(ctx=ctx, expression=node.expression, type=type)
        node.type = type
    else:
        verify_expression(ctx=ctx, expression=node.expression)
        node.type = node.expression.type

def verify_identifier(ctx: Context, node: Identifier, type: Type = None):
    _type = ctx.get_variable(name=node.id).type
    node.type = _type
    if type is not None and _type != type:
        raise TypeError(f"The variable {node.id} is not of type {type}")

def verify_function_call(ctx: Context, node: FunctionCall, type: Type = None):
    _function = ctx.get_function_signature(name=node.name)
    if len(_function.parameters) != len(node.arguments):
        raise TypeError(f"Function {node.name} has {len(_function.parameters)} parameters but it was given {len(node.arguments)}")
    idx=0
    arguments=[]
    for arg in node.arguments:
        verify_expression(ctx=ctx, expression=arg, type=_function.parameters[idx].type)
        arguments.append(arg.type)
        idx+=1
    if type is not None and _function.return_type != type :
        raise TypeError(f"The function {node.name} returns {_function.return_type} but it was expected {type}")
    node.type = _function.return_type


def verify_access_array(ctx: Context, node: AccessArray, _type: Type):
    array_type = ctx.get_variable(name=node.array).type
    if not isinstance(array_type, ArrayType):
        raise TypeError(f"The variable {node.array} is not an array")
    a = array_type
    for index in node.indexes:
        try:
            a=a.subtype
            verify_expression(ctx=ctx, expression=index, type=IntType())
            
        except AttributeError:
            raise TypeError(f"Its impossible to do that many indexes in array {node.array}")
    if type(a) != type(_type) and _type is not None:
        raise TypeError("The type given is not the same as the result of indexing the array")
    node.type = a
    node.array_type = array_type

## Verify Literal Types

def verify_array_literal(ctx: Context, node: ArrayLiteral, type: Type):
    if type is not None and not isinstance(type, ArrayType):
        raise TypeError(f"It was needed a {type} but it was given ArrayType")
    if node.elements is not None:
        for element in node.elements:
            verify_expression(ctx=ctx, expression=element, type=type.subtype)
    node.type = type
    size = len(node.elements) if node.elements is not None else 0
    node.size = size
    type.size = size

def verify_int_literal(node: IntLiteral, type: Type = None):
    if type is not None and not isinstance(type, IntType):
        raise TypeError(f"It was needed a {type} but it was given IntType")
    node.type = IntType()

def verify_boolean_literal(node: BooleanLiteral, type: Type = None):
    if type is not None and not isinstance(type, BooleanType):
        raise TypeError(f"It was needed a {type} but it was given BooleanType")
    node.type = BooleanType()

def verify_string_literal(node: StringLiteral, type: Type = None):
    if type is not None and not isinstance(type, StringType):
        raise TypeError(f"It was needed a {type} but it was given StringType")
    node.type = StringType()

def verify_char_literal(node: CharLiteral, type: Type = None):
    if type is not None and not isinstance(type, CharType):
        raise TypeError(f"It was needed a {type} but it was given CharType")
    node.type = CharType()

def verify_float_literal(node: FloatLiteral, type: Type = None):
    if type is not None and not isinstance(type, FloatType):
        raise TypeError(f"It was needed a {type} but it was given FloatType")
    node.type = FloatType()
