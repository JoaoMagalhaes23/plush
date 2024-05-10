from node import ProgramNode, Statement, Type, Expression, MutableVariable, ImmutableVariable, Assign, Function, MutableParameter, ImmutableParameter, Block, If, While, BinaryOp, Group, UnaryOp, NotOp, IntType, DoubleType, StringType, BooleanType, CharType, FloatType, VoidType, ArrayType, IntLiteral, DoubleLiteral, StringLiteral, BooleanLiteral, CharLiteral, FloatLiteral, Identifier, AccessArray, ArrayLiteral, FunctionCall
from dataclasses import dataclass

@dataclass
class Variable:
    name: str

@dataclass
class Func:
    name: str
    value: any

SPACER = "   "   
class Emitter(object):
    def __init__(self):
        self.count = 0
        self.lines = []
        self.stack = [{}]
        self.strings = {}

    def enter_scope(self):
        self.stack.append({})
    
    def exit_scope(self):
        self.stack.pop()
        
    def get_count(self):
        self.count += 1
        return self.count

    def get_id(self):
        new_id = self.get_count()
        return f"%x{new_id}"

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

    def set_string(self, value:str):
        v = f"@.str{self.get_count()}"
        self.strings[value] = v
        return v
    
    def get_string(self, value:str):
        if value in self.strings:
            return self.strings[value]
        else:
            return None
        

def compiler(ast: ProgramNode, emitter: Emitter=None):
    emitter = Emitter()
    emitter.set_function(n="print_int", value=None)
    emitter.set_function(n="print_string", value=None)
    emitter.set_function(n="print_boolean", value=None)
    for stmt in ast.statements:
        compiler_stmt(node=stmt, emitter=emitter)
    emitter << "declare void @print_int(i32)"
    emitter << "declare void @print_string(i8*)"
    emitter << "declare void @print_boolean(i1)"
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
    _type = compiler_type(node=node.type, emitter=emitter).get("type")
    v = emitter.set_variable(n=vname)
    if v[0] == "@":
        emitter << f"{v} = global {_type} {expr}"
    else:
        emitter << f"{SPACER}{v} = alloca {_type}"
        emitter << f"{SPACER}store {_type} {expr}, {_type}* {v}"

def compile_function(node: Function, emitter: Emitter):
    _dict = compiler_type(node=node.return_type, emitter=emitter)
    _type = _dict.get("type")
    function_name = emitter.set_function(n=node.name, value=_dict.get("default_value"))
    emitter.enter_scope()
    parameters=[]
    for par in node.parameters:
        result = compiler_stmt(node=par, emitter=emitter)
        parameters.append(result)
    parameters_string = ",".join(f"{element.get('type')} {element.get('name')}" for element in parameters)
    emitter << f"define {_type} {function_name}({parameters_string}) {{"
    emitter << "entry:"
    for p in parameters:
        _id = emitter.get_id()
        emitter << f"{SPACER}{_id} = alloca {p.get('type')}"
        emitter << f"{SPACER}store {p.get('type')} {p.get('name')}, {p.get('type')}* {_id}"
    compiler_stmt(node=node.block, emitter=emitter)
    emitter << f"{SPACER}ret {_type} {emitter.get_function_value(n=node.name)}"
    emitter << "}"
    emitter.exit_scope()
    
def compile_parameter(node: MutableParameter|ImmutableParameter, emitter: Emitter):
    pname = emitter.set_variable(n=node.name)
    _dict = compiler_type(node=node.type, emitter=emitter)
    _type = _dict.get("type")
    return {"type": _type, "name": pname}

def compile_block(node: Block, emitter: Emitter):
    for stmt in node.statements:
        compiler_stmt(node=stmt, emitter=emitter)

def compile_assign(node: Assign, emitter: Emitter):
    expr = compiler_expr(node=node.expression, emitter=emitter)
    _dict = compiler_type(node=node.type, emitter=emitter)
    _type = _dict.get("type")
    obj = emitter.get_obj(n=node.name)
    if isinstance(obj, Variable):
        emitter << f"{SPACER}store {_type} {expr}, {_type}* {obj.name}"
    else:
        emitter.set_function(n=node.name, value=expr)

