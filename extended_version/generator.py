from typing import Dict
import itertools
import os
from analyzer import get_values

def generate_arg_combinations(args):
    value_lists = [get_values(arg["type"]) for arg in args]

    if not value_lists:
        return [[]]
    return list(itertools.product(*value_lists))

def generate_test(func: Dict) -> str:
    name = func["name"]
    return_type = func["return_type"]
    args = func["args"]

    combinations = generate_arg_combinations(args)
    tests = ""

    for i, combo in enumerate(combinations):
        args_str = ", ".join(combo)

        if return_type == "void":
            body = f"{name}({args_str});\n    SUCCEED();"
        else:
            body = f"    auto result = {name}({args_str});\n" \
                   f"    EXPECT_EQ(result, /*?*/);"

        tests += f"\nTEST({name}Test, Case{i}) {{\n{body}\n}}\n"
    return tests

def wrap_tests(tests: str, source_file: str) -> str:
    header_name = os.path.basename(source_file)
    return f"""#include <gtest/gtest.h>
#include "{header_name}"

{tests}

#ifndef HAS_CUSTOM_MAIN
int main(int argc, char **argv) {{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}}
#endif
"""
