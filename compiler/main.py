import sys

from my_tokenizer import lexer
from my_parser import parser
from my_semantic import verify, Context
from my_compiler import compiler
from node import print_ast
# py main.py <path> <see_tokens> <see_parser_ast> <see_semantic_ast> <see_llvm_code> 


SEPARATOR = "#############################################"

def run_compiler(path, see_tokens, see_parser_ast, see_semantic_ast, see_llvm_code):
    with open(path, 'r') as f:
        data = f.read()
        f.close()
        
    if see_tokens == "1":
        lexer.input(data)
        while 1:
            tok = lexer.token()
            if not tok: break
            print(tok)
        print(SEPARATOR)
    else:
        print("Not seeing tokens")

    ast = parser.parse(data)

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
            "llc code.ll && clang -c plugin.c && clang -no-pie -fno-PIE code.s plugin.o -o code && ./code",
            shell=True,
        )
    else:
        print("Not seeing LLVM code")

if len(sys.argv) == 6:
    run_compiler(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
else:
    raise Exception("Call this file like this:\npy main.py <path> <see_tokens> <see_parser_ast> <see_semantic_ast> <see_llvm_code>")