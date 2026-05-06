def calculate(node):
    tu = node.translation_unit
    includes = set()

    try:
        for inc in tu.get_includes():
            if inc.include:
                includes.add(inc.include.name)
    except Exception:
        pass

    return {
        "includes": len(includes),
        "include_list": list(includes)
    }
