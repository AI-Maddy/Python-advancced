# Adapter Pattern

Converts the interface of a class into another interface that clients expect. Allows classes with incompatible interfaces to work together. Two variants: object adapter (composition) and class adapter (multiple inheritance).

## C++ Equivalent
Class adapter inherits from both Target and Adaptee; object adapter holds a pointer to the Adaptee and forwards calls.

## Files

| File | Description |
|---|---|
| `adapter.py` | Core implementation: `Target` ABC, `Adaptee` (legacy), `ObjectAdapter`, `ClassAdapter` |
| `example_1.py` | Legacy payment gateway adapted to a modern payment interface |
| `example_2.py` | Third-party XML library adapted to a JSON interface |
| `tests/test_adapter.py` | pytest suite |

## Run

```bash
python adapter.py                   # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Target` — ABC with `request() -> str` (what the client expects)
- `Adaptee` — legacy class with `specific_request()` and `legacy_compute()`
- `ObjectAdapter` — wraps `Adaptee` via composition
- `ClassAdapter` — inherits from both `Target` and `Adaptee`
