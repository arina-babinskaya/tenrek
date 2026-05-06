from clang.cindex import CursorKind

def collect_methods(class_cursor):
    accepted = {
        CursorKind.CXX_METHOD,
        CursorKind.CONSTRUCTOR,
        CursorKind.DESTRUCTOR,
    }

    result = []

    for child in class_cursor.get_children():
        if child.kind in accepted:
            result.append(child)

    return result


def collect_fields(class_cursor):
    result = set()

    for child in class_cursor.get_children():
        if child.kind == CursorKind.FIELD_DECL:
            result.add(child.spelling)

    return result


def method_key(cursor):
    usr = cursor.get_usr()
    if usr: return usr

    return f"{cursor.spelling}:{cursor.displayname}:{cursor.location.line}"