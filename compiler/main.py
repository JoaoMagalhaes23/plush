import sys

from ply import yacc, lex
from my_parser import *
from my_tokenizer import * 
from node import print_ast
from my_semantic import *
from my_compiler import *
from tests.error.lexical_errors import lexical_errors
# py main.py <path> <seeTokens> <seeParserAst> <seeSemanticAst> <seeLLVMcode> 
# py main.py /home/magalhaes/fcul/tc/plush_testsuite/compiler/tests/testing.pl 0 0 0 1

lex.lex()
yacc.yacc()

def run_tests():
    for test in lexical_errors:
        try:
            lex.input(test)
            while 1:
                tok = lex.token()
                if not tok: raise Exception("failed")
            print(f"Test was supposed to fail and it didn't.\n{test}")
        except Exception as e:
            print("ok")

def run_compiler(path, seeTokens, seeParserAst, seeSemanticAst, seeLLVMcode):
    with open(path, 'r') as f:
        data = f.read()
        f.close()
        
    if seeTokens == "1":
        lex.input(data)
        while 1:
            tok = lex.token()
            if not tok: break      # No more input
            print(tok)
        print("#############################################")
    else:
        print("Not seeing tokens")

    ast = yacc.parse(data)

    if seeParserAst == "1":
        print_ast(ast)
        print("#############################################")
    else:
        print("Not seeing parser AST")

    verify(Context(), ast)

    if seeSemanticAst == "1":
        print_ast(ast)
        print("#############################################")
    else:
        print("Not seeing semantic AST")

    if seeLLVMcode == "1":
        llvm_code = compiler(ast)
        print(llvm_code)
        with open("code.ll", "w") as f:
            f.write(llvm_code)
        import subprocess

        # /usr/local/opt/llvm/bin/lli code.ll
        r = subprocess.call(
            "llc code.ll && clang code.s plugin.o -o code && ./code",
            shell=True,
        )
    else:
        print("Not seeing LLVM code")

if len(sys.argv) == 1:
    run_tests()
elif len(sys.argv) == 6:
    run_compiler(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
else:
    raise Exception("Invalid number of arguments")