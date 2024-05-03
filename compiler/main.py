import sys

from ply import yacc, lex
from mparser import *
from tokrules import * 
from node import print_ast
from semantic import *

if len(sys.argv) < 2:
    path = "/home/magalhaes/fcul/tc/plush_testsuite/compiler/tests/testing.pl"
else:
    path = sys.argv[1]

with open(path, 'r') as f:
        data = f.read()
        f.close()
        
lex.lex()

see_parser = False
if see_parser:
    lex.input(data)
    while 1:
        tok = lex.token()
        if not tok: break      # No more input
        print(tok)
    print("#############################################")

yacc.yacc()
ast = yacc.parse(data)

verify(Context(), ast)

print_ast(ast)

print("Verified")
