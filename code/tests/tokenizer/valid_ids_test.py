import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(grandparent_dir)

# Now you can import the module
from my_tokenizer import lexer

def test_valid_ID():
    valid_id_name = """a"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'ID'

def test_valid_ID_with_underscore():
    valid_id_name = """_a"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'ID'

def test_valid_ID_with_numbers():
    valid_id_name = """_a1"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'ID'

def test_valid_ID_with_numbers_at_end():
    valid_id_name = """a1_"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'ID'

def test_valid_ID_with_underscore_in_the_middle():
    valid_id_name = """a_a"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'ID'
    
def test_valid_ID_with_underscore_in_the_middle_and_numbers():
    valid_id_name = """a_a1"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'ID'
    