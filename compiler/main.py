import sys

from ply import yacc, lex
from mparser import *
from tokrules import * 
from node import print_ast

#parser = yacc.yacc()

path = "/home/magalhaes/fcul/tc/plush_testsuite/compiler/tests/testing.pl"

with open(path, 'r') as f:
    data = f.read()
    f.close()

lex.lex()
yacc.yacc()
ast = yacc.parse(data)

print_ast(ast)

# with open(path, 'r') as f:
#     lex.input(f.read())
#     while True:
#         tok = lex.token()
#         if not tok:
#             break
#         print(tok)