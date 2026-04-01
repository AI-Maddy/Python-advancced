# Day 01 — Variables, Types, and Literals

Explore Python's built-in type system. Understand dynamic typing, type annotations, truthiness, and the differences from C++ static typing.

## C++ Equivalent
Day 01 of the C++ OOP course (primitive types, literals, `auto`, type widening).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: numeric types, strings, f-strings, `type()`, `isinstance()` |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day01.py` | pytest suite |

## Key Concepts

- `int`, `float`, `complex`, `bool`, `str`, `bytes`
- Arbitrary-precision integers (vs C++ fixed-width)
- Dynamic typing vs static typing; PEP 526 type annotations
- `None` type, truthiness, `is` vs `==`
- f-strings, string methods
- `type()`, `isinstance()`, `issubclass()`

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
