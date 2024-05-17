import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(grandparent_dir)

from my_parser import parser
from pytest import raises

def test_valid_if():
    valid_if = """
    function x (): int {
        if true {
            x := 1;
        }
    }
    """
    parser.parse(valid_if)
    
def test_valid_if_else():
    valid_if_else = """
    function x (): int {
        if true {
            x := 1;
        } else {
            x := 2;
        }
    }
    """
    parser.parse(valid_if_else)

def test_valid_if_else_if():
    valid_if_else = """
    function x (): int {
        if true {
            x := 1;
        } else if false {
            x := 2;
        }
    }
    """
    parser.parse(valid_if_else)

def test_valid_if_else_if_else():
    valid_if_else = """
    function x (): int {
        if true {
            x := 1;
        } else if false {
            x := 2;
        } else {
            x := 3;
        }
    }
    """
    parser.parse(valid_if_else)

def test_invalid_if_because_no_left_bracket():
    with raises(TypeError):
        invalid_if = """
        function x (): int {
            if true 
                x := 1;
            }
        }
        """
        parser.parse(invalid_if)

def test_invalid_if_because_no_right_bracket():
    with raises(TypeError):
        invalid_if = """
        function x (): int {
            if true {
                x := 1;
            
        }
        """
        parser.parse(invalid_if)