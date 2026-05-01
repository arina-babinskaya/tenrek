import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from typing import Literal
import fnmatch


app = typer.Typer(help="Tenrek is C++ code complexity analyzer tool")
console = Console()


def make_clang_args(standard: str):
    return [f"-std=c++{standard[-2:]}"]


def analyze_file(path: Path, standard: str):
    from tenrek.parser import CppParser
    from tenrek.analyzer import ComplexityAnalyzer

    parser = CppParser(path, standard=standard)
    parser.parse()

    analyzer = ComplexityAnalyzer(parser, standard=standard)
    return analyzer.analyze()


def show_result(result: list, file_name):
    table = Table(title=f"Analysis result of {file_name}")

    table.add_column("Name", style="cyan")
    table.add_column("Type")
    table.add_column("Metric")
    table.add_column("Value", style="magenta")

    for item in result:
        name = item.get("name", "")
        typ = item.get("type", "")

        for key, value in item.items():
            if key in ["name", "type"]:
                continue
            table.add_row(name, typ, key, str(value))

    console.print(table)


def show_multiple(results: list, file_names):
    for i in range(len(file_names)):
        show_result(results[i], file_names[i])


@app.command()
def file(
    path: Path = typer.Argument(..., exists=True),
    standard: str = typer.Option(
        "cpp17",
        "--standard",
        help="Write correct C++ standard (e.g cpp17)"
    ),
):
    """
    Analyze single file
    """

    allowed = {"cpp11", "cpp14", "cpp17", "cpp20", "cpp23"}
    if standard not in allowed:
        raise typer.BadParameter("Use cpp11/cpp14/cpp17/cpp20/cpp23")

    console.print(f"[bold green]Analyzing file:[/bold green] {path}")

    result = analyze_file(path, standard)

    show_result(result, path)


@app.command()
def folder(
    path: Path = typer.Argument(..., exists=True),
    standard: str = typer.Option(
        "cpp17",
        "--standard", 
        help="Write correct C++ standard (e.g cpp17)"
    ),
    exclude: list[str] = typer.Option(
        None,
        "--exclude",
        help="Exclude file or pattern (can be used multiple times)"
    ),
):
    """
    Analyze folder
    """

    allowed = {"cpp11", "cpp14", "cpp17", "cpp20", "cpp23"}
    if standard not in allowed:
        raise typer.BadParameter("Use cpp11/cpp14/cpp17/cpp20/cpp23")

    console.print(f"[bold blue]Analyzing folder:[/bold blue] {path}")

    results = []
    patterns = ["*.cpp", "*.hpp", "*.h"]
    file_names = []

    for pattern in patterns:
        for file in path.rglob(pattern):
            relative = str(file.relative_to(path))

            if any(fnmatch.fnmatch(relative, ex) for ex in exclude):
                console.print(f"[yellow]Skipped:[/yellow] {relative}")
                continue

            results.append(analyze_file(file, standard))
            file_names.append(relative)

    show_multiple(results, file_names)


if __name__ == "__main__":
    app()