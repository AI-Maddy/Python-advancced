# Context Manager Idiom

Python's equivalent of C++ RAII. Guarantees that setup and teardown code runs even when exceptions occur, using the `with` statement and `__enter__`/`__exit__` protocol.

## C++ Equivalent
RAII — `unique_ptr`, `lock_guard`, custom destructors; the resource is tied to object lifetime.

## Files

| File | Description |
|---|---|
| `context_manager.py` | Core implementation: `FileManager` (class-based), `@contextmanager` generator form, `contextlib.suppress`, `contextlib.closing` |
| `example_1.py` | Database connection context manager |
| `example_2.py` | Timing and resource-tracking context managers |
| `tests/test_context_manager.py` | pytest suite |

## Run

```bash
python context_manager.py           # demo
python -m pytest tests/ -v          # tests
```

## Key Concepts

- `__enter__` / `__exit__` — class-based protocol
- `@contextmanager` — generator-based shortcut via `contextlib`
- `contextlib.suppress` — silences specified exceptions
- `contextlib.closing` — wraps objects with a `close()` method
