
single_letter_id = """
val v: int := 10; 
"""

id_starting_with_number = """
val 1v: int := 10;
"""

id_containing_a_dot = """
val te.st: int := 10;
"""

id_containing_a_dash = """
val te-st: int := 10;
"""

type_dont_exists = """
val test: type := 10;
"""

integer_cannot_start_with_underscore = """
val test: int := _10;
"""

integer_cannot_end_with_underscore = """
val test: int := 10_;
"""

invalid_character = """
val test: int := @;
"""

missing_the_comment_character = """
val test: int := 10; this is a comment
"""

lexical_errors = [
    single_letter_id, 
    id_starting_with_number,
    id_containing_a_dot,
    id_containing_a_dash,
    type_dont_exists,
    integer_cannot_start_with_underscore,
    integer_cannot_end_with_underscore,
    invalid_character,
    missing_the_comment_character
]

