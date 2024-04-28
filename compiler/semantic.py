from node import *
from dataclasses import dataclass

@dataclass
class FunctionDeclarationSignature:
    parameters: list
    return_type: Node

@dataclass
class FunctionSignature:
    parameters: list
    return_type: Node

@dataclass
class MutableVariableDefinition:
    type: Node

@dataclass
class ImmutableVariableDefinition:
    type: Node

class TypeError(Exception):
    pass

class Context(object):
    def __init__(self):
        self.stack = [{}]
    
    def get_type(self, name):
        for scope in self.stack:
            if name in scope:
                return scope[name]
        raise TypeError(f"Variable {name} is not in context")
    
    def set_function_signature_in_scope(self, name, parameters, return_type):
        scope = self.stack[0]
        scope[name] = FunctionSignature(parameters, return_type)
    
    def set_function_declaration_signature_in_scope(self, name, parameters, return_type):
        scope = self.stack[0]
        scope[name] = FunctionDeclarationSignature(parameters, return_type)
    
    def set_mutable_variable_type(self, name, type):
        scope = self.stack[0]
        scope[name] = MutableVariableDefinition(type)
    
    def set_immutable_variable_type(self, name, type):
        scope = self.stack[0]
        scope[name] = ImmutableVariableDefinition(type)

    def check_assign(self, name, type):
        for scope in self.stack:
            temp = scope.get(name)
            if isinstance(temp, MutableVariableDefinition):
                if temp.type != type:
                    raise TypeError(f"Variable {name} has type {temp.type} but it was given {type}")
                return
            if isinstance(temp, ImmutableVariableDefinition):
                raise TypeError(f"Variable {name} is immutable")
        raise TypeError(f"Variable {name} is not in context")
    
    def has_variable(self, name):
        for scope in self.stack:
            temp = scope.get(name)
            if isinstance(temp, MutableVariableDefinition) or isinstance(temp, ImmutableVariableDefinition):
                return True
        return False
    
    def check_identifier(self, name, type):
        for scope in self.stack:
            temp = scope.get(name)
            if isinstance(temp, MutableVariableDefinition) or isinstance(temp, ImmutableVariableDefinition):
                if temp.type != type:
                    raise TypeError(f"Variable {name} has type {temp.type} but has given {type}")
                return
            
    def check_if_function_name_exists(self, name, parameters, return_type):
        scope = self.stack[0]
        temp = scope.get(name)
        if temp is not None:
            if isinstance(temp, FunctionSignature):
                raise TypeError(f"Function {name} already been declared")
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

    def check_function_call(self, name, arguments):
        for scope in self.stack:
            temp = scope.get(name)
            if isinstance(temp, FunctionSignature) or isinstance(temp, FunctionDeclarationSignature):
                if len(temp.parameters) != len(arguments):
                    raise TypeError(f"Function {name} has {len(temp.parameters)} parameters but it was given {len(arguments)}")
                for i in range(len(arguments)):
                    if temp.parameters[i].child != arguments[i]:
                        raise TypeError(f"Function {name} has parameter {temp.parameters[i].child} but it was given {arguments[i]}")
                return temp.return_type
        raise TypeError(f"Function {name} is not in context or the number of parameters is wrong")   
    
    def has_name_in_current_scope(self, name):
        return name in self.stack[0]

    def enter_scope(self):
        self.stack.insert(0, {})

    def exit_scope(self):
        self.stack.pop(0)

def verify(ctx:Context, node: Node):
    if isinstance(node, ProgramNode):
        return verifyProgramNode(ctx, node)
    elif isinstance(node, TopLevelDeclarations):
        return verifyTopLevelDeclarations(ctx, node)
    elif isinstance(node, ImmutableVariable):
        return verifyImmutableVariable(ctx, node)
    elif isinstance(node, MutableVariable):
        return verifyMutableVariable(ctx, node)
    elif isinstance(node, Assign):
        return verifyAssign(ctx, node)
    elif isinstance(node, Index):
        return verifyIndex(ctx, node)
    elif isinstance(node, Function):
        return verifyFunction(ctx, node)
    elif isinstance(node, ParameterList):
        return verifyParameterList(ctx, node)
    elif isinstance(node, NotOp):
        return verifyNotOp(ctx, node)
    elif isinstance(node, UnaryOp):
        return verifyUnaryOp(ctx, node)
    elif isinstance(node, BinaryOp):
        return verifyBinaryOp(ctx, node)
    elif isinstance(node, If):
        return verifyIf(ctx, node)
    elif isinstance(node, ElseIf):
        return verifyElseIf(ctx, node)
    elif isinstance(node, Else):
        return verifyElse(ctx, node)
    elif isinstance(node, While):
        return verifyWhile(ctx, node)
    elif isinstance(node, IntLiteral):
        return verifyIntLiteral()
    elif isinstance(node, BooleanLiteral):
        return verifyBooleanLiteral()
    elif isinstance(node, DoubleLiteral):
        return verifyDoubleLiteral()
    elif isinstance(node, StringLiteral):
        return verifyStringLiteral()
    elif isinstance(node, CharLiteral):
        return verifyCharLiteral()
    elif isinstance(node, FloatLiteral):
        return verifyFloatLiteral()
    elif isinstance(node, Identifier):
        return verifyIdentifier(ctx, node)
    elif isinstance(node, Block):
        return verifyBlock(ctx, node)
    elif isinstance(node, FunctionCall):
        return verifyFunctionCall(ctx, node)
    elif isinstance(node, ArgumentsList):
        return verifyArgumentsList(ctx, node)
    else:
        raise TypeError(f"Node {node} nao reconhecido")
        
