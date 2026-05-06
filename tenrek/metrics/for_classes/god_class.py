from clang.cindex import CursorKind


def calculate(node):
    methods = 0
    fields = 0

    for child in node.get_children():
        if child.kind == CursorKind.CXX_METHOD:
            methods += 1

        elif child.kind == CursorKind.FIELD_DECL:
            fields += 1

    return methods + fields