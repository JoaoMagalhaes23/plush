import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(grandparent_dir)

# Now you can import the module
from my_parser import parser
from my_type_checker import verify, Context
from pytest import raises

def generate_ast(data):
    ast = parser.parse(data)
    return ast
