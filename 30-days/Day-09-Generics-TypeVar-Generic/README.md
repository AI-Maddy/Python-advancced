# Day 09 — Generics, TypeVar, and Generic

Write type-safe generic classes and functions using `TypeVar` and `Generic[T]`. Understand how Python's generics relate to C++ templates.

## C++ Equivalent
Day 09 of the C++ OOP course (function templates, class templates `template<typename T>`).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: `TypeVar`, `Generic[T]`, bounded type vars, `ParamSpec`, `Concatenate` |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day09.py` | pytest suite |

## Key Concepts

- `TypeVar("T")` — declares a generic type variable
- `Generic[T]` — base class for generic classes
- Bounded type vars: `TypeVar("T", bound=Comparable)`
- Constrained type vars: `TypeVar("T", int, str)`
- `ParamSpec` — captures callable parameter specs
- Generic functions vs generic classes

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
