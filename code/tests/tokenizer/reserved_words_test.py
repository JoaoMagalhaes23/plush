import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(grandparent_dir)

# Now you can import the module
from my_tokenizer import lexer

def test_if():
    valid_id_name = """if"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'IF'

def test_else():
    valid_id_name = """else"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'ELSE'

def test_while():
    valid_id_name = """while"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'WHILE'

def test_function():
    valid_id_name = """function"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'FUNCTION'

def test_var():
    valid_id_name = """var"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'MUTABLE_VARIABLE'

def test_val():
    valid_id_name = """val"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'IMMUTABLE_VARIABLE'

def test_boolean():
    valid_id_name = """boolean"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'BOOLEAN'

def test_char():
    valid_id_name = """char"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'CHAR'

def test_int():
    valid_id_name = """int"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'INT'

def test_float():
    valid_id_name = """float"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'FLOAT'

def test_string():
    valid_id_name = """string"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'STRING'

def test_void():
    valid_id_name = """void"""
    lexer.input(valid_id_name)
    tok = lexer.token()
    assert tok.type == 'VOID'