# Day 02 — Functions, Lambdas, and Closures

Master Python's first-class function model: positional and keyword arguments, variadic signatures, lambda expressions, closures, and higher-order functions.

## C++ Equivalent
Day 02 of the C++ OOP course (functions, `std::function`, lambdas, function pointers).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: function definitions, `*args`/`**kwargs`, closures, `functools` |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day02.py` | pytest suite |

## Key Concepts

- `def`, positional vs keyword arguments, default values
- `*args`, `**kwargs`, keyword-only arguments (`*,`)
- `lambda` expressions
- Closures and `nonlocal`
- Higher-order functions: `map`, `filter`, `functools.reduce`
- `functools.partial` for partial application

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
