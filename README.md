# Tenrek

Tenrek is a C++ code complexity analyzer based on Clang AST.

It analyzes C++ files and folders and reports code metrics such as cyclomatic complexity, cognitive complexity, nesting depth, lines of code, Halstead metrics, fan-in/fan-out, cohesion metrics, and class size indicators.

## Features

* Analyze a single C++ file
* Analyze all `.cpp` files in a folder
* Exclude files by pattern
* Support C++ standards: `cpp11`, `cpp14`, `cpp17`, `cpp20`, `cpp23`
* Display metric values in color:

  * green — good
  * yellow — warning
  * red — needs attention
* Show descriptions for all supported metrics

## Install

```bash
pip install tenrek
```

Tenrek uses Python bindings for Clang. You also need `libclang` installed on your system.

### macOS

```bash
brew install llvm
```

If `libclang` is not found automatically:

```bash
export LIBCLANG_PATH="/opt/homebrew/opt/llvm/lib/libclang.dylib"
```

## Usage

Analyze a single file:

```bash
tenrek file main.cpp
```

Analyze a folder:

```bash
tenrek folder src
```

Analyze a folder and exclude files by pattern:

```bash
tenrek folder src --exclude "*.hpp"
```

Use a specific C++ standard:

```bash
tenrek file main.cpp --standard cpp20
```

Show all available metrics:

```bash
tenrek metrics
```

Show help for one metric:

```bash
tenrek metrics cyclomatic
```

## Supported metrics

* `cyclomatic`
* `cognitive_complexity`
* `nesting`
* `loc`
* `nloc`
* `longest_string`
* `average_string_lenght`
* `maintainability_index`
* `fan_in`
* `fan_out`
* `god_class`
* `lcom1`
* `lcom4`
* `halstead_uniq_elements`
* `halstead_all_elements`
* `halstead_volume`
* `halstead_difficulty`
* `halstead_effort`
* `halstead_time`

## Example

```bash
tenrek file examples/main.cpp
```

Example output:

```text
Analysis result of examples/main.cpp

Name        Type      Metric                  Value
main        function  cyclomatic              2
main        function  cognitive_complexity    1
main        function  nesting                 1
main        function  loc                     12
```

Metric values are colored according to their severity.

## Development

Clone the repository:

```bash
git clone https://github.com/arina-babinskaya/tenrek
cd tenrek
```

Create a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install the project locally:

```bash
python -m pip install -e .
```

Install test dependencies:

```bash
python -m pip install pytest
```

Run tests:

```bash
python -m pytest -q
```

## Build package

```bash
python -m pip install build twine
python -m build
twine check dist/*
```

## License

MIT
