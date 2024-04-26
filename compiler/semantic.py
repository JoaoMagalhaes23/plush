from node import *
from dataclasses import dataclass

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
        raise TypeError(f"Variavel {name} nao esta no contexto")
    
    def set_type(self, name, value):
        scope = self.stack[0]
        scope[name] = value
    
    def set_function_type(self, name, parameters, return_type):
        scope = self.stack[0]
        scope[name] = FunctionSignature(parameters, return_type)
    
    def set_mutable_variable_type(self, name, type):
        scope = self.stack[0]
        scope[name] = MutableVariableDefinition(type)
    
    def set_immutable_variable_type(self, name, type):
        scope = self.stack[0]
        scope[name] = ImmutableVariableDefinition(type)

    def has_var(self, name):
        for scope in self.stack:
            temp = scope.get(name)
            if isinstance(temp, MutableVariableDefinition) or isinstance(temp, ImmutableVariableDefinition):
                return True
        return False
    
    def has_function(self, name):
        for scope in self.stack:
            temp = scope.get(name)
            if name in scope:
                if isinstance(temp, FunctionSignature):
                    return True
        return False

    def has_mutable_var(self, name):
        for scope in self.stack:
            temp = scope.get(name)
            if isinstance(temp, MutableVariableDefinition):
                return True
            if isinstance(temp, ImmutableVariableDefinition):
                raise TypeError(f"Variavel {name} e imutavel")
            if isinstance(temp, FunctionSignature):
                raise TypeError(f"Variavel {name} e uma funcao")
        return False

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
    elif isinstance(node, ImmutableParameter):
        return verifyImmutableParameter(ctx, node)
    elif isinstance(node, MutableParameter):
        return verifyMutableParameter(ctx, node)
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
        raise TypeError(f"{node.name} já foi declarado")
    variable_type = node.children[0]
    ctx.set_immutable_variable_type(node.name, variable_type)
    expression_type = verify(ctx, node.children[1])
    if expression_type != variable_type:
        raise TypeError(f"Variavel {node.name} tem tipo {variable_type} mas foi atribuido {expression_type}")

def verifyMutableVariable(ctx: Context, node: Node):
    if ctx.has_name_in_current_scope(node.name):
        raise TypeError(f"{node.name} já foi declarado")
    variable_type = node.children[0]
    ctx.set_mutable_variable_type(node.name, variable_type)
    expression_type = verify(ctx, node.children[1])
    if expression_type != variable_type:
        raise TypeError(f"Variavel {node.name} tem tipo {variable_type} mas foi atribuido {expression_type}")

def verifyAssign(ctx: Context, node: Node):
    if not ctx.has_mutable_var(node.name):
        raise TypeError(f"Variavel {node.name} nao foi declarada")
    n = ctx.get_type(node.name)
    expression_type = verify(ctx, node.children[0])
    if expression_type != n.type:
        raise TypeError(f"Variavel {node.name} tem tipo {n.type} mas foi atribuido {expression_type}")

def verifyIndex(ctx: Context, node: Node):
    index_type = verify(ctx, node.child[0])
    if not isinstance(index_type, IntType):
        raise TypeError(f"Index so pode ser aplicado a tipos inteiros")
    return ctx.get_type(node.array)

def verifyNotOp(ctx: Context, node: Node):
    child_type = verify(ctx, node.children[0])
    if not isinstance(child_type, BooleanType):
        raise TypeError(f"Operacao not so pode ser aplicada a tipos booleanos")
    return child_type

def verifyUnaryOp(ctx: Context, node: Node):
    child_type = verify(ctx, node.children[0])
    if not isinstance(child_type, IntType) and not isinstance(child_type, FloatType) and not isinstance(child_type, DoubleType):
        raise TypeError(f"Operacao unária so pode ser aplicada a tipos numericos")
    return child_type

