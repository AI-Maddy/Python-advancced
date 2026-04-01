# Day 13 — Decorators In Depth

Master Python's decorator system: simple wrappers, parameterised decorator factories, class-based decorators, stacking order, and standard library decorators.

## C++ Equivalent
Day 13 of the C++ OOP course (higher-order function templates, `std::function` wrappers, policy classes).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: `@functools.wraps`, decorator factories, class-based decorators, stacking, `lru_cache`, `cached_property` |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day13.py` | pytest suite |

## Key Concepts

- Simple decorator: `def decorator(func): ... return wrapper`
- `@functools.wraps(func)` — preserve `__name__`, `__doc__`, `__wrapped__`
- Parameterised decorator factory: decorator that takes arguments
- Class-based decorator: `__init__` wraps the function; `__call__` invokes it
- Stacking: decorators apply bottom-up; call order is top-down
- `@functools.lru_cache`, `@functools.cache`, `@functools.cached_property`

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
