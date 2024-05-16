from node import ProgramNode, Statement, Type, Expression, MutableVariable, ImmutableVariable, Assign, AssignArray, Function, MutableParameter, ImmutableParameter, Block, If, While, BinaryOp, Group, UnaryOp, NotOp, IntType, StringType, BooleanType, CharType, FloatType, VoidType, ArrayType, IntLiteral, StringLiteral, BooleanLiteral, CharLiteral, FloatLiteral, Identifier, AccessArray, ArrayLiteral, FunctionCall
from dataclasses import dataclass

@dataclass
class Variable:
    name: str

@dataclass
class Func:
    name: any

SPACER = "   "   
class Emitter(object):
    def __init__(self):
        self.count = 0
        self.strings_counter = 0
        self.arrays_counter = 0
        self.lines = []
        self.stack = [{}]

    def enter_scope(self):
        self.stack.insert(0, {"_": self.count})
        self.count = 0
    
    def exit_scope(self):
        self.count = self.stack.pop(0)["_"]
        
    def get_count(self):
        self.count += 1
        return self.count

    def get_id(self):
        new_id = self.get_count()
        return f"%x{new_id}"

    def get_string_counter(self):
        self.strings_counter += 1
        return self.strings_counter
    
    def get_array_counter(self):
        self.arrays_counter += 1
        return self.arrays_counter

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
    
    def set_parameter(self, n: str):
        scope = self.stack[0]
        _id = f"%{n}.addr"
        scope[n] = Variable(name=_id)
        return _id
    
    def set_function(self, n: str):
        scope = self.stack[0]
        scope[n] = Func(name="%retval")
        return "%retval"

    def check_if_is_global_scope(self):
        return len(self.stack) == 1
        

def compiler(ast: ProgramNode, emitter: Emitter=None):
    emitter = Emitter()
    for stmt in ast.statements:
        compiler_stmt(node=stmt, emitter=emitter)
    emitter << "declare void @print_int(i32)"
    emitter << "declare void @print_string(i8*)"
    emitter << "declare void @print_boolean(i1)"
    emitter << "declare void @print_float(float)"
    emitter << "declare void @print_int_array(i32*, i32)"
    emitter << "declare void @print_2d_int_array(i32**, i32, i32)"
    emitter << "declare i8* @concatenate_strings(i8*, i8*)"
    emitter << "declare i8* @int_to_string(i32)"
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
    elif isinstance(node, AssignArray):
        return compile_assign_array(node=node, emitter=emitter)

def compile_variable(node: MutableVariable|ImmutableVariable, emitter: Emitter):
    expr = compiler_expr(node=node.expression, emitter=emitter)
    v = emitter.set_variable(n=node.name)
    _type = compiler_type(node=node.type, emitter=emitter)
    if v[0] == "@":
        emitter << f"{v} = unnamed_addr global {_type} {expr}"
    else:
        emitter << f"{SPACER}{v} = alloca {_type}"
        emitter << f"{SPACER}store {_type} {expr}, {_type}* {v}"

def compile_function(node: Function, emitter: Emitter):
    _type = compiler_type(node=node.return_type, emitter=emitter)
    emitter.enter_scope()
    parameters=[]
    for par in node.parameters:
        result = compiler_stmt(node=par, emitter=emitter)
        parameters.append(result)
    parameters_string = ", ".join(f"{element.get('type')} {element.get('llvm_name')}" for element in parameters)
    emitter << f"define {_type} @{node.name}({parameters_string}) {{"
    emitter << "entry:"
    if _type != "void":
        emitter << f"{SPACER}%retval = alloca {_type}"
    emitter.set_function(n=node.name)
    for p in parameters:
        llvm_name = emitter.set_parameter(n=p.get('name'))
        emitter << f"{SPACER}{llvm_name} = alloca {p.get('type')}"
        emitter << f"{SPACER}store {p.get('type')} {p.get('llvm_name')}, {p.get('type')}* {llvm_name}"
    compiler_stmt(node=node.block, emitter=emitter)
    return_id = emitter.get_id()
    if _type != "void":
        emitter << f"{SPACER}{return_id} = load {_type}, {_type}* %retval"
        emitter << f"{SPACER}ret {_type} {return_id}"
    else:
        emitter << f"{SPACER}ret void"
    emitter << "}"
    emitter.exit_scope()
    
def compile_parameter(node: MutableParameter|ImmutableParameter, emitter: Emitter):
    _type = compiler_type(node=node.type, emitter=emitter)
    return {"type": _type, "llvm_name": f"%{node.name}", "name": node.name}

def compile_block(node: Block, emitter: Emitter):
    for stmt in node.statements:
        compiler_stmt(node=stmt, emitter=emitter)

def compile_assign(node: Assign, emitter: Emitter):
    variable = emitter.get_obj(n=node.variable).name
    expr = compiler_expr(node=node.expression, emitter=emitter)
    _type = compiler_type(node=node.type, emitter=emitter)
    emitter << f"{SPACER}store {_type} {expr}, {_type}* {variable}"

def compile_assign_array(node: AssignArray, emitter: Emitter):
    expr = compiler_expr(node=node.expression, emitter=emitter)
    _type = compiler_type(node=node.type, emitter=emitter)
    array = compiler_expr(node=node._array, emitter=emitter)
    emitter << f"{SPACER}store {_type} {expr}, {_type}* {array}"

