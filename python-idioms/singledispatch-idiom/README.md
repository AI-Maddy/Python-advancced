# Singledispatch Idiom

`@functools.singledispatch` provides type-based function overloading. The generic function dispatches to the most specific registered implementation based on the type of its first argument.

## C++ Equivalent
Function overloading; tag dispatch; `if constexpr` template specialisation.

## Files

| File | Description |
|---|---|
| `singledispatch_idiom.py` | Core implementation: `@singledispatch` serialiser, `@singledispatchmethod` on a class method |
| `example_1.py` | Type-aware pretty-printer dispatching on int, float, list, dict |
| `example_2.py` | Shape area calculator using `singledispatchmethod` |
| `tests/test_singledispatch_idiom.py` | pytest suite |

## Run

```bash
python singledispatch_idiom.py      # demo
python -m pytest tests/ -v          # tests
```

## Key Concepts

- `@singledispatch` — register a generic fallback; use `@func.register(type)` for specialisations
- `@singledispatchmethod` (Python 3.8+) — same as `singledispatch` but for class/instance methods
- Dispatch order — most specific type wins; falls back to the base `object` handler
- Runtime introspection — `func.dispatch(type)` returns the implementation that would be called
