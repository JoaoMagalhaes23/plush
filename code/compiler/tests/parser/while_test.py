import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(grandparent_dir)

from my_parser import parser
from pytest import raises

def test_valid_while():
    valid_while = """
    function x (): int {
        while true {
            x := 1;
        }
    }
    """
    parser.parse(valid_while)

def test_invalid_while_because_no_curly_brackets():
    invalid_while = """
    function x (): int {
        while true
            x := 1;
        }
    }
    """
    with raises(TypeError) :
        parser.parse(invalid_while)

def test_invalid_while_because_no_expression():
    invalid_while = """
    function x (): int {
        while {
            x := 1;
        }
    }
    """
    with raises(TypeError):
        parser.parse(invalid_while)

