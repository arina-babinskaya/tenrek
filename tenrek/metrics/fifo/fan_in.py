from .fifo_help_functions import class_uses_type
from .fifo_help_functions import callable_uses_type

def calculate(target_class, parser):
    target_name = target_class.spelling
    users = set()

    classes = parser.get_classes()
    functions = parser.get_functions()
    methods = parser.get_methods()

    for clas in classes:
        if clas.spelling == target_name:
            continue

        if class_uses_type(clas, target_name):
            users.add(clas.spelling)

    for func in functions:
        if callable_uses_type(func, target_name):
            users.add(func.spelling)

    for method in methods:
        owner = method.semantic_parent.spelling if method.semantic_parent else ""
        fullname = f"{owner}::{method.spelling}" #for separating same methods in different classes

        if owner == target_name: #for skipping target class methods
            continue

        if callable_uses_type(method, target_name):
            users.add(fullname)

    return len(users)
