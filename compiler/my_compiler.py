from node import *

class Emitter(object):
    def __init__(self):
        self.count = 0
        self.lines = []

    def get_count(self):
        self.count += 1
        return self.count

    def get_id(self):
        id = self.get_count()
        return f"cas_{id}"

    def __lshift__(self, v):
        self.lines.append(v)

    def get_code(self):
        return "\n".join(self.lines)

    def get_pointer_name(self, n: str):
        return f"%pont_{n}"
    
    def get_global_name(self, n: str):
        return f"@{n}"

def compiler(ast: ProgramNode, emitter:Emitter=None):
    emitter = Emitter()

    emitter << "declare i32 @printf(i8*, ...) #1"

    for stmt in ast.statements:
        compiler_stmt(node=stmt, emitter=emitter)
    return emitter.get_code()

def compiler_stmt(node: Statement, emitter: Emitter, indent: int = 0):
    if isinstance(node, MutableVariable) or isinstance(node, ImmutableVariable):
        compile_variable(node=node, emitter=emitter, indent=indent)
    if isinstance(node, Assign):
        compile_assign(node=node, emitter=emitter, indent=indent)
        
def compiler_type(node: Type, emitter: Emitter):  
    if isinstance(node, IntType):
        return "i32"
    if isinstance(node, FloatType):
        return "float"
    if isinstance(node, CharType):
        return "i8"
    if isinstance(node, BooleanType):
        return "i1"
    if isinstance(node, StringType):
        return "ptr" 

def compiler_expr(node: Expression, emitter: Emitter):
    if isinstance(node, IntLiteral):
        return int(node.value)
    else:
        return compiler_expr(node, emitter)

def compile_variable(node: MutableVariable|ImmutableVariable, emitter: Emitter, indent: int = 0):
    vname = node.name
    expr = node.expression
    expr = compiler_expr(node=expr, emitter=emitter)
    type = compiler_type(node=node.type, emitter=emitter)
    if indent != 0:
        pname = emitter.get_pointer_name(n=vname)
        emitter << '\t' * indent + f"{pname} = alloca {type}"
        emitter << '\t' * indent + f"store {type} {expr}, {type}* {pname}"
    else:
        emitter.get_global_name(n=vname)
        emitter << '\t' * indent + f"@{vname} = dso_local global {type} {expr}"

def compile_assign(node: Assign, emitter: Emitter, indent: int = 0):
    variable = emitter.get_pointer_name(n=node.name) if indent != 0 else emitter.get_global_name(n=node.name)
    expr = compiler_expr(node=node.expression, emitter=emitter)
    type = compiler_type(node=node.type, emitter=emitter)
    emitter << '\t' * indent + f"store {type} {expr}, ptr {variable}"

    # elif isinstance(ast, MutableVariable):
    #     vname = ast.name
    #     expr = ast.expression
    #     pname = emitter.get_pointer_name(vname)
    #     emitter << f"{pname} = alloca i32"
    #     emitter << f"store i32 {compiler(expr, emitter)}, i32* {pname}"
    # elif isinstance(ast, ImmutableVariable):
    #     vname = ast.name
    #     expr = ast.expression
    #     pname = emitter.get_pointer_name(vname)
    #     emitter << f"{pname} = alloca i32"
    #     emitter << f"store i32 {compiler(expr, emitter)}, i32* {pname}"
    # elif isinstance(ast, Function):
    #     pass
    # elif isinstance(ast, IntLiteral):
    #     return int(ast.value)
    # elif isinstance(ast, BooleanLiteral):
    #     return True if ast.value == "true" else False
    # elif isinstance(ast, DoubleLiteral):
    #     return float(ast.value)
    # elif isinstance(ast, StringLiteral):
    #     return str(ast.value)
    # elif isinstance(ast, CharLiteral):
    #     return chr(ast.value)
    # elif isinstance(ast, FloatLiteral):
    #     return float(ast.value)
    # elif isinstance(ast, ArrayLiteral):
    #     return [compiler(expr, emitter) for expr in ast.expressions]
    # elif isinstance(ast, BinaryOp):
    #     if ast.operator == "+":
    #         return compiler(ast.left, emitter) + compiler(ast.right, emitter)
    #     elif ast.operator == "-":
    #         return compiler(ast.left, emitter) - compiler(ast.right, emitter)
    #     elif ast.operator == "*":
    #         return compiler(ast.left, emitter) * compiler(ast.right, emitter)
    #     elif ast.operator == "/":
    #         return compiler(ast.left, emitter) / compiler(ast.right, emitter)
    #     elif ast.operator == "==":
    #         return compiler(ast.left, emitter) == compiler(ast.right, emitter)
    #     elif ast.operator == "!=":
    #         return compiler(ast.left, emitter) != compiler(ast.right, emitter)
    #     elif ast.operator == ">":
    #         return compiler(ast.left, emitter) > compiler(ast.right, emitter)
    #     elif ast.operator