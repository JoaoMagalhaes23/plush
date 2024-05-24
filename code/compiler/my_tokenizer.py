# https://www.dabeaz.com/ply/ply.html#ply_nn34
from ply import lex
import codecs

reserved = {
    'import'    : 'IMPORT',
    'if'        : 'IF',
    'else'      : 'ELSE',
    'while'     : 'WHILE',
    'function'  : 'FUNCTION',
    'var'       : 'MUTABLE_VARIABLE',
    'val'       : 'IMMUTABLE_VARIABLE',
    'boolean'   : 'BOOLEAN',
    'char'      : 'CHAR',
    'int'       : 'INT',
    'float'     : 'FLOAT',
    'string'    : 'STRING',
    'void'      : 'VOID',
}

tokens = [
    'ID',
    # BRAKETS
    'L_BRACKET',
    'R_BRACKET',
    'L_S_BRACKET',
    'R_S_BRACKET',
    # PARENTHESES
    'L_PAREN',
    'R_PAREN',
    # TYPES
    'BOOLEAN_LITERAL',
    'CHAR_LITERAL',
    'INT_LITERAL',
    'FLOAT_LITERAL',
    'STRING_LITERAL',
    # OPERATORS
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'MOD',
    'COLON',
    'COLON_EQUALS',
    'EQUALS',
    'DIFFERENT',
    'LESS',
    'GREATER',
    'LESS_EQUAL',
    'GREATER_EQUAL',
    'AND',
    'OR',
    'SEMICOLON',
    'COMMA',
    'NOT',
    'POWER',
] + list(reserved.values())

t_ignore            = ' \t'
#BRACKETS
t_L_BRACKET         = r'{'
t_R_BRACKET         = r'}'
t_L_S_BRACKET       = r'\['
t_R_S_BRACKET       = r'\]'
t_L_PAREN           = r'\('
t_R_PAREN           = r'\)'
#OPERATORS
t_PLUS              = r'\+'
t_MINUS             = r'-'
t_MULTIPLY          = r'\*'
t_DIVIDE            = r'\/'
t_MOD               = r'%'
t_COLON             = r':'
t_COLON_EQUALS      = r':='
t_EQUALS            = r'='
t_DIFFERENT         = r'!='
t_LESS              = r'<'
t_GREATER           = r'>'
t_LESS_EQUAL        = r'<='
t_GREATER_EQUAL     = r'>='
t_AND               = r'&&'
t_OR =              r'\|\|'
t_SEMICOLON         = r';'
t_COMMA             = r','
t_POWER             = r'\^'
t_NOT               = r'!'


def t_BOOLEAN_LITERAL(t):
    r'true|false'
    return t

def t_CHAR_LITERAL(t):
    r'\'[a-zA-Z0-9]\''
    return t

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT_LITERAL(t):
    r'[0-9]([0-9]|_[0-9])*'
    t.value = int(t.value.replace("_", ""))
    return t

def t_STRING_LITERAL(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = codecs.decode(t.value[1:-1], 'unicode_escape')
    return t

def t_ID(t):
    r'_*[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(),'ID')
    return t

def t_error(t):
    raise TypeError(f"Illegal character {t.value[0]}") 
    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_COMMENT(t):
    r'\#.*'
    pass
    
lexer = lex.lex()

if __name__ == "__main__":
    lexer.input(
        """
        import sys;
        val actual_min : int := -9;
        val actual_max : int := 9;

        function maxRangeSquared(var mi:int, val ma:int) : int {
            var current_max : int := mi ^ 2;
            while mi <= ma {
                var current_candidate : int := mi ^ 2;
                if current_candidate > current_max {
                    current_max := current_candidate;
                }
            } 
            maxRangeSquared := current_max; # This line returns the current max!
        }


        function main(val args:[string]): void {
            val result : int := maxRangeSquared(actual_min, actual_max);
            print_int(result);
        }
        """
    )
    while 1:
        tok = lexer.token()
        if not tok: break
        print(tok)
    print("Done")