def verifyBinaryOp(ctx: Context, node: Node):
    left_type = verify(ctx, node.children[0])
    right_type = verify(ctx, node.children[1])
    if left_type != right_type:
        raise TypeError(f"Operacao {node.op} so pode ser aplicada a operandos do mesmo tipo")
    operation = node.op
    if operation in ['+', '-', '*', '/', '^', '%']:
        if not isinstance(left_type, IntType) and not isinstance(left_type, FloatType) and not isinstance(left_type, DoubleType):
            raise TypeError(f"Operacao {operation} so pode ser aplicada a tipos numericos")
        return left_type
    elif operation in ['<', '>', '<=', '>=', '=', '!=', '&&', '||']:
        return BooleanType()

def verifyIdentifier(ctx: Context, node: Node):
    value = node.value
    if not ctx.has_var(value):
        raise TypeError(f"Variavel {value} nao foi declarada")
    return ctx.get_type(value)

def verifyFunction(ctx: Context, node: Node):
    ctx.enter_scope()
    function_name = node.name
    if ctx.has_function(function_name):
        raise TypeError(f"Funcao {function_name} ja esta definida")
    parameters = node.children[0] 
    verify(ctx, parameters) # verify parameters
    return_type = node.children[1] # verify return
    ctx.set_function_type(function_name, parameters, return_type)
    if len(node.children) == 3:
        verify(ctx, node.children[2]) # verify block
    ctx.exit_scope()
    
def verifyParameterList(ctx: Context, node: Node):
    for par in node.children:
        verify(ctx, par)

def verifyImmutableParameter(ctx: Context, node: Node):
    par_name = node.name
    par_type = node.child
    if ctx.has_var(par_name):
        raise TypeError(f"Parametro {par_name} ja foi declarado")
    ctx.set_type(par_name, par_type)
    
def verifyMutableParameter(ctx: Context, node: Node):
    par_name = node.name
    par_type = node.child
    if ctx.has_var(par_name):
        raise TypeError(f"Parametro {par_name} ja foi declarado")
    ctx.set_type(par_name, par_type)

def verifyIf(ctx: Context, node: Node):
    condition_type = verify(ctx, node.children[0])
    if condition_type != BooleanType():
        raise TypeError(f"Condicao do if deve ser booleana")
    verify(ctx, node.children[1])
    if len(node.children) == 3:
        verify(ctx, node.children[2])

def verifyElseIf(ctx: Context, node: Node):
    condition_type = verify(ctx, node.children[0])
    if condition_type != BooleanType():
        raise TypeError(f"Condicao do else if deve ser booleana")
    verify(ctx, node.children[1])
    if len(node.children) == 3:
        verify(ctx, node.children[2])

def verifyElse(ctx: Context, node: Node):
    verify(ctx, node.children[0])

def verifyWhile(ctx: Context, node: Node):
    condition_type = verify(ctx, node.children[0])
    if condition_type != BooleanType():
        raise TypeError(f"Condicao do while deve ser booleana")
    verify(ctx, node.children[1])
    
def verifyBlock(ctx: Context, node: Node):
    ctx.enter_scope()
    for st in node.children:
        verify(ctx, st)
    ctx.exit_scope()
    
def verifyIdentifier(ctx: Context, node: Node):
    value = node.value
    if not ctx.has_var(value):
        raise TypeError(f"Variavel {value} nao foi declarada")
    return ctx.get_type(value)

def verifyFunctionCall(ctx: Context, node: Node):
    function_name = node.name
    if not ctx.has_function(function_name):
        raise TypeError(f"Funcao {function_name} nao foi definida")
    function_type = ctx.get_type(function_name)
    if not isinstance(function_type, Function):
        raise TypeError(f"Variavel {function_name} nao e uma funcao")
    parameters = node.children
    if len(parameters) != len(function_type.parameters):
        raise TypeError(f"Numero de parametros incorreto")
    for i in range(len(parameters)):
        par_type = verify(ctx, parameters[i])
        if par_type != function_type.parameters[i]:
            raise TypeError(f"Parametro {i} tem tipo {par_type} mas deveria ser {function_type.parameters[i]}")
    return function_type.return_type

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