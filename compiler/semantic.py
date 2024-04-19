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


def verify(ctx:Context, node: Node):
    if isinstance(node, ProgramNode):
        for decl in node.children:
            verify(ctx, decl)
    elif isinstance(node, TopLevelDeclarations):
        for decl in node.children:
            verify(ctx, decl)
    elif isinstance(node, ImmutableVariable):
        if ctx.has_var_in_current_scope(node.name):
            raise TypeError(f"Variavel {node.name} ja foi declarada")
        ctx.set_type(node.name, node.children[0])
    elif isinstance(node, MutableVariable):
        if ctx.has_var_in_current_scope(node.name):
            raise TypeError(f"Variavel {node.name} ja foi declarada")
        ctx.set_type(node.name, node.children[0])
    elif isinstance(node, Assign):
        if not ctx.has_var(node.name):
            raise TypeError(f"Variavel {node.name} nao foi declarada")
        ctx.set_type(node.name, node.children[0])
    elif isinstance(node, Function):
        ctx.enter_scope()
        for param in node.children[0].children:
            ctx.set_type(param.name, param.type)
        verify(ctx, node.children[2])
        ctx.exit_scope()
    elif isinstance(node, ParameterList):
        for param in node.children:
            verify(ctx, param)
    elif isinstance(node, Parameter):
        pass
    else:
        raise TypeError(f"Node {node} nao reconhecido")
        

