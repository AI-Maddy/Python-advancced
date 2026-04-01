# Descriptor Idiom

Descriptors implement `__get__`, `__set__`, and/or `__delete__` to customise attribute access at the class level. They are the mechanism behind `@property`, `classmethod`, and `staticmethod`.

## C++ Equivalent
Operator overloading on proxy objects; member access control via private members and accessor methods.

## Files

| File | Description |
|---|---|
| `descriptor.py` | Core implementation: `Validated` (data descriptor), `Typed`, `Clamped`, `LazyProperty` (non-data descriptor) |
| `example_1.py` | Type-validated model fields |
| `example_2.py` | Lazy computed property with caching |
| `tests/test_descriptor.py` | pytest suite |

## Run

```bash
python descriptor.py                # demo
python -m pytest tests/ -v          # tests
```

## Key Concepts

- Data descriptor — implements `__get__` + `__set__`; takes precedence over instance `__dict__`
- Non-data descriptor — implements only `__get__`; instance `__dict__` can shadow it
- `__set_name__` — called at class creation to give the descriptor its attribute name
- `Validated` — raises `ValueError` when a predicate fails