def compile_function_call(node: FunctionCall, emitter: Emitter):
    llvm_type = compiler_type(node=node.type, emitter=emitter)
    args = []
    for arg in node.arguments:
        expre = compiler_expr(node=arg, emitter=emitter)
        _type = compiler_type(node=arg.type, emitter=emitter)
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
        return "i32"
    if isinstance(node, FloatType):
        return "float"
    if isinstance(node, CharType):
        return "i8"
    if isinstance(node, BooleanType):
        return "i1"
    if isinstance(node, StringType):
        return "i8*" 
    if isinstance(node, VoidType):
        return "void"
    if isinstance(node, ArrayType):
        _type = compiler_type(node=node.subtype, emitter=emitter)
        return f"{_type}*"

import struct
def float_to_hex(f: float):
    return hex(struct.unpack('<Q', struct.pack('<d', f))[0])

def compiler_expr(node: Expression, emitter: Emitter):
    if isinstance(node, IntLiteral):
        return node.value
    elif isinstance(node, FloatLiteral):
        return float_to_hex(float(node.value))
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
    elif isinstance(node, AccessArray):
        return compile_access_array(node=node, emitter=emitter) 
    
def compile_string_literal(node: StringLiteral, emitter: Emitter):
    string_name = f"@.str.{emitter.get_string_counter()}"
    _type = f"[{len(node.value)+1} x i8]"
    s = f"{string_name} = private unnamed_addr global {_type} c\"{node.value}\\00\""
    emitter.lines.insert(0, s)
    return f"getelementptr inbounds ({_type}, {_type}* {string_name}, i64 0, i64 0)"

def compile_array_literal(node: ArrayLiteral, emitter: Emitter):
    elements = []
    for i in range(len(node.elements)):
        elem = compiler_expr(node=node.elements[i], emitter=emitter)
        elem_type = compiler_type(node=node.elements[i].type, emitter=emitter)
        elements.append(f"{elem_type} {elem}")
    elems_string = ", ".join(elements)
    array_id = f"@.array{emitter.get_array_counter()}"
    array_type = f"[{len(node.elements)} x {elem_type}]"
    emitter.lines.insert(0, f"{array_id} = global {array_type} [{elems_string}]")
    return f"getelementptr inbounds ({array_type}, {array_type}* {array_id}, i64 0, i64 0)"
        
def compile_identifier(node: Identifier, emitter: Emitter):
    obj = emitter.get_obj(n=node.id)
    _type = compiler_type(node=node.type, emitter=emitter)
    _id = emitter.get_id()
    emitter << f"{SPACER}{_id} = load {_type}, {_type}* {obj.name}"
    return _id

def compile_binary_op(node: BinaryOp, emitter: Emitter):
    left = compiler_expr(node=node.left_expression, emitter=emitter)
    right = compiler_expr(node=node.right_expression, emitter=emitter)
    _type = compiler_type(node=node.left_expression.type, emitter=emitter)
    _id = emitter.get_id()
    emitter << f"{SPACER}{_id} = {get_llvm_function(node.op)} {_type} {left}, {right}"
    return _id

def compile_group(node: Group, emitter: Emitter):
    return compiler_expr(node=node.expression, emitter=emitter)

def compile_unary_op(node: UnaryOp, emitter: Emitter):
    if isinstance(node.expression, FloatLiteral) or isinstance(node.expression, IntLiteral):
        node.expression.value = -node.expression.value
        return compiler_expr(node=node.expression, emitter=emitter)
    else:    
        expr = compiler_expr(node=node.expression, emitter=emitter)
        _id = emitter.get_id()
        emitter << f"{SPACER}{_id} = sub i32 0, {expr}"
        return _id

def compile_not_op(node: NotOp, emitter: Emitter):
    expr = compiler_expr(node=node.expression, emitter=emitter)
    _id = emitter.get_id()
    emitter << f"{SPACER}{_id} = xor i1 {expr}, true"
    return _id

def compile_access_array(node: AccessArray, emitter: Emitter):
    llvm_name = emitter.get_obj(n=node.array).name
    _type = node.array_type
    for index in node.indexes:
        index = compiler_expr(node=index, emitter=emitter)
        _sub_type = compiler_type(node=_type, emitter=emitter)
        _id = emitter.get_id()
        emitter << f"{SPACER}{_id} = load {_sub_type}, {_sub_type}* {llvm_name}"
        llvm_name = _id
        _type = _type.subtype
    index_ptr = f"%index.ptr{emitter.get_count()}"
    t = compiler_type(node=_type, emitter=emitter)
    emitter << f"{SPACER}{index_ptr} = getelementptr inbounds {t}, {t}* {llvm_name}, i32 {index}"
    if node.assigned:
        return index_ptr
    else:
        arrayidx = f"%arrayidx{emitter.get_count()}"
        emitter << f"{SPACER}{arrayidx} = load {t}, {t}* {index_ptr}"
        return arrayidx

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

def get_default_value(type: Type):
    if isinstance(type, IntType):
        return 0
    elif isinstance(type, FloatType):
        return 0.0
    elif isinstance(type, CharType):
        return 0
    elif isinstance(type, BooleanType):
        return 0
    elif isinstance(type, StringType):
        return "null"
    elif isinstance(type, ArrayType):
        return "null"
    elif isinstance(type, VoidType):
        return None
    return None 
