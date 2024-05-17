import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(grandparent_dir)

# Now you can import the module
from my_tokenizer import lexer
from pytest import raises

def test_valid_INT_LITERAL():
    valid_int_literal = """1"""
    lexer.input(valid_int_literal)
    tok = lexer.token()
    assert tok.type == 'INT_LITERAL'

def test_valid_INT_LITERAL_with_underscore():
    valid_int_literal = """1_000"""
    lexer.input(valid_int_literal)
    tok = lexer.token()
    assert tok.type == 'INT_LITERAL'

def test_invalid_INT_LITERAL_with_underscores_in_the_middle():
    valid_int_literal = """1_000_000"""
    lexer.input(valid_int_literal)
    tok = lexer.token()
    assert tok.type == 'INT_LITERAL'
    
def test_invalid_INT_LITERAL_with_underscore_at_the_end():
    with raises(TypeError):
        invalid_int_literal = """1_000_"""
        lexer.input(invalid_int_literal)
        assert lexer.token().type == 'INT_LITERAL'
        lexer.token() # This will raise an exception

def test_invalid_INT_LITERAL_with_underscore_at_the_beginning():
    with raises(TypeError):
        invalid_int_literal = """_1_000"""
        lexer.input(invalid_int_literal)
        lexer.token()
