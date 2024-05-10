import sys

from ply import yacc, lex
from my_tokenizer import *
from my_parser import *
from my_semantic import verify, Context
from my_compiler import compiler
from node import print_ast
from tests.error.lexical_errors import lexical_errors
# py main.py <path> <see_tokens> <see_parser_ast> <see_semantic_ast> <see_llvm_code> 
# py main.py /home/magalhaes/fcul/tc/plush_testsuite/compiler/tests/testing.pl 0 0 0 1

lex.lex()
yacc.yacc()

SEPARATOR = "#############################################"

def run_tests():
    for test in lexical_errors:
        try:
            lex.input(test)
            while 1:
                tok = lex.token()
                if not tok: raise Exception("failed")
            print(f"Test was supposed to fail and it didn't.\n{test}")
        except Exception:
            print("ok")

def run_compiler(path, see_tokens, see_parser_ast, see_semantic_ast, see_llvm_code):
    with open(path, 'r') as f:
        data = f.read()
        f.close()
        
    if see_tokens == "1":
        lex.input(data)
        while 1:
            tok = lex.token()
            if not tok: break      # No more input
            print(tok)
        print(SEPARATOR)
    else:
        print("Not seeing tokens")

    ast = yacc.parse(data)

    if see_parser_ast == "1":
        print_ast(ast)
        print(SEPARATOR)
    else:
        print("Not seeing parser AST")

    verify(Context(), ast)

    if see_semantic_ast == "1":
        print_ast(ast)
        print(SEPARATOR)
    else:
        print("Not seeing semantic AST")

    if see_llvm_code == "1":
        llvm_code = compiler(ast)
        print(llvm_code)
        print(f"{SEPARATOR}\n")

        with open("code.ll", "w") as f:
            f.write(llvm_code)
        import subprocess

        # /usr/local/opt/llvm/bin/lli code.ll
        subprocess.call(
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