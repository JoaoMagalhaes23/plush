from node import ProgramNode, Statement, Type, Expression, MutableVariable, ImmutableVariable, Assign, AssignArray, Function, MutableParameter, ImmutableParameter, Block, If, While, BinaryOp, Group, UnaryOp, NotOp, IntType, StringType, BooleanType, CharType, FloatType, VoidType, ArrayType, IntLiteral, StringLiteral, BooleanLiteral, CharLiteral, FloatLiteral, Identifier, AccessArray, ArrayLiteral, FunctionCall
from dataclasses import dataclass

@dataclass
class Variable:
    expression: any

@dataclass
class Func:
    function: Function
class Context(object):
    def __init__(self):
        self.stack = [{}]

    def set_variable(self, name, value):
        self.stack[-1][name] = Variable(expression=value)
    
    def set_function(self, name, function: Function):
        self.stack[0][name] = Func(function=function)

    def assign_new_value(self, name, value):
        for scope in self.stack[::-1]:
            if name in scope:
                scope[name] = Variable(expression=value)
                return
    
    def get_variable(self, name):
        for scope in self.stack[::-1]:
            if name in scope:
                return scope[name]

    def get_function(self, name):
        scope = self.stack[0]
        return scope.get(name)
    
    def enter_scope(self):
        self.stack.append({})

    def exit_scope(self):
        self.stack.pop() 

def interpreter(ctx: Context, ast: ProgramNode):
    for statement in ast.statements:
        if isinstance(statement, ImmutableVariable) or isinstance(statement, MutableVariable):
            ctx.set_variable(statement.name, interpreter_expression(ctx, statement.expression))
        if isinstance(statement, Function):
            ctx.set_function(statement.name, statement)
    main = ctx.get_function("main")
    if main is None:
        raise Exception("No main function")
    interpreter_statement(ctx, main.function)

def interpreter_statement(ctx: Context, stmt: Statement):
    if isinstance(stmt, Block):
        return interpreter_block(ctx, stmt)
    elif isinstance(stmt, Function):
        return interpreter_function(ctx, stmt)
    elif isinstance(stmt, MutableVariable) or isinstance(stmt, ImmutableVariable):
        return interpreter_variable(ctx, stmt)
    elif isinstance(stmt, ImmutableParameter) or isinstance(stmt, MutableParameter):
        return interpreter_parameter(ctx, stmt)
    elif isinstance(stmt, FunctionCall):
        return interpreter_function_call(ctx, stmt)
    elif isinstance(stmt, If):
        return interpreter_if(ctx, stmt)
    elif isinstance(stmt, While):
        return interpreter_while(ctx, stmt)
    elif isinstance(stmt, Assign):
        return interpreter_assign(ctx, stmt)
    elif isinstance(stmt, AssignArray):
        return interpreter_assign_array(ctx, stmt)
    
def interpreter_expression(ctx, expression: Expression):
    if isinstance(expression, IntLiteral) or isinstance(expression, StringLiteral) or isinstance(expression, CharLiteral) or isinstance(expression, FloatLiteral):
        return expression.value
    elif isinstance(expression, BooleanLiteral):
        return True if expression.value == "true" else False
    elif isinstance(expression, Identifier):
        return ctx.get_variable(expression.id).expression
    elif isinstance(expression, FunctionCall):
        return interpreter_function_call(ctx, expression)
    elif isinstance(expression, BinaryOp):
        return interpreter_binary_op(ctx, expression)
    elif isinstance(expression, Group):
        return interpreter_expression(ctx, expression.expression)
    elif isinstance(expression, UnaryOp):
        return -interpreter_expression(ctx, expression.expression)
    elif isinstance(expression, NotOp):
        return not interpreter_expression(ctx, expression.expression)
    elif isinstance(expression, ArrayLiteral):
        return [interpreter_expression(ctx, e) for e in expression.elements]
    elif isinstance(expression, AccessArray):
        return interpreter_access_array(ctx, expression)
    
