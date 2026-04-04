import os
from parser import CppParser
from generator import generate_test, wrap_tests


def main():
    input_path = "level1.cpp"
    output_path = "generated_tests.cpp"

    parser = CppParser()
    funcs = parser.parse_file(input_path)

    all_tests_code = ""
    for f in funcs:
        all_tests_code += generate_test(f)
    
    print("Parsed funcs:", funcs)
    final = wrap_tests(all_tests_code, input_path)
    with open(output_path, "w") as f:
        f.write(final)
        print(f"Tests generated: {len(funcs)}.")


if __name__ == "__main__":
    main()

