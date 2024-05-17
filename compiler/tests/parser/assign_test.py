import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(grandparent_dir)

# Now you can import the module
from my_parser import parser
from pytest import raises

def test_valid_assign():
    valid_assign = """
    function x (): int {
        x := 1;
    }
    """
    parser.parse(valid_assign)

def test_invalid_assign_because_no_semicolon():
    with raises(TypeError):
        invalid_assign = """
        function x (): int {
            x := 1
        }"""
        parser.parse(invalid_assign)

def test_invalid_assign_because_no_expression():
    with raises(TypeError):
        invalid_assign = """
        function x (): int {
            x := ;
        }"""
        parser.parse(invalid_assign)

def test_invalid_assign_because_no_id():
    with raises(TypeError):
        invalid_assign = """
        function x (): int {
            := ;
        }"""
        parser.parse(invalid_assign)

def test_invalid_assign_because_bad_semicolon_equals_sign():
    with raises(TypeError):
        invalid_assign = """
        function x (): int {
            x = ;
        }"""
        parser.parse(invalid_assign)

