import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(grandparent_dir)

from my_parser import parser
from pytest import raises

def test_valid_array():
    valid_array = """
    function x (): int {
        var a: [[[int]]] := {1,2,3};
    }
    """
    parser.parse(valid_array)

def test_invalid_array_because_no_curly_brackets():
    invalid_array = """
    function x (): int {
        var a: [int] := 1,2,3;
    }
    """
    with raises(TypeError) :
        parser.parse(invalid_array)

def test_invalid_array_because_no_type():
    invalid_array = """
    function x (): int {
        var a := {1,2,3};
    }
    """
    with raises(TypeError):
        parser.parse(invalid_array)

def test_invalid_array_because_no_colon():
    invalid_array = """
    function x (): int {
        var a [int] := {1,2,3};
    }
    """
    with raises(TypeError):
        parser.parse(invalid_array)

def test_invalid_array_because_no_id():
    invalid_array = """
    function x (): int {
        var : [int] := {1,2,3};
    }
    """
    with raises(TypeError):
        parser.parse(invalid_array)

def test_invalid_array_because_no_assignment():
    invalid_array = """
    function x (): int {
        var a: [int];
    }
    """
    with raises(TypeError):
        parser.parse(invalid_array)

def test_valid_index():
    valid_index = """
    function x (): int {
        var a: [int] := {1,2,3};
        var b: int := a[1][2][3];
    }
    """
    parser.parse(valid_index)

def test_invalid_index_because_no_left_bracket():
    invalid_index = """
    function x (): int {
        var a: [int] := {1,2,3};
        var b: int := a1];
    }
    """
    with raises(TypeError):
        parser.parse(invalid_index)

def test_invalid_index_because_no_right_bracket():
    invalid_index = """
    function x (): int {
        var a: [int] := {1,2,3};
        var b: int := a[1;
    }
    """
    with raises(TypeError):
        parser.parse(invalid_index)

def test_invalid_index_because_no_expression():
    invalid_index = """
    function x (): int {
        var a: [int] := {1,2,3};
        var b: int := a[];
    }
    """
    with raises(TypeError):
        parser.parse(invalid_index)
