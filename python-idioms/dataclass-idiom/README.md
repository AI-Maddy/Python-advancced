# Dataclass Idiom

Python's "Rule of Zero" — `@dataclass` auto-generates `__init__`, `__repr__`, and `__eq__` from annotated fields, eliminating boilerplate. Frozen dataclasses provide immutable value objects.

## C++ Equivalent
Rule of Zero (letting the compiler generate copy/move constructor and destructor); aggregate initialisation; `const` structs for value types.

## Files

| File | Description |
|---|---|
| `dataclass_idiom.py` | Core implementation: `Point`, `RGB` (frozen), `__post_init__`, `field()`, `InitVar`, `dataclasses.asdict`/`replace` |
| `example_1.py` | Domain model with mutable and frozen dataclasses |
| `example_2.py` | Configuration objects and DTO patterns |
| `tests/test_dataclass_idiom.py` | pytest suite |

## Run

```bash
python dataclass_idiom.py           # demo
python -m pytest tests/ -v          # tests
```

## Key Concepts

- `@dataclass` — generates `__init__`, `__repr__`, `__eq__`
- `@dataclass(frozen=True)` — immutable; generates `__hash__`
- `@dataclass(slots=True)` — memory-efficient (Python 3.10+)
- `field(default_factory=...)` — mutable default values
- `__post_init__` — validation after `__init__`
- `dataclasses.asdict`, `dataclasses.replace` — utility functions
