import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(grandparent_dir)

# Now you can import the module
from my_tokenizer import lexer
from pytest import raises

def test_raises_exception_because_of_underscore():
    with raises(TypeError):
        invalid_variable_name = """_"""
        lexer.input(invalid_variable_name)
        while 1:
            tok = lexer.token()
            if not tok: break

def test_raises_exception_because_of_til():
    with raises(TypeError):
        invalid_variable_name = """~"""
        lexer.input(invalid_variable_name)
        while 1:
            tok = lexer.token()
            if not tok: break
            
def test_raises_exception_because_of_at():
    with raises(TypeError):
        invalid_variable_name = """@"""
        lexer.input(invalid_variable_name)
        while 1:
            tok = lexer.token()
            if not tok: break

def test_raises_exception_because_of_invalid_use_of_string_identifiers():
    with raises(TypeError):
        invalid_variable_name = """\"test\'"""
        lexer.input(invalid_variable_name)
        lexer.token()

def test_raises_exception_because_of_invalid_single_bar():
    with raises(TypeError):
        invalid_variable_name = """|"""
        lexer.input(invalid_variable_name)
        lexer.token()

def test_raises_exception_because_of_invalid_ampersand():
    with raises(TypeError):
        invalid_variable_name = """&"""
        lexer.input(invalid_variable_name)
        lexer.token()