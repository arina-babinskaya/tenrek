from clang.cindex import CursorKind

def calculate(node):
    complexity = 1

    for n in node.walk_preorder():
        if n.kind in [
            CursorKind.IF_STMT,
            CursorKind.FOR_STMT,
            CursorKind.WHILE_STMT,
            CursorKind.CASE_STMT,
            CursorKind.DEFAULT_STMT,
            CursorKind.CONDITIONAL_OPERATOR
        ]:
            complexity += 1

    return complexity