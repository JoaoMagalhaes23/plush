from node import ProgramNode, Statement, Type, Expression, MutableVariable, ImmutableVariable, Assign, Function, MutableParameter, ImmutableParameter, Block, If, While, BinaryOp, Group, UnaryOp, NotOp, IntType, DoubleType, StringType, BooleanType, CharType, FloatType, VoidType, ArrayType, IntLiteral, DoubleLiteral, StringLiteral, BooleanLiteral, CharLiteral, FloatLiteral, Identifier, AccessArray, ArrayLiteral, FunctionCall
from dataclasses import dataclass

@dataclass
class Variable:
    name: str

@dataclass
class String:
    plush_identifier: str
    llvm_id: str

@dataclass
class Array:
    plush_identifier: str
    llvm_id: str

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

    def enter_scope(self):
        self.stack.insert(0, {})
    
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

    def set_global_array(self, n: str):
        v = f"@{n}"
        self.arrays[n] =  v 
        return v

    def check_if_is_global_scope(self):
        return len(self.stack) == 1
        

def compiler(ast: ProgramNode, emitter: Emitter=None):
    emitter = Emitter()
    emitter.set_function(n="print_int", value=None)
    emitter.set_function(n="print_string", value=None)
    emitter.set_function(n="print_boolean", value=None)
    emitter.set_function(n="print_int_array", value=None)
    for stmt in ast.statements:
        compiler_stmt(node=stmt, emitter=emitter)
    emitter << "declare void @print_int(i32)"
    emitter << "declare void @print_string(i8*)"
    emitter << "declare void @print_boolean(i1)"
    emitter << "declare void @print_int_array(i32*, i32)"
    emitter << "declare void @print_2d_int_array(i32**, i32, i32)"
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
    elif isinstance(node, If):
        return compile_if(node=node, emitter=emitter)
    elif isinstance(node, While):
        compile_while(node=node, emitter=emitter)
        
def compile_variable(node: MutableVariable|ImmutableVariable, emitter: Emitter):
    vname = node.name
    expr = compiler_expr(node=node.expression, emitter=emitter)
    v = emitter.set_variable(n=vname)
    _type = compiler_type(node=node.type, emitter=emitter).get("type")
    if v[0] == "@":
        emitter << f"{v} = unnamed_addr global {_type} {expr}"
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
    emitter.enter_scope()
    for stmt in node.statements:
        compiler_stmt(node=stmt, emitter=emitter)
    emitter.exit_scope()

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
    llvm_type = compiler_type(node=node.type, emitter=emitter).get("type")
    args = []
    for arg in node.arguments:
        expre = compiler_expr(node=arg, emitter=emitter)
        t = compiler_type(node=arg.type, emitter=emitter)
        _type = t.get("type") if arg.type is not ArrayType else t.get("type_pointer")
        args.append(f"{_type} {expre}")
    args_string = ", ".join(args)
    if llvm_type == "void":
        emitter << f"{SPACER}call {llvm_type} @{node.name}({args_string})"
    else:
        _id = emitter.get_id()
        emitter << f"{SPACER}{_id} = call {llvm_type} @{node.name}({args_string})"
        return _id

def compile_if(node: If, emitter: Emitter):
    cond = compiler_expr(node=node.condition, emitter=emitter)
    b1 = f"if.then{emitter.get_count()}"
    end = f"if.end{emitter.get_count()}"
    b2 = end if node.b2 is None else f"if.else{emitter.get_count()}"
    emitter << f"{SPACER}br i1 {cond}, label %{b1}, label %{b2}"
    emitter << f"{b1}:"
    compiler_stmt(node=node.b1, emitter=emitter)
    emitter << f"{SPACER}br label %{end}"
    if node.b2 is not None:
        emitter << f"{b2}:"
        compiler_stmt(node=node.b2, emitter=emitter)
        emitter << f"{SPACER}br label %{end}"
    emitter << f"{end}:"

def compile_while(node: While, emitter: Emitter):
    cond_label = f"while.cond{emitter.get_count()}"
    code_while_body = f"while.body{emitter.get_count()}"
    code_while_end = f"while.end{emitter.get_count()}"
    emitter << f"{SPACER}br label %{cond_label}"
    emitter << f"{cond_label}:"
    expre = compiler_expr(node=node.condition, emitter=emitter)
    emitter << f"{SPACER}br i1 {expre}, label %{code_while_body}, label %{code_while_end}"
    emitter << f"{code_while_body}:"
    compiler_stmt(node=node.block, emitter=emitter)
    emitter << f"{SPACER}br label %{cond_label}"
    emitter << f"{code_while_end}:"
    
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
    if isinstance(node, ArrayType):
        _type = compiler_type(node=node.subtype, emitter=emitter).get("type")
        return {"type": f"{_type}*"}
        
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
    elif isinstance(node, FunctionCall):
        return compile_function_call(node=node, emitter=emitter)
    elif isinstance(node, ArrayLiteral):
        return compile_array_literal(node=node, emitter=emitter)
    elif isinstance(node, BinaryOp):
        return compile_binary_op(node=node, emitter=emitter)
    elif isinstance(node, Group):
        return compile_group(node=node, emitter=emitter)
    elif isinstance(node, UnaryOp):
        return compile_unary_op(node=node, emitter=emitter)
    elif isinstance(node, NotOp):
        return compile_not_op(node=node, emitter=emitter)
    
def compile_string_literal(node: StringLiteral, emitter: Emitter):
    string_name = f"@.str.{emitter.get_count()}"
    _type = f"[{len(node.value)+1} x i8]"
    s = f"{string_name} = private unnamed_addr global {_type} c\"{node.value}\\00\""
    emitter.lines.insert(0, s)
    return f"getelementptr inbounds ({_type}, {_type}* {string_name}, i64 0, i64 0)"

def compile_array_literal(node: ArrayLiteral, emitter: Emitter):
    if emitter.check_if_is_global_scope():    
        elements = []
        for i in range(len(node.elements)):
            elem = compiler_expr(node=node.elements[i], emitter=emitter)
            elem_type = compiler_type(node=node.elements[i].type, emitter=emitter).get("type")
            elements.append(f"{elem_type} {elem}")
        elems_string = ", ".join(elements)
        array_id = f"@.array{emitter.get_count()}"
        array_type = f"[{len(node.elements)} x {elem_type}]"
        emitter.lines.append(f"{array_id} = global {array_type} [{elems_string}]")
        return f"getelementptr inbounds ({array_type}, {array_type}* {array_id}, i64 0, i64 0)"
    else: 
        array_id = f"array{emitter.get_count()}"
        subtype_type = compiler_type(node=node.type.subtype, emitter=emitter).get("type")
        emitter << f"{SPACER}%{array_id} = alloca {subtype_type}, i32 {len(node.elements)}"
        index = 0
        for node in node.elements:
            elem = compiler_expr(node=node, emitter=emitter)
            index_id = f"%{array_id}.index{index}"
            emitter << f"{SPACER}{index_id} = getelementptr inbounds {subtype_type}, {subtype_type}* %{array_id}, i32 {index}"
            emitter << f"{SPACER}store {subtype_type} {elem}, {subtype_type}* {index_id}"
            index+=1
        array_ptr = f"array{emitter.get_count()}ptr"
        emitter << f"{SPACER}%{array_ptr} = getelementptr inbounds {subtype_type}, {subtype_type}* %{array_id}, i32 0"
        return f"%{array_ptr}"
    
    
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
    