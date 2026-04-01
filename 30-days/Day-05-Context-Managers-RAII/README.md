# Day 05 — Context Managers and RAII

Python's deterministic resource management idiom using the `with` statement. Covers class-based and generator-based context managers, and standard library helpers from `contextlib`.

## C++ Equivalent
Day 05 of the C++ OOP course (RAII, `unique_ptr`, `lock_guard`, destructor guarantees).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: `__enter__`/`__exit__`, `@contextmanager`, `contextlib.suppress`, `contextlib.closing` |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day05.py` | pytest suite |

## Key Concepts

- `with` statement and the context manager protocol
- `__enter__` — setup; return value bound to `as` target
- `__exit__(exc_type, exc_val, exc_tb)` — teardown; return `True` to suppress exceptions
- `@contextmanager` — generator-based shortcut (try/yield/finally)
- `contextlib.suppress` — silences specified exception types
- `contextlib.closing` — wraps any object with a `close()` method

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