def compile_function_call(node: FunctionCall, emitter: Emitter):
    function_name = emitter.get_obj(n=node.name).name
    llvm_type = compiler_type(node=node.type, emitter=emitter).get("type")
    args = []
    for arg in node.arguments:
        expre = compiler_expr(node=arg, emitter=emitter)
        _type = compiler_type(node=arg.type, emitter=emitter).get("type")
        args.append({"expre":expre, "type":_type})
    args_string = ",".join(f"{element.get('type')} {element.get('expre')}" for element in args)
    if llvm_type == "void":
        emitter << f"{SPACER}call {llvm_type} {function_name}({args_string})"
    else:
        emitter << f"{SPACER}{emitter.get_id()} = call {llvm_type} {function_name}({args_string})"
        
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
        return node.value
    elif isinstance(node, FloatLiteral):
        return node.value
    elif isinstance(node, BooleanLiteral):
        return node.value
    elif isinstance(node, StringLiteral):
        return compile_string_literal(node=node, emitter=emitter)
    elif isinstance(node, CharLiteral):
        return node.value
    elif isinstance(node, Identifier):
        return compile_identifier(node=node, emitter=emitter)
    elif isinstance(node, BinaryOp):
        return compile_binary_op(node=node, emitter=emitter)
    elif isinstance(node, Group):
        return compile_group(node=node, emitter=emitter)
    elif isinstance(node, UnaryOp):
        return compile_unary_op(node=node, emitter=emitter)
    elif isinstance(node, NotOp):
        return compile_not_op(node=node, emitter=emitter)
    
def compile_string_literal(node: StringLiteral, emitter: Emitter):
    s = emitter.get_string(value=node.value)
    string_name = s if s is not None else emitter.set_string(value=node.value)
    _type = f"[{len(node.value)+1} x i8]"
    if s is None:
        s = f"{string_name} = private unnamed_addr constant {_type} c\"{node.value}\\00\""
        emitter.lines.insert(0, s)
    return f" getelementptr inbounds ({_type}, {_type}* {string_name}, i64 0, i64 0) "

def compile_identifier(node: Identifier, emitter: Emitter):
    obj = emitter.get_obj(n=node.id)
    _type = compiler_type(node=node.type, emitter=emitter).get("type")
    _id = emitter.get_id()
    emitter << f"{SPACER}{_id} = load {_type}, {_type}* {obj.name}"
    return _id

def compile_binary_op(node: BinaryOp, emitter: Emitter):
    left = compiler_expr(node=node.left_expression, emitter=emitter)
    right = compiler_expr(node=node.right_expression, emitter=emitter)
    _type = compiler_type(node=node.type, emitter=emitter).get("type")
    _id = emitter.get_id()
    emitter << f"{SPACER}{_id} = {get_llvm_function(node.op)} {_type} {left}, {right}"
    return _id

def compile_group(node: Group, emitter: Emitter):
    return compiler_expr(node=node.expression, emitter=emitter)

def compile_unary_op(node: UnaryOp, emitter: Emitter):
    expr = compiler_expr(node=node.expression, emitter=emitter)
    _id = emitter.get_id()
    emitter << f"{SPACER}{_id} = sub i32 0, {expr}"
    return _id

def compile_not_op(node: NotOp, emitter: Emitter):
    expr = compiler_expr(node=node.expression, emitter=emitter)
    _id = emitter.get_id()
    emitter << f"{SPACER}{_id} = xor i1 {expr}, true"
    return _id

def get_llvm_function(operation: str):
    if operation == "+":
        return "add"
    elif operation == "-":
        return "sub"
    elif operation == "*":
        return "mul"
    elif operation == "/":
        return "sdiv"
    elif operation == "%":
        return "srem"
    elif operation == "<":
        return "icmp slt"
    elif operation == ">":
        return "icmp sgt"
    elif operation == "<=":
        return "icmp sle"
    elif operation == ">=":
        return "icmp sge"
    elif operation == "=":
        return "icmp eq"
    elif operation == "!=":
        return "icmp ne"
    elif operation == "&&":
        return "and"
    elif operation == "||":
        return "or"
    elif operation == "^":
        return "xor"
    elif operation == "!":
        return "not"
    