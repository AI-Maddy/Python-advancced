# Day 00 — Setup and Basics

Set up a reliable Python development environment: interpreter, virtual environment, package manager, and tooling. Learn the Python execution model and REPL fundamentals.

## C++ Equivalent
Day 00 of the C++ OOP 30-day course (toolchain setup: compiler, CMake, IDE).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: execution model, venv, pip, `__name__`, REPL tips |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day00.py` | pytest suite |

## Key Concepts

- Python installation, `python -m venv .venv`, `pip install`
- Running Python: interactive REPL, script, `-m` flag
- `print()`, `help()`, `type()`, `dir()`
- `__name__ == "__main__"` guard
- Bytecode / `__pycache__` overview
- `pyproject.toml` and `pytest.ini` basics

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
