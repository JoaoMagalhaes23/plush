from node import *

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MOD'),
    ('right', 'POWER'),
    ('nonassoc', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL', 'EQUALS', 'DIFFERENT'),
    ('left', 'AND'),
    ('left', 'OR'),
    ('right', 'NOT'),
    ('right','UMINUS'),

)

def p_start(p):
    '''
    start : top_level_declarations
    '''
    p[0] = ProgramNode(statements=p[1])

def p_top_level_declarations(p):
    '''
    top_level_declarations  : top_level_declaration top_level_declarations
                            | top_level_declaration
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

    
def p_top_level_declaration(p):
    '''
    top_level_declaration   : create_variable SEMICOLON
                            | function
    '''
    p[0] = p[1]

def p_create_variable(p):
    '''
    create_variable : MUTABLE_VARIABLE ID COLON type COLON_EQUALS expression
                    | IMMUTABLE_VARIABLE ID COLON type COLON_EQUALS expression   
    '''
    if p[1] == 'var':
        p[0] = MutableVariable(name=p[2], type=p[4], expression=p[6])
    else:
        p[0] = ImmutableVariable(name=p[2], type=p[4], expression=p[6])
            
def p_assign(p):
    '''
    assign : ID COLON_EQUALS expression
    '''
    p[0] = Assign(name=p[1], expression=p[3])
    
def p_function(p):
    '''
    function    : FUNCTION ID L_PAREN parameter_list R_PAREN COLON type L_BRACKET block R_BRACKET
                | FUNCTION ID L_PAREN parameter_list R_PAREN COLON type SEMICOLON
    '''
    if len(p) == 11:
        p[0] = Function(name=p[2], parameters= p[4], return_type=p[7], block=p[9])
    else:
        p[0] = Function(name=p[2], parameters= p[4], return_type=p[7])

def p_parameter_list(p):
    '''
    parameter_list  : parameter COMMA parameter_list
                    | parameter
                    |
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []
        
def p_parameter(p):
    '''
    parameter   : MUTABLE_VARIABLE ID COLON type
                | IMMUTABLE_VARIABLE ID COLON type
    '''
    if p[1] == 'var':
        p[0] = MutableParameter(name=p[2], type=p[4])
    else:
        p[0] = ImmutableParameter(name=p[2], type=p[4])
    
def p_block(p):
    ''' 
    block   : statement block 
            | statement
    '''
    if len(p) == 2:
        p[0] = Block(statements=[p[1]])
    else:
        p[0] = Block(statements=[p[1]] + p[2].statements)
    
def p_statement(p):
    '''
    statement   : if_statement
                | while_statement
                | assign SEMICOLON
                | create_variable SEMICOLON
                | function_call SEMICOLON
    '''
    p[0] = p[1]

def p_if_statement(p):
    '''
    if_statement    : IF expression L_BRACKET block R_BRACKET
                    | IF expression L_BRACKET block R_BRACKET else_if_statements
                    | IF expression L_BRACKET block R_BRACKET ELSE L_BRACKET block R_BRACKET
    '''
    if len(p) == 6:
        p[0] = If(condition=p[2], b1=p[4])
    elif len(p) == 7:
        p[0] = If(condition=p[2], b1=p[4], b2=p[6])
    else:
        p[0] = If(condition=p[2], b1=p[4], b2=p[8])
        
def p_else_if_statements(p):
    '''
    else_if_statements  : ELSE IF expression L_BRACKET block R_BRACKET
                        | ELSE IF expression L_BRACKET block R_BRACKET else_if_statements
                        | ELSE IF expression L_BRACKET block R_BRACKET ELSE L_BRACKET block R_BRACKET
    '''
    if len(p) == 7:
        p[0] = If(condition=p[3], b1=p[5])
    elif len(p) == 8:
        p[0] = If(condition=p[3], b1=p[5], b2=p[7])
    else:
        p[0] = If(condition=p[3], b1=p[5], b2=p[9])

def p_while_statement(p):
    '''
    while_statement : WHILE expression L_BRACKET block R_BRACKET
    '''
    p[0] = While(condition=p[2], block=p[4])

