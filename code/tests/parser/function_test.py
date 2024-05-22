import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(grandparent_dir)

from my_parser import parser
from pytest import raises

def test_valid_function_declaration():
    valid_function = """function main (): int;"""
    parser.parse(valid_function)

def test_invalid_function_declaration_because_no_semicolon():
    with raises(TypeError):
        invalid_function = """function main () int"""
        parser.parse(invalid_function)

def test_invalid_function_declaration_because_no_return_type():
    with raises(TypeError):
        invalid_function = """function main ()"""
        parser.parse(invalid_function)

def test_invalid_function_declaration_because_no_parentheses():
    with raises(TypeError):
        invalid_function = """function main : int;"""
        parser.parse(invalid_function)

def test_invalid_function_declaration_because_no_id():
    with raises(TypeError):
        invalid_function = """function (): int;"""
        parser.parse(invalid_function)

def test_invalid_function_declaration_because_no_function():
    with raises(TypeError):
        invalid_function = """main (): int;"""
        parser.parse(invalid_function)

def test_invalid_function_declaration_because_no_colon():
    with raises(TypeError):
        invalid_function = """function main () int"""
        parser.parse(invalid_function)
        
def test_invalid_function_declaration_because_parentheses_not_closed():
    with raises(TypeError):
        invalid_function = """function main( int;"""
        parser.parse(invalid_function)

def test_invalid_function_declaration_because_parentheses_not_opened():
    with raises(TypeError):
        invalid_function = """function main ) int;"""
        parser.parse(invalid_function)

def test_valid_function_declaration_with_parameters():
    valid_function = """function main (val x: int, val y: int): int;"""
    parser.parse(valid_function)

def test_invalid_function_declaration_because_parameter_have_no_type():
    with raises(TypeError):
        invalid_function = """function main (val x:);"""
        parser.parse(invalid_function)

def test_invalid_function_declaration_because_parameter_have_no_id():
    with raises(TypeError):
        invalid_function = """function main (val : int);"""
        parser.parse(invalid_function)
    
def test_invalid_function_declaration_because_parameter_have_no_colon():
    with raises(TypeError):
        invalid_function = """function main (val x int);"""
        parser.parse(invalid_function)

def test_invalid_function_declaration_because_parameter_have_no_comma():
    with raises(TypeError):
        invalid_function = """function main (val x: int var y: int);"""
        parser.parse(invalid_function)

def test_invalid_function_declaration_because_parameter_have_no_colon():
    with raises(TypeError):
        invalid_function = """function main (val x int, var y int);"""
        parser.parse(invalid_function)

def test_invalid_function_declaration_because_parameter_have_no_val():
    with raises(TypeError):
        invalid_function = """function main (x: int, y: int);"""
        parser.parse(invalid_function)

def test_valid_function_with_block():
    valid_function = """function main (): int { x := 1; }"""
    parser.parse(valid_function)

def test_invalid_function_with_block_because_no_left_bracket():
    with raises(TypeError):
        invalid_function = """function main (): int x := 1; }"""
        parser.parse(invalid_function)

def test_invalid_function_with_block_because_no__right_bracket():
    with raises(TypeError):
        invalid_function = """function main (): int { x := 1;"""
        parser.parse(invalid_function)

