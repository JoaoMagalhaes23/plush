from node import *

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

    def has_var(self, name):
        for scope in self.stack:
            if name in scope:
                return True
        return False

    def has_var_in_current_scope(self, name):
        return name in self.stack[0]

    def enter_scope(self):
        self.stack.insert(0, {})

    def exit_scope(self):
        self.stack.pop(0)

literalToType = {
    IntLiteral:     IntType,
    DoubleLiteral:  DoubleType,
    StringLiteral:  StringType,
    BooleanLiteral: BooleanType,
    CharLiteral:    CharType,
    FloatLiteral:   FloatType
}

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
    elif isinstance(node, Function):
        return verifyFunction(ctx, node)
    elif isinstance(node, ParameterList):
        return verifyParameterList(ctx, node)
    elif isinstance(node, UnaryOp):
        return verifyUnaryOp(ctx, node)
    elif isinstance(node, BinaryOp):
        return verifyBinaryOp(ctx, node)
    elif isinstance(node, If):
        return verifyIf(ctx, node)
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
    else:
        raise TypeError(f"Node {node} nao reconhecido")
        
def verifyProgramNode(ctx: Context, node: Node):
    for decl in node.children:
        verify(ctx, decl)

def verifyTopLevelDeclarations(ctx: Context, node: Node):
    for decl in node.children:
        verify(ctx, decl)

def verifyImmutableVariable(ctx: Context, node: Node):
    if ctx.has_var_in_current_scope(node.name):
        raise TypeError(f"Variavel {node.name} ja foi declarada")
    variable_type = node.children[0]
    ctx.set_type(node.name, variable_type)
    if len(node.children) > 1:
        expression_type = verify(ctx, node.children[1])
        if expression_type != variable_type:
            raise TypeError(f"Variavel {node.name} tem tipo {variable_type} mas foi atribuido {expression_type}")
    
def verifyMutableVariable(ctx: Context, node: Node):
    if ctx.has_var_in_current_scope(node.name):
        raise TypeError(f"Variavel {node.name} foi declarada")
    variable_type = node.children[0]
    ctx.set_type(node.name, variable_type)
    if len(node.children) > 1:
        expression_type = verify(ctx, node.children[1])
        if expression_type != variable_type:
            raise TypeError(f"Variavel {node.name} tem tipo {variable_type} mas foi atribuido {expression_type}")

def verifyAssign(ctx: Context, node: Node):
    if not ctx.has_var(node.name):
        raise TypeError(f"Variavel {node.name} nao foi declarada")
    ctx.set_type(node.name, node.children[0])

def verifyUnaryOp(ctx: Context, node: Node):
    if ctx.has_var(node.children[0]):
        return ctx.get_type(node.children[0])
    if not isinstance(node.children[0], IntLiteral):
        raise TypeError(f"Operacao {node.op} so pode ser aplicada a inteiros")
    return IntType()

def verifyBinaryOp(ctx: Context, node: Node):
    left_type = verify(ctx, node.children[0])
    right_type = verify(ctx, node.children[1])
    if left_type != right_type:
        raise TypeError(f"Operacao {node.op} so pode ser aplicada a operandos do mesmo tipo")
    return left_type

def verifyIdentifier(ctx: Context, node: Node):
    value = node.value
    if not ctx.has_var(value):
        raise TypeError(f"Variavel {value} nao foi declarada")
    return ctx.get_type(value)

def verifyFunction(ctx: Context, node: Node):
    ctx.enter_scope()
    function_name = node.name
    if ctx.has_var(function_name):
        raise TypeError(f"Funcao {function_name} ja esta definida")
    verify(ctx, node.children[0]) # verify parameters
    return_type = node.children[1] # verify return
    ctx.set_type(function_name, return_type)
    verify(ctx, node.children[2]) # verify block
    ctx.exit_scope()
    
def verifyParameterList(ctx: Context, node: Node):
    for par in node.children:
        verify(ctx, par)

def verifyIf(ctx: Context, node: Node):
    condition_type = verify(ctx, node.children[0])
    if condition_type != BooleanType():
        raise TypeError(f"Condicao do if deve ser booleana")
    verify(ctx, node.children[1])
    if len(node.children) == 3:
        verify(ctx, node.children[2])

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