def p_expression(p):
    '''
    expression  : expression MULTIPLY expression
                | expression DIVIDE expression
                | expression MOD expression
                | expression POWER expression
                | expression PLUS expression
                | expression MINUS expression
                | expression LESS expression
                | expression GREATER expression
                | expression GREATER_EQUAL expression
                | expression LESS_EQUAL expression
                | expression EQUALS expression
                | expression DIFFERENT expression
                | expression AND expression
                | expression OR expression
                | L_PAREN expression R_PAREN
                | value
    '''
    if p[1] == '(':
        p[0] = Group(expression=p[2])
    elif len(p) == 4:
        p[0] = BinaryOp(op=p[2], left_expression=p[1], right_expression =  p[3])
    else:
        p[0] = p[1]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = UnaryOp(expression=p[2])

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = NotOp(expression=p[2])

def p_type(p):
    '''
    type    : type_int
            | type_double
            | type_string
            | type_boolean
            | type_char
            | type_float
            | type_void
            | type_array
    '''
    p[0] = p[1]

def p_type_int(p):
    '''
    type_int : INT
    '''
    p[0] = IntType()

def p_type_double(p):
    '''
    type_double : DOUBLE
    '''
    p[0] = DoubleType()

def p_type_string(p):
    '''
    type_string : STRING
    '''
    p[0] = StringType()

def p_type_boolean(p):
    '''
    type_boolean : BOOLEAN
    '''
    p[0] = BooleanType()

def p_type_char(p):
    '''
    type_char : CHAR
    '''
    p[0] = CharType()
    
def p_type_float(p):
    '''
    type_float : FLOAT
    '''
    p[0] = FloatType()

def p_type_void(p):
    '''
    type_void : VOID
    '''
    p[0] = VoidType()

def p_type_array(p):
    '''
    type_array : L_S_BRACKET type R_S_BRACKET
    '''
    p[0] = ArrayType(subtype=p[2])
    
def p_value(p):
    '''
    value   : literal_int
            | literal_double
            | literal_string
            | literal_boolean
            | literal_char
            | literal_float
            | identifier
            | function_call
            | index
            | array
    '''
    p[0] = p[1]

def p_literal_int(p):
    '''
    literal_int : INT_LITERAL
    '''
    p[0] = IntLiteral(value = p[1])

def p_literal_double(p):
    '''
    literal_double : DOUBLE_LITERAL
    '''
    p[0] = DoubleLiteral(value = p[1])

def p_literal_string(p):
    '''
    literal_string : STRING_LITERAL
    '''
    p[0] = StringLiteral(value = p[1])

def p_literal_boolean(p):
    '''
    literal_boolean : BOOLEAN_LITERAL
    '''
    p[0] = BooleanLiteral(value = p[1])

def p_literal_char(p):
    '''
    literal_char : CHAR_LITERAL
    '''
    p[0] = CharLiteral(value = p[1])

def p_literal_float(p):
    '''
    literal_float : FLOAT_LITERAL
    '''
    p[0] = FloatLiteral(value = p[1])

def p_identifier(p):
    '''
    identifier  : ID
    '''
    p[0] = Identifier(id = p[1])

def p_index(p):
    '''
    index   : ID temp
    temp    : L_S_BRACKET expression R_S_BRACKET temp
            | L_S_BRACKET expression R_S_BRACKET
    '''
    if len(p) == 5:
        p[0] = [p[2]] + p[4]
    elif len(p) == 4:
        p[0] = [p[2]]
    else:
        p[0] = AccessArray(array=p[1], indexes=p[2])


def p_array(p):
    '''
    array   : L_BRACKET array_literal R_BRACKET
            | L_BRACKET R_BRACKET
    '''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = ArrayLiteral()

def p_array_literal(p):
    '''
    array_literal   : expression COMMA array_literal
                    | expression
    '''
    if len(p) == 4:
        p[0] = ArrayLiteral(elements=[p[1]] + p[3].elements)
    elif len(p) == 2:
        p[0] = ArrayLiteral(elements=[p[1]])

def p_function_call(p):
    '''
    function_call : ID L_PAREN arguments_list R_PAREN
    '''
    p[0] = FunctionCall(name=p[1], arguments=p[3])

def p_arguments_list(p):
    '''
    arguments_list  : expression COMMA arguments_list
                    | expression
                    |
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []

def p_error(p):
    if p:
        raise Exception(f"Syntax error at token {p.value} that is at line {p.lineno}")
    else:
        print("Syntax error at EOF")
        #raise Exception("Syntax error at EOF")
