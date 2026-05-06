from itertools import combinations
from clang.cindex import CursorKind
from .lcom_help_functions import (
    collect_methods,
    collect_fields,
    method_key
)


def calculate(class_cursor):
    """
    Industrial-grade LCOM1 (Chidamber & Kemerer) for C++ via libclang.

    Supports:
    - fields in any access section
    - constructors / destructors optional ignore
    - overloaded methods
    - static methods
    - inherited field access (if visible in AST)
    - nested expressions
    - templates (as parsed by clang)

    Returns:
        int
    """

    fields = collect_fields(class_cursor)
    methods = collect_methods(class_cursor)

    if len(methods) < 2:
        return 0

    usage = {}

    for method in methods:
        key = method_key(method)
        usage[key] = collect_used_fields(method, fields)

    p, q = 0, 0

    method_keys = list(usage.keys())

    for m1, m2 in combinations(method_keys, 2):
        if usage[m1] & usage[m2]: q += 1
        else: p += 1

    return max(p - q, 0)


def collect_used_fields(method_cursor, class_fields):
    used = set()

    def walk(node):
        kinds = {
            CursorKind.MEMBER_REF_EXPR,
            CursorKind.DECL_REF_EXPR,
            CursorKind.UNEXPOSED_EXPR,
        }

        if node.kind in kinds:
            name = node.spelling
            if name in class_fields:
                used.add(name)

        for c in node.get_children():
            walk(c)

    walk(method_cursor)
    return used