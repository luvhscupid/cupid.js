# Calculator Handoff Specification

## Purpose

Build a tiny Python 3 calculator as an integration test of the Cloud Codex ↔ Local Codex workflow. Use only Python's standard library.

## Interface

Create `calculator.py` with four module-level functions:

- `add(a, b)` returns `a + b`.
- `subtract(a, b)` returns `a - b`.
- `multiply(a, b)` returns `a * b`.
- `divide(a, b)` returns `a / b`.

Each function accepts numeric `int` or `float` operands and returns Python's normal arithmetic result. Division uses true division; division by zero raises Python's `ZeroDivisionError`. No command-line interface or third-party package is required.

Create `test_calculator.py` with tests using `unittest` from the standard library.

## Acceptance criteria

- All four functions implement the specified operations.
- Tests cover each operation, including negative or fractional values where useful, and assert division by zero raises `ZeroDivisionError`.
- Tests run from this directory with `python -m unittest -v` (or the platform's Python 3 launcher equivalent).
- Only Python 3 standard-library features are used.
- Local Codex records the exact command and result in `CHECKPOINT.md`.
- No unrelated project files are changed.
