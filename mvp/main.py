from mvp.mvp_parser import parse_func
from mvp.mvp_generator import generate_test
from mvp.mvp_template import wrap_tests


def main():
    with open("examples/mvp_sample.cpp") as f:
        code = f.read()

    funcs = parse_func(code)

    test = ""
    for fn in funcs:
        test += generate_test(fn)

    final = wrap_tests(test)

    with open("mvp/output.cpp", "w") as f:
        f.write(final)

if __name__ == "__main__":
    main()
