import sys

from my_parser import parser
from my_type_checker import verify, Context
from my_compiler import compiler
from node import ast_to_json_file
from my_interpreter import interpreter, Context as InterpreterContext
import subprocess
import os

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        show_ast_as_json = True if "--json" in sys.argv else False
        run_with_interpreter = True if "--interpreter" in sys.argv else False
        output_directory = "generated_files"
        output_file_path = os.path.join(output_directory, "code.ll")
        plugin_object_file = os.path.join(output_directory, "plugin.o")
        asm_file_path = os.path.join(output_directory, "code.s")
        executable_path = os.path.join(output_directory, "code")
        try:
            with open(file_path, 'r') as f:
                data = f.read()
            
            ast = parser.parse(data)
            verify(ctx=Context(), ast=ast)
            if show_ast_as_json:
                ast_to_json_file(ast=ast, directory=output_directory)
            if run_with_interpreter:
                interpreter(InterpreterContext(), ast)
            else:
                llvm_code = compiler(ast=ast)
                
                os.makedirs(output_directory, exist_ok=True)
                
                with open(output_file_path, "w") as f:
                    f.write(llvm_code)
                
                subprocess.call(
                    f"llc {output_file_path} && clang -c plugin.c -o {plugin_object_file} && clang -no-pie -fno-PIE {asm_file_path} {plugin_object_file} -o {executable_path} && ./{executable_path}",
                    shell=True,
                )
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        raise TypeError("Call this file like this:\npy main.py <path>")

if __name__ == "__main__":
    main()
    