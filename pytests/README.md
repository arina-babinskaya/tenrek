# Tenrek product tests

These tests check the project as a user-facing CLI tool, not only isolated metric functions.

## What is covered

- `tenrek metrics`
- `tenrek metrics <metric_name>`
- unknown metric error handling
- `tenrek file <path>`
- `tenrek folder <path> --exclude <pattern>`
- colored metric/verdict rendering through Rich
- evaluator threshold boundaries
- `god_class` returning one integer for one class: `methods + fields`

## How to install test dependencies

```bash
pip install pytest
```

If your project is not installed as a package yet:

```bash
pip install -e .
```

## How to run

```bash
pytest -q
```

Run only CLI product tests:

```bash
pytest -q tests/test_cli_product.py
```

Run only evaluator tests:

```bash
pytest -q tests/test_evaluator_product.py
```

## Expected assumptions

These tests assume your CLI contains:

```python
app = typer.Typer(...)
```

and that `tenrek.cli` exposes:

```python
app
show_result
```

They also assume your `MetricEvaluator` uses these effective boundaries:

- cyclomatic: green <= 10, yellow <= 20, red > 20
- cognitive_complexity: green <= 25, yellow <= 40, red > 40
- maintainability_index: green >= 20, yellow >= 10, red < 10

If you deliberately choose different thresholds, update the parametrized values in
`tests/test_evaluator_product.py`.
