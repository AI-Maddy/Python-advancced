# Classmethod Factory Idiom

`@classmethod` provides named alternative constructors that make object creation intent clear. This is Python's idiomatic equivalent of the C++ named constructor idiom.

## C++ Equivalent
Named constructor idiom — static factory methods (`Date::fromString()`, `Date::today()`); private constructors with public static creators.

## Files

| File | Description |
|---|---|
| `classmethod_factory.py` | Core implementation: `Date` with `from_string()`, `from_timestamp()`, `today()` class methods; `__init_subclass__`, `__class_getitem__` |
| `example_1.py` | Domain objects (User, Product) with multiple named constructors |
| `example_2.py` | Registry pattern using `@classmethod` and `__init_subclass__` |
| `tests/test_classmethod_factory.py` | pytest suite |

## Run

```bash
python classmethod_factory.py       # demo
python -m pytest tests/ -v          # tests
```

## Key Concepts

- `@classmethod` — receives the class (`cls`) as first argument; can construct any subclass
- Named constructor — makes construction intent clear: `Date.from_string("2024-01-15")`
- `__init_subclass__` — hook for subclass configuration without a full metaclass
- `__class_getitem__` — enables generic syntax `MyClass[int]` without full `Generic[T]`
