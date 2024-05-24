import sys

from my_parser import parser
from my_type_checker import verify, Context
from my_compiler import compiler
from node import ast_to_json_file
from my_interpreter import interpreter, Context as InterpreterContext
import subprocess
import os

def handle_imports(ast, modules, base_directory):
    lib_directory = os.path.join(base_directory, "lib")
    if not os.path.exists(lib_directory):
        print(f"Directory '{lib_directory}' does not exist.")
        return
    for imp in ast.imports:
        import_name = imp.file_name
        if import_name not in modules:
            path = os.path.join(lib_directory, f"{import_name}.pl")
            if not os.path.exists(path):
                print(f"File '{path}' does not exist.")
                continue
            try:
                with open(path, 'r') as f:
                    data = f.read()
                module_ast = parser.parse(data)
                ast.statements += module_ast.statements
                modules[import_name] = module_ast.statements
                if module_ast.imports:
                    handle_imports(module_ast, modules, base_directory)
            except Exception as e:
                print(f"Failed to read or parse file '{path}': {e}")

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        show_ast_as_json = "--json" in sys.argv
        run_with_interpreter = "--interpreter" in sys.argv
        base_directory = os.path.dirname(os.path.abspath(__file__))
        generated_files_directory = "generated_files"
        with open(file_path, 'r') as f:
            data = f.read()
        ast = parser.parse(data)
        
        if ast.imports:
            handle_imports(ast, {}, base_directory)
        output_directory = os.path.join(base_directory, generated_files_directory)
        
        verify(ctx=Context(), ast=ast)
        if show_ast_as_json:
            ast_to_json_file(ast=ast, directory=output_directory)
        if run_with_interpreter:
            interpreter(InterpreterContext(), ast)
        else:
            output_file_path = os.path.join(output_directory, "code.ll")
            plugin_object_file = os.path.join(output_directory, "plugin.o")
            asm_file_path = os.path.join(output_directory, "code.s")
            executable_path = os.path.join(output_directory, "code")
            
            llvm_code = compiler(ast=ast)
            
            os.makedirs(output_directory, exist_ok=True)
            
            with open(output_file_path, "w") as f:
                f.write(llvm_code)           
            subprocess.call(
                f"llc {output_file_path} && clang -c plugin.c -o {plugin_object_file} && clang -no-pie -fno-PIE {asm_file_path} {plugin_object_file} -o {executable_path} && ./{generated_files_directory}/code",
                shell=True,
            )

    else:
        raise TypeError("Call this file like this:\npy main.py <path>")

if __name__ == "__main__":
    main()
    