# __slots__ Idiom

`__slots__` replaces the instance `__dict__` with a fixed set of slot descriptors, reducing per-instance memory usage significantly for classes with many instances.

## C++ Equivalent
Struct or class with a fixed set of data members — no dynamic attribute addition; predictable memory layout.

## Files

| File | Description |
|---|---|
| `slots_idiom.py` | Core implementation: `PointWithDict` vs `PointWithSlots`, memory comparison, slots with inheritance, `__weakref__` |
| `example_1.py` | High-volume particle simulation comparing dict vs slots memory |
| `example_2.py` | Slots in an inheritance chain with `__dict__` re-enabled at one level |
| `tests/test_slots_idiom.py` | pytest suite |

## Run

```bash
python slots_idiom.py               # demo
python -m pytest tests/ -v          # tests
```

## Key Concepts

- `__slots__ = ("x", "y")` — declares the only allowed attributes; eliminates `__dict__`
- Memory saving — each slot is a fixed-size descriptor vs a hash-table entry
- Inheritance — subclasses must also declare `__slots__` to avoid reintroducing `__dict__`
- `__weakref__` — add to `__slots__` explicitly if weak references are needed
