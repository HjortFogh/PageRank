# FIXME: boolean input

import sys
from typing import Tuple, List

Field = Tuple[str, type, any]

def format_field(field : Field):
    """Returns a field formated as a string"""
    description, value_type, default_value = field
    return f"<{description}:{value_type.__name__}{('=' + str(default_value)) * (default_value != None)}>"

def print_correct_usage(fields : List[Field]):
    """Prints the correct usage, given a list of fields"""
    print(f"Usage: {sys.argv[0]} {' '.join([format_field(field) for field in fields])}")

def request(*args : List[Field]):
    """..."""

    # Check if arguments are passed in correct order
    is_optional = False
    for field in args:
        if not field[1] in [int, str, float, bool]: raise Exception(f"Invalid type: '{field[1].__name__}'")
        if field[2] != None: is_optional = True
        elif field[2] == None and is_optional: raise Exception("Non-optional arguments must be before optional arguments")
    
    # Check for help (-h, --help)
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print_correct_usage(args)
        sys.exit(0)

    # Get values from command line
    values = []
    
    for i, (d, t, v) in enumerate(args):
        if i + 1 >= len(sys.argv) and v == None:
            print("Incorrect argument count")
            print_correct_usage(args)
            sys.exit(0)

        if t != bool:
            try:
                if i + 1 >= len(sys.argv): value = v
                else: value = t(sys.argv[i + 1])
            except ValueError:
                print(f"Cannot parse value: '{sys.argv[i + 1]}' to type '{t.__name__}'")
                print_correct_usage(args)
                sys.exit(0)
        else:
            print("FIXME: Boolean support")
            sys.exit(0)
        
        values.append(value)
    
    return values
