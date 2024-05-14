from node import *

class Context(object):
    def __init__(self):
        self.stack = [{}]

    def set(self, name, value):
        self.stack[-1][name] = value

    def get(self, name):
        for scope in self.stack[::-1]:
            if name in scope:
                return scope[name]
        raise Exception("Variavel {} nao encontrada".format(name))

    def get_function(self, name):
        scope = self.stack[0]
        func = scope.get(name)
        return func
    
    def enter_scope(self):
        self.stack.append({})

    def exit_scope(self):
        self.stack.pop() 

def interpreter(ctx: Context, ast: ProgramNode):
    ctx.enter_scope()
    for stmt in ast.statements:
        interpret_statement(ctx=ctx, stmt=stmt)
    ctx.exit_scope()

def interpret_statement(ctx: Context, stmt: Statement):
    if isinstance(stmt, MutableVariable) or isinstance(stmt, ImmutableVariable):
        value = interpret_expression(ctx=ctx, expression=stmt.expression, type=stmt.type)
        ctx.set(stmt.name, value)
    elif isinstance(stmt, If):
        if interpret_expression(ctx=ctx, expression=stmt.condition, type=stmt.type):
            interpret_statement(ctx=ctx, stmt=stmt.b1)
        else:
            if stmt.b2 is not None:
                interpret_statement(ctx=ctx, stmt=stmt.b2)
    elif isinstance(stmt, While):
        while interpret_expression(ctx=ctx, expression=stmt.condition, type=stmt.type):
            interpret_statement(ctx=ctx, stmt=stmt.block)
    elif isinstance(stmt, Function):
        ctx.set(stmt.name, stmt) 
    elif isinstance(stmt, FunctionCall):
        pass
    
def interpret_expression(ctx: Context, expression: Expression, type: Type):
    if isinstance(expression, IntLiteral):
        return int(expression.value)
    elif isinstance(expression, BooleanLiteral):
        return True if expression.value == "true" else False
    elif isinstance(expression, DoubleLiteral):
        return float(expression.value)
    elif isinstance(expression, StringLiteral):
        return str(expression.value)
    elif isinstance(expression, CharLiteral):
        return chr(expression.value)
    elif isinstance(expression, FloatLiteral):
        return float(expression.value)
    elif isinstance(expression, ArrayLiteral):
        return [interpret_expression(ctx, expr, type) for expr in expression.expressions]
    elif isinstance(expression, BinaryOp):
        if expression.operator == "+":
            return interpret_expression(ctx, expression.left, type) + interpret_expression(ctx, expression.right, type)
        elif expression.operator == "-":
            return interpret_expression(ctx, expression.left, type) - interpret_expression(ctx, expression.right, type)
        elif expression.operator == "*":
            return interpret_expression(ctx, expression.left, type) * interpret_expression(ctx, expression.right, type)
        elif expression.operator == "/":
            return interpret_expression(ctx, expression.left, type) / interpret_expression(ctx, expression.right, type)
        elif expression.operator == "%":
            return interpret_expression(ctx, expression.left, type) % interpret_expression(ctx, expression.right, type)
        elif expression.operator == "^":
            return interpret_expression(ctx, expression.left, type) ** interpret_expression(ctx, expression.right, type)
        elif expression.operator == "=":
            return interpret_expression(ctx, expression.left, type) == interpret_expression(ctx, expression.right, type)
        elif expression.operator == "!=":
            return interpret_expression(ctx, expression.left, type) != interpret_expression(ctx, expression.right, type)
        elif expression.operator == ">":
            return interpret_expression(ctx, expression.left, type) > interpret_expression(ctx, expression.right, type)
        elif expression.operator == "<":
            return interpret_expression(ctx, expression.left, type) < interpret_expression(ctx, expression.right, type)
        elif expression.operator == ">=":
            return interpret_expression(ctx, expression.left, type) >= interpret_expression(ctx, expression.right, type)
        elif expression.operator == "<=":
            return interpret_expression(ctx, expression.left, type) <= interpret_expression(ctx, expression.right, type)
        elif expression.operator == "&&":
            return interpret_expression(ctx, expression.left, type) and interpret_expression(ctx, expression.right, type)
        elif expression.operator == "||":
            return interpret_expression(ctx, expression.left, type) or interpret_expression(ctx, expression.right, type)
    elif isinstance(expression, UnaryOp):
        return - interpret_expression(ctx, expression.expression, type)
    elif isinstance(expression, NotOp):
        return not interpret_expression(ctx, expression.expression, type)