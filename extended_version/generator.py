from typing import Dict
import itertools
import os
from analyzer import get_values, normalize_type

def generate_arg_combinations(args):
    value_lists = [get_values(arg["type"]) for arg in args]

    if not value_lists:
        return [[]]
    return list(itertools.product(*value_lists))


def generate_assert(return_type: str) -> str:
    rt = normalize_type(return_type)

    if rt == "void":
        return "SUCCEED();"

    if rt == "bool":
        return "EXPECT_TRUE(result);  // or EXPECT_FALSE"

    if rt in {"float", "double"}:
        return "EXPECT_NEAR(result, /*expected*/, 1e-5);"

    if "*" in return_type:
        return "EXPECT_NE(result, nullptr);"

    return "EXPECT_EQ(result, /*expected*/);"


def generate_test(func: Dict) -> str:
    name = func["name"]
    return_type = func["return_type"]
    args = func["args"]

    suite_name = format_test_suite_name(name) # for test name
    combinations = generate_arg_combinations(args)
    tests = ""

    for i, combo in enumerate(combinations):
        args_str = ", ".join(combo)
        case_name = generate_case_name(args, combo) # for case name

        if not case_name:
            case_name = f"Case{i}"

        if normalize_type(return_type) == "void":
            body = f"{name}({args_str});\n    SUCCEED();"
        else:
            assertion = generate_assert(return_type)
            body = (
                f"auto result = {name}({args_str});\n"
                f"    {assertion}"
            )

        tests += f"""
TEST({suite_name},{case_name}) {{
    {body}
}}
"""
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

#for meaningful tests' names

def generate_case_name(args, values):
    parts = []

    for arg, val in zip(args, values):
        name = arg["name"]

        if val in {"0", "0.0"}:
            parts.append(f"{name}Zero")
        elif val in {"1", "1.0"}:
            parts.append(f"{name}One")
        elif val in {"-1", "-1.0"}:
            parts.append(f"{name}Negative")
        
        elif val in {str(2**15 - 1), str(2**31 - 1), str(2**63 - 1), "3.4e38", "1.7e308"}:
            parts.append(f"{name}Max_Val")
        elif val in {str(-2**15), str(-2**31), str(-2**63), "-3.4e38", "-1.7e308"}:
            parts.append(f"{name}Min_Val")
# пока не трогаю char и string
# ВАЖНО: нужно будет учесть, что long long * long long по размеру больше просто long long

        elif val == "true":
            parts.append(f"{name}True")
        elif val == "false":
            parts.append(f"{name}False")
        elif val == "nullptr":
            parts.append(f"{name}Null")
        elif val == '""':
            parts.append(f"{name}Empty")
        elif val.startswith('"'):
            parts.append(f"{name}String")
        else:
            parts.append(f"{name}Val")

    return "_".join(parts)
# TO DO: add edge cases!!!!

def format_test_suite_name(func_name: str) -> str:
    return func_name[0].upper() + func_name[1:] + "_Test"