def interpreter_block(ctx: Context, block: Block):
    ctx.enter_scope()
    for statement in block.statements:
        interpreter_statement(ctx, statement)
    ctx.exit_scope()

def interpreter_function(ctx: Context, function: Function):
    ctx.enter_scope()
    for param in function.parameters:
        interpreter_statement(ctx, param)
    ctx.set_variable(function.name, get_default_value(function.return_type))
    interpreter_statement(ctx, function.block)
    return_value = ctx.get_variable(function.name).expression
    ctx.exit_scope()
    return return_value
    
def interpreter_variable(ctx: Context, variable: MutableVariable| ImmutableVariable):
    ctx.set_variable(variable.name, interpreter_expression(ctx, variable.expression))

def interpreter_parameter(ctx: Context, parameter: MutableParameter | ImmutableParameter):
    ctx.set_variable(parameter.name, parameter.expression)

def interpreter_function_call(ctx: Context, function_call: FunctionCall):
    if function_call.name in ["print_int", "print_string", "print_char", "print_float", "print_boolean", "print_int_array", "print_2d_int_array"]:
        print(interpreter_expression(ctx, function_call.arguments[0]), end="")
    elif function_call.name == "concatenate_strings":
        return interpreter_expression(ctx, function_call.arguments[0]) + interpreter_expression(ctx, function_call.arguments[1], end="")
    elif function_call.name == "int_to_string":
        return str(interpreter_expression(ctx, function_call.arguments[0]), end="")
    else:
        func = ctx.get_function(function_call.name).function
        i = 0
        for param in func.parameters:
            param.expression = interpreter_expression(ctx, function_call.arguments[i])
            i += 1
        return interpreter_statement(ctx, func)

def interpreter_if(ctx: Context, if_stmt: If):
    if interpreter_expression(ctx, if_stmt.condition):
        interpreter_statement(ctx, if_stmt.b1)
    else:
        if if_stmt.b2 is not None:
            interpreter_statement(ctx, if_stmt.b2)

def interpreter_while(ctx: Context, while_stmt: While):
    while interpreter_expression(ctx, while_stmt.condition):
        interpreter_statement(ctx, while_stmt.block)

def interpreter_assign(ctx: Context, assign: Assign):
    ctx.assign_new_value(assign.variable, interpreter_expression(ctx, assign.expression))

def interpreter_binary_op(ctx: Context, binary_op: BinaryOp):
    left = interpreter_expression(ctx, binary_op.left_expression)
    right = interpreter_expression(ctx, binary_op.right_expression)
    if binary_op.op == "+":
        return left + right
    elif binary_op.op == "-":
        return left - right
    elif binary_op.op == "*":
        return left * right
    elif binary_op.op == "/":
        return left // right
    elif binary_op.op == "%":
        return left % right
    elif binary_op.op == "<":
        return left < right
    elif binary_op.op == ">":
        return left > right
    elif binary_op.op == "<=":
        return left <= right
    elif binary_op.op == ">=":
        return left >= right
    elif binary_op.op == "=":
        return left == right
    elif binary_op.op == "!=":
        return left != right
    elif binary_op.op == "&&":
        return left and right
    elif binary_op.op == "||":
        return left or right
    elif binary_op.op == '^':
        return left ** right

def interpreter_access_array(ctx: Context, access_array: AccessArray):
    array = ctx.get_variable(access_array.array).expression
    for idx in access_array.indexes:
        a = interpreter_expression(ctx, idx)
        array = array[a]
    return array

def interpreter_assign_array(ctx: Context, assign_array: AssignArray):
    access_array = assign_array._array
    array = ctx.get_variable(access_array.array).expression
    
    # Evaluate all index expressions
    indexes = [interpreter_expression(ctx, idx) for idx in access_array.indexes]
    
    # Traverse the array to the second-to-last index
    current_element = array
    for i in range(len(indexes) - 1):
        current_element = current_element.elements[indexes[i]]
    
    # Assign the value to the final index
    final_index = indexes[-1]
    current_element[final_index] = interpreter_expression(ctx, assign_array.expression)
    
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