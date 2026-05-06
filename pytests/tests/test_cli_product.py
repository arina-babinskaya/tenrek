import io
from pathlib import Path

import pytest
from rich.console import Console
from typer.testing import CliRunner

from tenrek.cli import app
import tenrek.cli as cli


SAMPLES = Path(__file__).parent / "cpp_samples"


@pytest.fixture
def runner():
    return CliRunner()


def test_metrics_command_lists_all_metrics(runner):
    result = runner.invoke(app, ["metrics"])

    assert result.exit_code == 0
    assert "Available metrics" in result.stdout
    assert "cyclomatic" in result.stdout
    assert "Cognitive Complexity" in result.stdout
    assert "maintainability_index" in result.stdout


def test_metrics_command_shows_single_metric_help(runner):
    result = runner.invoke(app, ["metrics", "cyclomatic"])

    assert result.exit_code == 0
    assert "cyclomatic" in result.stdout
    assert "Cyclomatic Complexity" in result.stdout
    assert "Available metrics" not in result.stdout


def test_metrics_command_fails_for_unknown_metric(runner):
    result = runner.invoke(app, ["metrics", "does_not_exist"])

    assert result.exit_code == 1
    assert "Unknown metric" in result.stdout
    assert "does_not_exist" in result.stdout


def test_file_command_analyzes_cpp_file(runner):
    result = runner.invoke(app, ["file", str(SAMPLES / "simple.cpp")])

    assert result.exit_code == 0
    assert "Analyzing file" in result.stdout
    assert "Analysis result" in result.stdout
    assert "add" in result.stdout
    assert "cyclomatic" in result.stdout
    assert "1" in result.stdout


def test_folder_command_respects_exclude_pattern(runner):
    result = runner.invoke(
        app,
        [
            "folder",
            str(SAMPLES),
            "--exclude",
            "exclude_me.cpp",
        ],
    )

    assert result.exit_code == 0
    assert "Analysis result" in result.stdout
    assert "excluded_function_should_not_appear" not in result.stdout


def test_show_result_renders_ansi_colors_for_metric_values(monkeypatch):
    stream = io.StringIO()

    monkeypatch.setattr(
        cli,
        "console",
        Console(
            file=stream,
            force_terminal=True,
            color_system="standard",
            width=140,
        ),
    )

    cli.show_result(
        [
            {
                "name": "bad_func",
                "type": "function",
                "cyclomatic": 21,
            },
            {
                "name": "ok_func",
                "type": "function",
                "cyclomatic": 2,
            },
        ],
        "sample.cpp",
    )

    output = stream.getvalue()

    assert "\x1b[" in output
    assert "21" in output
    assert "2" in output
    assert "\x1b[31m21\x1b[0m" in output
    assert "\x1b[32m2\x1b[0m" in output