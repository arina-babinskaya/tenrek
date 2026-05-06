from pathlib import Path
from tenrek.parser import CppParser
from fnmatch import fnmatch


class FolderParser:
    def __init__(self, folder, standard="cpp17", exclude=None):
        self.folder = Path(folder)
        self.standard = standard
        self.exclude = exclude or []
        self.parsers = []


    # do not acount excluded files 
    def _is_excluded(self, file: Path):
        relative = str(file.relative_to(self.folder))

        return any(
            fnmatch(relative, pattern)
            for pattern in self.exclude
        )


    def parse(self):
        files = list(self.folder.rglob("*.cpp"))

        for file in files:
            if self._is_excluded(file):
                continue

            p = CppParser(str(file), self.standard)
            p.parse()
            self.parsers.append(p)


    def _collect(self, method_name):
        result = []
        seen = set()

        for parser in self.parsers:
            items = getattr(parser, method_name)()

            for item in items:
                key = item.get_usr()

                if key not in seen:
                    seen.add(key)
                    result.append(item)

        return result
    

    def _delegate(self, method_name, node):
        for parser in self.parsers:
            try:
                return getattr(parser, method_name)(node)
            except Exception:
                continue

        raise ValueError(f"Node not found in any parser: {node.spelling}")
    

    def get_classes(self):
        return self._collect("get_classes")

    def get_functions(self):
        return self._collect("get_functions")

    def get_methods(self):
        return self._collect("get_methods")


    def get_function_info(self, node):
        return self._delegate("get_function_info", node)

    def get_class_info(self, node):
        return self._delegate("get_class_info", node)