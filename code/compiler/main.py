import sys

from my_parser import parser
from my_type_checker import verify, Context
from my_compiler import compiler
from node import ast_to_json_file
from my_interpreter import interpreter, Context as InterpreterContext
import subprocess
import os

def handle_imports(ast, modules, base_directory):
    for imp in ast.imports:
        import_name = imp.file_name
        import_path = os.path.join(base_directory, import_name)
        
        if import_name not in modules:
            if not os.path.exists(import_path):
                print(f"File '{import_path}' does not exist.")
                continue
            
            try:
                with open(import_path, 'r') as f:
                    data = f.read()
                
                module_ast = parser.parse(data)
                ast.statements += module_ast.statements
                modules[import_name] = module_ast.statements
                
                if module_ast.imports:
                    new_base_directory = os.path.dirname(import_path)
                    handle_imports(module_ast, modules, new_base_directory)
            except Exception as e:
                print(f"Failed to read or parse file '{import_path}': {e}")

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        show_ast_as_json = "-json" in sys.argv
        run_with_interpreter = "-i" in sys.argv
        args = []
        if "-args" in sys.argv:
            args = sys.argv[sys.argv.index("-args") + 1:]
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
            args.insert(0, file_path)
            interpreter(InterpreterContext(), ast, args)
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
                f"llc {output_file_path} && clang -c plugin.c -o {plugin_object_file} && clang -no-pie -fno-PIE {asm_file_path} {plugin_object_file} -o {executable_path} && ./{generated_files_directory}/code {' '.join(args)}",
                shell=True,
            )
    else:
        raise TypeError("Call this file like this:\npy main.py <path>")

if __name__ == "__main__":
    main()
    