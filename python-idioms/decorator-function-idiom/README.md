# Decorator Function Idiom

Higher-order functions that wrap other functions to add behaviour (logging, caching, retrying, timing) without modifying the wrapped function. `@functools.wraps` preserves the original function's metadata.

Note: this is Python's `@decorator` syntax, which is distinct from the GoF structural Decorator pattern (covered in `structural/decorator-pattern`).

## C++ Equivalent
Higher-order function templates; policy-based design; wrapper classes with `operator()`.

## Files

| File | Description |
|---|---|
| `decorator_function.py` | Core implementation: `log_calls`, parameterised decorator factory, class-based decorator, `@functools.lru_cache`, `@functools.cached_property` |
| `example_1.py` | Retry, rate-limit, and timing decorators |
| `example_2.py` | Authentication and validation decorators for web-style handlers |
| `tests/test_decorator_function.py` | pytest suite |

## Run

```bash
python decorator_function.py        # demo
python -m pytest tests/ -v          # tests
```

## Key Concepts

- `@functools.wraps` — preserves `__name__`, `__doc__`, `__wrapped__`
- Parameterised decorator — decorator factory that returns a decorator
- Class-based decorator — `__init__` wraps the function; `__call__` invokes it
- `@functools.lru_cache` / `@functools.cache` — memoisation
- `@functools.cached_property` — lazy computed attribute cached after first access
