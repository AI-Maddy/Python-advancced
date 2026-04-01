# Day 12 — Iterators and Generators

Implement Python's iterator protocol with `__iter__`/`__next__`, and write memory-efficient lazy pipelines with generator functions and `yield from`.

## C++ Equivalent
Day 12 of the C++ OOP course (iterators, `begin()`/`end()`, range-based `for`, `std::generator` C++23).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: custom iterators, generator functions, generator expressions, `yield from`, pipelines |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day12.py` | pytest suite |

## Key Concepts

- Iterator protocol: `__iter__()` returns `self`; `__next__()` raises `StopIteration`
- `iter()` / `next()` built-in functions
- Generator functions with `yield` — lazy, memory-efficient
- Generator expressions: `(expr for x in iterable)`
- `yield from` — delegate to a sub-iterator
- Pipeline pattern: chain generators for data transformation

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
