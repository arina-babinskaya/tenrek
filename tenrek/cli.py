import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from typing import Optional


app = typer.Typer(help="Tenrek is C++ code complexity analyzer tool")
console = Console()


METRIC_DESCRIPTIONS = {
    "cyclomatic": (
        "Cyclomatic Complexity: number of independent execution paths "
        "through the code."
    ),

    "cognitive_complexity": (
        "Cognitive Complexity: measures how difficult the code is "
        "for a human to understand."
    ),

    "nesting": (
        "Maximum nesting depth of control structures "
        "(if/for/while/switch/etc)."
    ),

    "loc": (
        "Lines of Code: total number of lines."
    ),

    "nloc": (
        "Non-empty Lines of Code: number of non-blank lines."
    ),

    "longest_string": (
        "Length of the longest line in the source file."
    ),

    "average_string_lenght": (
        "Average line length in the source file."
    ),

    "maintainability_index": (
        "Maintainability Index: overall maintainability score. "
        "Higher values are better."
    ),

    "fan_in": (
        "Fan-in: number of external elements "
        "that depend on this element."
    ),

    "fan_out": (
        "Fan-out: number of external elements "
        "used by this element."
    ),

    "god_class": (
        "God Class metric: total number of methods and fields "
        "inside the class."
    ),

    "lcom1": (
        "LCOM1 (Lack of Cohesion of Methods): "
        "measures how unrelated class methods are."
    ),

    "lcom4": (
        "LCOM4: number of connected components in a class. "
        "1 means cohesive; values greater than 1 may indicate "
        "that the class should be split."
    ),

    "halstead_uniq_elements": (
        "Halstead Unique Elements: number of unique operators "
        "and operands."
    ),

    "halstead_all_elements": (
        "Halstead Total Elements: total number of operators "
        "and operands."
    ),

    "halstead_volume": (
        "Halstead Volume: estimated implementation size "
        "based on vocabulary and program length."
    ),

    "halstead_difficulty": (
        "Halstead Difficulty: estimated difficulty "
        "of understanding or writing the code."
    ),

    "halstead_effort": (
        "Halstead Effort: estimated effort required "
        "to implement or maintain the code."
    ),

    "halstead_time": (
        "Halstead Time: estimated implementation time "
        "derived from Halstead Effort."
    ),
}


def run_analysis(parser, standard):
    from tenrek.analyzer import ComplexityAnalyzer

    analyzer = ComplexityAnalyzer(parser, standard=standard)
    return analyzer.analyze()


def analyze_file(path: Path, standard: str):
    from tenrek.parser import CppParser

    parser = CppParser(path, standard=standard)
    parser.parse()

    return run_analysis(parser, standard)


def analyze_folder(path: Path, standard: str, exclude: list[str]):
    from tenrek.folder_parser import FolderParser

    parser = FolderParser(path, standard=standard, exclude=exclude or [])
    parser.parse()

    return run_analysis(parser, standard)


def validate_standard(standard):
    allowed = {"cpp11", "cpp14", "cpp17", "cpp20", "cpp23"}

    if standard not in allowed:
        raise typer.BadParameter("Use cpp11/cpp14/cpp17/cpp20/cpp23")


def format_metric_value(value):
    if isinstance(value, float):
        return f"{value:.3f}"

    return str(value)


def colorize_value(value, verdict: str) -> str:
    if verdict == "green":
        return f"[green]{value}[/green]"

    if verdict == "yellow":
        return f"[yellow]{value}[/yellow]"

    if verdict == "red":
        return f"[red]{value}[/red]"

    return str(value)


def show_result(result: list[dict], file_name):
    from tenrek.evaluator import MetricEvaluator

    evaluator = MetricEvaluator()

    table = Table(title=f"Analysis result of {file_name}")

    table.add_column("Name", style="cyan")
    table.add_column("Type")
    table.add_column("Metric")
    table.add_column("Value")

    skip_fields = {
        "name",
        "type",
        "start_line",
        "end_line",
        "bases",
    }

    for item in result:
        name = item.get("name", "")
        typ = item.get("type", "")

        for key, value in item.items():
            if key in skip_fields:
                continue

            verdict = evaluator.evaluate(key, value)
            formatted_value = format_metric_value(value)
            colored_value = colorize_value(formatted_value, verdict)

            table.add_row(
                name,
                typ,
                key,
                colored_value,
            )

    console.print(table)


@app.command()
def file(
    path: Path = typer.Argument(..., exists=True),
    standard: str = typer.Option("cpp17", "--standard"),
):
    """
    Analyze single file
    """

    validate_standard(standard)

    console.print(f"[bold green]Analyzing file:[/bold green] {path}")

    result = analyze_file(path, standard)

    show_result(result, path)


@app.command()
def folder(
    path: Path = typer.Argument(..., exists=True),
    standard: str = typer.Option("cpp17", "--standard"),
    exclude: list[str] = typer.Option(
        None,
        "--exclude",
        help="Exclude file or pattern (can be used multiple times)",
    ),
):
    """
    Analyze folder
    """

    validate_standard(standard)

    console.print(f"[bold blue]Analyzing folder:[/bold blue] {path}")

    result = analyze_folder(path, standard, exclude or [])

    show_result(result, path)


@app.command()
def metrics(
    name: Optional[str] = typer.Argument(
        None,
        help="Metric name. If omitted, shows all metrics.",
    )
):
    """
    Show metric descriptions
    """

    if name is not None:
        description = METRIC_DESCRIPTIONS.get(name)

        if description is None:
            console.print(f"[red]Unknown metric:[/red] {name}")
            console.print("Use [bold]tenrek metrics[/bold] to see all available metrics.")
            raise typer.Exit(code=1)

        console.print(f"[bold cyan]{name}[/bold cyan]")
        console.print(description)
        return

    table = Table(title="Available metrics")

    table.add_column("Metric", style="cyan")
    table.add_column("Description")

    for metric_name, description in sorted(METRIC_DESCRIPTIONS.items()):
        table.add_row(metric_name, description)

    console.print(table)


if __name__ == "__main__":
    app()