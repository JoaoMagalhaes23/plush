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
    p[0] = ProgramNode(children=[p[1]])

def p_top_level_declarations(p):
    '''
    top_level_declarations  : top_level_declaration top_level_declarations
                            | top_level_declaration
    '''
    if len(p) == 2:
        p[0] = TopLevelDeclarations(children=[p[1]])
    else:
        p[0] = TopLevelDeclarations(children=[p[1]] + p[2].children)

    
def p_top_level_declaration(p):
    '''
    top_level_declaration   : create_variable SEMICOLON
                            | assign SEMICOLON
                            | function
    '''
    p[0] = p[1]

def p_create_variable(p):
    '''
    create_variable : MUTABLE_VARIABLE ID COLON type t
                    | IMMUTABLE_VARIABLE ID COLON type t   
    '''
    if p[1] == 'var':
        if p[5] != None:
            p[0] = MutableVariable(name=p[2], children=[p[4], p[5]])
        else:
            p[0] = MutableVariable(name=p[2], children=[p[4]])
    else:
        if p[5] != None:
            p[0] = ImmutableVariable(name=p[2], children=[p[4], p[5]])
        else:
            p[0] = ImmutableVariable(name=p[2], children=[p[4]])

def p_t(p):
    '''
    t   : COLON_EQUALS expression
        | 
    '''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_assign(p):
    '''
    assign : ID COLON_EQUALS expression
    '''
    p[0] = Assign(name=p[1], children=[p[3]])
    
def p_function(p):
    '''
    function : FUNCTION ID L_PAREN parameter_list R_PAREN COLON type L_BRACKET block R_BRACKET
    '''
    p[0] = Function(name=p[2], children=[p[4], p[7], p[9]])

def p_parameter_list(p):
    '''
    parameter_list  : create_variable COMMA parameter_list
                    | create_variable
    '''
    if len(p) == 2:
        p[0] = ParameterList(children=[p[1]])
    else:
        p[0] = ParameterList(children=[p[1]] + p[3].children)
    
def p_block(p):
    ''' 
    block   : statement block 
            | statement
    '''
    if len(p) == 2:
        p[0] = Block(children=[p[1]])
    else:
        p[0] = Block(children=[p[1]] + p[2].children)
    
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
    if_statement    : IF expression L_BRACKET block R_BRACKET else_if_statements
    '''
    if p[6] != None:
        p[0] = If(children=[p[2], p[4], p[6]])
    else:
        p[0] = If(children=[p[2], p[4]])

def p_else_if_statements(p):
    '''
    else_if_statements  : ELSE IF expression L_BRACKET block R_BRACKET else_if_statements
                        | ELSE IF expression L_BRACKET block R_BRACKET
                        | ELSE L_BRACKET block R_BRACKET
    '''
    if len(p) == 8:
        p[0] = ElseIf(children=[p[3], p[5], p[7]])
    elif len(p) == 7:
        p[0] = ElseIf(children=[p[3], p[5]])
    else:
        p[0] = Else(children=[p[3]])

def p_while_statement(p):
    '''
    while_statement : WHILE expression L_BRACKET block R_BRACKET
    '''
    p[0] = While(children=[p[2], p[4]])

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
        p[0] = Group(children=[p[2]])
    elif len(p) == 4:
        p[0] = BinaryOp(op=p[2], children=[p[1], p[3]])
    else:
        p[0] = p[1]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = UnaryOp(op=p[1], children=[p[2]])

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = UnaryOp(op=p[1], children=[p[2]])

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
    p[0] = ArrayType(children=[p[2]])
    
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
            | array
    '''
    p[0] = p[1]

def p_literal_int(p):
    '''
    literal_int : INT_LITERAL
    '''
    p[0] = IntLiteral(p[1])

def p_literal_double(p):
    '''
    literal_double : DOUBLE_LITERAL
    '''
    p[0] = DoubleLiteral(p[1])

def p_literal_string(p):
    '''
    literal_string : STRING_LITERAL
    '''
    p[0] = StringLiteral(p[1])

def p_literal_boolean(p):
    '''
    literal_boolean : BOOLEAN_LITERAL
    '''
    p[0] = BooleanLiteral(p[1])

def p_literal_char(p):
    '''
    literal_char : CHAR_LITERAL
    '''
    p[0] = CharLiteral(p[1])

def p_literal_float(p):
    '''
    literal_float : FLOAT_LITERAL
    '''
    p[0] = FloatLiteral(p[1])

def p_identifier(p):
    '''
    identifier  : ID
                | ID L_S_BRACKET expression R_S_BRACKET
    '''
    if len(p) == 5:
        p[0] = Index(array=p[1], children=[p[3]])
    else: 
        p[0] = Identifier(p[1])

def p_array(p):
    '''
    array   : L_S_BRACKET values_list R_S_BRACKET
            | L_BRACKET R_BRACKET
    '''
    p[0] = p[2]

def p_values_list(p):
    '''
    values_list : value COMMA values_list
                | value
                |
    '''
    if len(p) == 4:
        p[0] = ArrayLiteral(children=[p[1]] + p[3].children)
    elif len(p) == 2:
        p[0] = ArrayLiteral(children=[p[1]])
    else:
        p[0] = ArrayLiteral()

def p_function_call(p):
    '''
    function_call : ID L_PAREN arguments_list R_PAREN
    '''
    p[0] = FunctionCall(name=p[1], children=[p[3]])

def p_arguments_list(p):
    '''
    arguments_list  : expression COMMA arguments_list
                    | expression
                    |
    '''
    if len(p) == 4:
        p[0] = ArgumentsList(children=[p[1], p[3]])
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ArgumentsList()

def p_error(p):
    if p:
        print("Syntax error at token %s" % p.value)
    else:
        print("Syntax error at EOF")
