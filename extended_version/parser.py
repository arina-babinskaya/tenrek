import clang.cindex

import os
lib_path = '/opt/homebrew/opt/llvm/lib/libclang.dylib'
if os.path.exists(lib_path):
    clang.cindex.Config.set_library_file(lib_path)
# я потом поменяю 4 строчки выше - это мой временный костыль

class CppParser:
    def __init__(self):
        self.index = clang.cindex.Index.create() #make main odject

    def parse_file(self, file_path):
        tu = self.index.parse(file_path, args=['-std=c++20']) #translation unit

        for diag in tu.diagnostics:
            print(f"Clang Error: {diag}")

        funcs = []

        for node in tu.cursor.walk_preorder(): #recursive (all functions will be detected)
            if node.kind == clang.cindex.CursorKind.FUNCTION_DECL: #need function type only
                if node.location.file and node.location.file.name == file_path:
                    func_data = {
                        "name": node.spelling,
                        "return_type": node.result_type.spelling, 
                        "args": [{"type": arg.type.spelling, "name": arg.spelling} 
                                 for arg in node.get_arguments()]
                    }
                    funcs.append(func_data)
        return funcs


