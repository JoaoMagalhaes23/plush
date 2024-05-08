from node import *

@dataclass
class Variable:
    name: str

@dataclass
class Func:
    name: str
    value: any
    
class Emitter(object):
    def __init__(self):
        self.count = 0
        self.lines = []
        self.stack = [{}]

    def enter_scope(self):
        self.stack.append({})
    
    def exit_scope(self):
        self.stack.pop()
        
    def get_count(self):
        self.count += 1
        return self.count

    def get_id(self):
        id = self.get_count()
        return f"%x{id}"

    def __lshift__(self, v):
        self.lines.append(v)

    def get_code(self):
        return "\n".join(self.lines)
    
    def get_obj(self, n: str):
        for scope in self.stack:
            if n in scope:
                return scope[n] 
    
    def set_variable(self, n: str):
        scope = self.stack[0]
        if len(self.stack) == 1:
            scope[n] = Variable(name=f"@{n}")
            return f"@{n}"
        else:
            scope[n] =  Variable(name=f"%{n}")
            return f"%{n}"
    
    def set_function(self, n: str, value:any):
        scope = self.stack[0]
        scope[n] = Func(name=f"@{n}", value=value)
        return f"@{n}"
    
    def get_function_value(self, n: str):
        for scope in self.stack:
            if n in scope:
                return scope[n].value

def compiler(ast: ProgramNode, emitter:Emitter=None):
    emitter = Emitter()
    emitter.set_function(n="print_int", value=None)
    for stmt in ast.statements:
        compiler_stmt(node=stmt, emitter=emitter)
    emitter << "declare void @print_int(i32)"
    return emitter.get_code()

def compiler_stmt(node: Statement, emitter: Emitter):
    if isinstance(node, MutableVariable) or isinstance(node, ImmutableVariable):
        return compile_variable(node=node, emitter=emitter)
    elif isinstance(node, Function):
        return compile_function(node=node, emitter=emitter)
    elif isinstance(node, MutableParameter) or isinstance(node, ImmutableParameter):
        return compile_parameter(node=node, emitter=emitter)
    elif isinstance(node, Block):
        return compile_block(node=node, emitter=emitter)
    elif isinstance(node, Assign):
        return compile_assign(node=node, emitter=emitter)
    elif isinstance(node, FunctionCall):
        return compile_function_call(node=node, emitter=emitter)
        
def compile_variable(node: MutableVariable|ImmutableVariable, emitter: Emitter):
    vname = node.name
    expr = node.expression
    expr = compiler_expr(node=expr, emitter=emitter)
    type = compiler_type(node=node.type, emitter=emitter).get("type")
    v = emitter.set_variable(n=vname)
    if v[0] == "@":
        emitter << f"{v} = global {type} {expr}"
    else:
        emitter << f"   {v} = alloca {type}"
        emitter << f"   store {type} {expr}, {type}* {v}"

def compile_function(node: Function, emitter: Emitter):
    dict = compiler_type(node=node.return_type, emitter=emitter)
    type = dict.get("type")
    function_name = emitter.set_function(n=node.name, value=dict.get("default_value"))
    emitter.enter_scope()
    parameters=[]
    for par in node.parameters:
        result = compiler_stmt(node=par, emitter=emitter)
        parameters.append(result)
    parameters_string = ",".join(f"{element.get('type')} {element.get('name')}" for element in parameters)
    emitter << f"define {type} {function_name}({parameters_string}) {{"
    emitter << "entry:"
    for p in parameters:
        id = emitter.get_id()
        emitter << f"   {id} = alloca {p.get('type')}"
        emitter << f"   store {p.get('type')} {p.get('name')}, {p.get('type')}* {id}"
    compiler_stmt(node=node.block, emitter=emitter)
    emitter << f"   ret {type} {emitter.get_function_value(n=node.name)}"
    emitter << "}"
    emitter.exit_scope()
    
def compile_parameter(node: MutableParameter|ImmutableParameter, emitter: Emitter):
    pname = emitter.set_variable(n=node.name)
    dict = compiler_type(node=node.type, emitter=emitter)
    type = dict.get("type")
    return {"type": type, "name": pname}

def compile_block(node: Block, emitter: Emitter):
    for stmt in node.statements:
        compiler_stmt(node=stmt, emitter=emitter)

def compile_assign(node: Assign, emitter: Emitter):
    expr = compiler_expr(node=node.expression, emitter=emitter)
    dict = compiler_type(node=node.type, emitter=emitter)
    type = dict.get("type")
    obj = emitter.get_obj(n=node.name)
    if isinstance(obj, Variable):
        emitter << f"   store {type} {expr}, {type}* {obj.name}"
    else:
        emitter.set_function(n=node.name, value=expr)

def compile_function_call(node: FunctionCall, emitter: Emitter):
    function_name = emitter.get_obj(n=node.name).name
    llvm_type = compiler_type(node=node.type, emitter=emitter).get("type")
    args = []
    for arg in node.arguments:
        expre = compiler_expr(node=arg, emitter=emitter)
        type = compiler_type(node=arg.type, emitter=emitter).get("type")
        args.append({"expre":expre, "type":type})
    args_string = ",".join(f"{element.get('type')} {element.get('expre')}" for element in args)
    if llvm_type == "void":
        emitter << f"   call {llvm_type} {function_name}({args_string})"
    else:
        emitter << f"   {emitter.get_id()} = call {llvm_type} {function_name}({args_string})"
        
def compiler_type(node: Type, emitter: Emitter):  
    if isinstance(node, IntType):
        return {"type":"i32", "default_value": 0}
    if isinstance(node, FloatType):
        return {"type":"float", "default_value": 0}
    if isinstance(node, CharType):
        return {"type":"i8", "default_value": 0}
    if isinstance(node, BooleanType):
        return {"type":"i1", "default_value": "false"}
    if isinstance(node, StringType):
        return {"type":"i8*", "default_value": ""} 
    if isinstance(node, VoidType):
        return {"type": "void"}
        
def compiler_expr(node: Expression, emitter: Emitter):
    if isinstance(node, IntLiteral):
        return int(node.value)
    elif isinstance(node, Identifier):
        return compile_identifier(node=node, emitter=emitter)
    else:
        return compiler_expr(node, emitter)

def compile_identifier(node: Identifier, emitter: Emitter):
    #%7 = load i32, i32* %4, align 4
    obj = emitter.get_obj(n=node.id)
    type = compiler_type(node=node.type, emitter=emitter).get("type")
    id = emitter.get_id()
    emitter << f"   {id} = load {type}, {type}* {obj.name}"
    return id