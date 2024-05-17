import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(grandparent_dir)

# Now you can import the module
from my_parser import parser
from pytest import raises

def test_valid_mutable_variable_declaration():
    valid_variable_declaration = """var x: int := 1;"""
    parser.parse(valid_variable_declaration)

def test_valid_immutable_variable_declaration():
    valid_variable_declaration = """val x: int := 1;"""
    parser.parse(valid_variable_declaration)

def test_invalid_variable_declaration_because_equals_sign():
    with raises(TypeError):
        invalid_variable_declaration = """var x: int = 1;"""
        parser.parse(invalid_variable_declaration)

def test_invalid_variable_declaration_because_no_semicolon():
    with raises(TypeError):
        invalid_variable_declaration = """var x: int := 1"""
        parser.parse(invalid_variable_declaration)

def test_invalid_variable_declaration_because_no_colon():
    with raises(TypeError):
        invalid_variable_declaration = """var x int := 1;"""
        parser.parse(invalid_variable_declaration)

def test_invalid_variable_declaration_because_no_type():
    with raises(TypeError):
        invalid_variable_declaration = """var x: = 1;"""
        parser.parse(invalid_variable_declaration)

def test_invalid_variable_declaration_because_no_expression():
    with raises(TypeError):
        invalid_variable_declaration = """var x: int :=;"""
        parser.parse(invalid_variable_declaration)

def test_invalid_variable_declaration_because_no_id():
    with raises(TypeError):
        invalid_variable_declaration = """var : int := 1;"""
        parser.parse(invalid_variable_declaration)

def test_invalid_variable_declaration_because_no_var():
    with raises(TypeError):
        invalid_variable_declaration = """x: int := 1;"""
        parser.parse(invalid_variable_declaration)


