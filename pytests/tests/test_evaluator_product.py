import pytest

from tenrek.evaluator import MetricEvaluator


@pytest.fixture
def evaluator():
    return MetricEvaluator()


@pytest.mark.parametrize(
    ("metric", "value", "expected"),
    [
        ("cyclomatic", 10, "green"),
        ("cyclomatic", 11, "yellow"),
        ("cyclomatic", 20, "yellow"),
        ("cyclomatic", 21, "red"),
        ("cognitive_complexity", 25, "green"),
        ("cognitive_complexity", 26, "yellow"),
        ("cognitive_complexity", 41, "red"),
        ("nesting", 3, "green"),
        ("nesting", 4, "yellow"),
        ("nesting", 6, "red"),
        ("loc", 40, "green"),
        ("loc", 41, "yellow"),
        ("loc", 81, "red"),
        ("nloc", 30, "green"),
        ("nloc", 31, "yellow"),
        ("nloc", 61, "red"),
        ("lcom4", 1, "green"),
        ("lcom4", 2, "yellow"),
        ("lcom4", 4, "red"),
    ],
)
def test_lower_is_better_threshold_boundaries(evaluator, metric, value, expected):
    assert evaluator.evaluate(metric, value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (20, "green"),
        (10, "yellow"),
        (9, "red"),
    ],
)
def test_maintainability_index_uses_higher_is_better_scale(evaluator, value, expected):
    assert evaluator.evaluate("maintainability_index", value) == expected


@pytest.mark.parametrize("value", [None, "12", True, float("nan"), float("inf")])
def test_invalid_values_are_unknown(evaluator, value):
    assert evaluator.evaluate("cyclomatic", value) == "unknown"


def test_evaluate_result_adds_verdict_fields_without_touching_identity_fields(evaluator):
    result = {
        "name": "foo",
        "type": "function",
        "start_line": 1,
        "end_line": 3,
        "cyclomatic": 2,
        "maintainability_index": 25,
    }

    evaluated = evaluator.evaluate_result(result)

    assert evaluated["name"] == "foo"
    assert evaluated["cyclomatic_verdict"] == "green"
    assert evaluated["maintainability_index_verdict"] == "green"
    assert "name_verdict" not in evaluated
    assert "type_verdict" not in evaluated