def verifyProgramNode(ctx: Context, node: Node):
    for decl in node.children:
        verify(ctx, decl)

def verifyTopLevelDeclarations(ctx: Context, node: Node):
    for decl in node.children:
        verify(ctx, decl)

def verifyImmutableVariable(ctx: Context, node: Node):
    if ctx.has_name_in_current_scope(node.name):
        raise TypeError(f"{node.name} already been declared")
    variable_type = node.children[0]
    ctx.set_immutable_variable_type(node.name, variable_type)
    expression_type = verify(ctx, node.children[1])
    if expression_type != variable_type:
        raise TypeError(f"Variable {node.name} has type {variable_type} but it was given {expression_type}")

def verifyMutableVariable(ctx: Context, node: Node):
    if ctx.has_name_in_current_scope(node.name):
        raise TypeError(f"{node.name} already been declared")
    variable_type = node.children[0]
    ctx.set_mutable_variable_type(node.name, variable_type)
    expression_type = verify(ctx, node.children[1])
    if expression_type != variable_type:
        raise TypeError(f"Variable {node.name} has type {variable_type} but it was given {expression_type}")

def verifyAssign(ctx: Context, node: Node):
    expression_type = verify(ctx, node.children[0])
    ctx.check_assign(node.name, expression_type)

def verifyIndex(ctx: Context, node: Node):
    index_type = verify(ctx, node.child[0])
    if not isinstance(index_type, IntType):
        raise TypeError(f"The index can only be an integer")
    return ctx.get_type(node.array)

def verifyNotOp(ctx: Context, node: Node):
    child_type = verify(ctx, node.children[0])
    if not isinstance(child_type, BooleanType):
        raise TypeError(f"Operation not can only be applied to boolean types")
    return child_type

def verifyUnaryOp(ctx: Context, node: Node):
    child_type = verify(ctx, node.children[0])
    if not isinstance(child_type, IntType) and not isinstance(child_type, FloatType) and not isinstance(child_type, DoubleType):
        raise TypeError(f"Unary operation can only be applied to numeric types")
    return child_type

def verifyBinaryOp(ctx: Context, node: Node):
    left_type = verify(ctx, node.children[0])
    right_type = verify(ctx, node.children[1])
    if left_type != right_type:
        raise TypeError(f"Operation {node.op} can only be applied to the same types")
    operation = node.op
    if operation in ['+', '-', '*', '/', '^', '%']:
        if not isinstance(left_type, IntType) and not isinstance(left_type, FloatType) and not isinstance(left_type, DoubleType):
            raise TypeError(f"Operation {operation} can only be applied to numeric types")
        return left_type
    elif operation in ['<', '>', '<=', '>=', '=', '!=', '&&', '||']:
        return BooleanType()

def verifyFunction(ctx: Context, node: Node):
    function_name = node.name
    parameters_list = node.children[0] 
    verify(ctx, parameters_list) # verify parameters
    return_type = node.children[1] # verify return
    t = ctx.check_if_function_name_exists(function_name, parameters_list.children, return_type)
    if len(node.children) == 3:
        ctx.set_function_signature_in_scope(function_name, parameters_list.children, return_type)
        ctx.enter_scope()
        verify(ctx, node.children[2]) # verify block
        ctx.exit_scope()
    else:
        if isinstance(t, FunctionDeclarationSignature):
            raise TypeError(f"Function {function_name} already been declared")
        ctx.set_function_declaration_signature_in_scope(function_name, parameters_list.children, return_type)
    
def verifyParameterList(ctx: Context, node: Node):
    value_counts = {}
    for par in node.children:
        if par.name in value_counts:
            raise TypeError(f"Parameter with name {par.name} already been declared")
        else:
            value_counts[par.name] = 1

def verifyIf(ctx: Context, node: Node):
    condition_type = verify(ctx, node.children[0])
    if condition_type != BooleanType():
        raise TypeError(f"If condition must be boolean")
    verify(ctx, node.children[1])
    if len(node.children) == 3:
        verify(ctx, node.children[2])

def verifyElseIf(ctx: Context, node: Node):
    condition_type = verify(ctx, node.children[0])
    if condition_type != BooleanType():
        raise TypeError(f"Else if condition must be boolean")
    verify(ctx, node.children[1])
    if len(node.children) == 3:
        verify(ctx, node.children[2])

def verifyElse(ctx: Context, node: Node):
    verify(ctx, node.children[0])

def verifyWhile(ctx: Context, node: Node):
    condition_type = verify(ctx, node.children[0])
    if condition_type != BooleanType():
        raise TypeError(f"While condition must be boolean")
    verify(ctx, node.children[1])
    
def verifyBlock(ctx: Context, node: Node):
    ctx.enter_scope()
    for st in node.children:
        verify(ctx, st)
    ctx.exit_scope()
    
def verifyIdentifier(ctx: Context, node: Node):
    value = node.value
    if not ctx.has_variable(value):
        raise TypeError(f"Variable {value} is not in context")
    return ctx.get_type(value).type

def verifyFunctionCall(ctx: Context, node: Node):
    arguments = verify(ctx, node.children[0])
    return ctx.check_function_call(node.name, arguments)

def verifyArgumentsList(ctx: Context, node: Node):
    return [verify(ctx, arg) for arg in node.children]

## Verify Literal Types

def verifyIntLiteral():
    return IntType()

def verifyBooleanLiteral():
    return BooleanType()

def verifyDoubleLiteral():
    return DoubleType()

def verifyStringLiteral():
    return StringType()

def verifyCharLiteral():
    return CharType()

def verifyFloatLiteral():
    return FloatType()