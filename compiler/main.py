import sys

from ply import yacc, lex
from my_parser import *
from my_tokenizer import * 
from node import print_ast
from my_semantic import *
from my_compiler import *

# py main.py <path> <seeTokens> <seeParserAst> <seeSemanticAst> <seeLLVMcode> 
# py main.py /home/magalhaes/fcul/tc/plush_testsuite/compiler/tests/testing.pl 0 0 0 1
if len(sys.argv) != 6:
    raise Exception("Invalid number of arguments")

with open(sys.argv[1], 'r') as f:
        data = f.read()
        f.close()
        
lex.lex()

see_parser = False
if sys.argv[2] == "1":
    lex.input(data)
    while 1:
        tok = lex.token()
        if not tok: break      # No more input
        print(tok)
    print("#############################################")
else:
    print("Not seeing tokens")

yacc.yacc()
ast = yacc.parse(data)

if sys.argv[3] == "1":
    print_ast(ast)
    print("#############################################")
else:
    print("Not seeing parser AST")

verify(Context(), ast)

if sys.argv[4] == "1":
    print_ast(ast)
    print("#############################################")
else:
    print("Not seeing semantic AST")

if sys.argv[5] == "1":
    llvm_code = compiler(ast)
    print(llvm_code)
else:
    print("Not seeing LLVM code")
