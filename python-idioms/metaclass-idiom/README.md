# Metaclass Idiom

Metaclasses are the "classes of classes" — they control class creation. Use them for singleton enforcement, automatic subclass registration, and interface validation. `__init_subclass__` is a lighter alternative for most use cases.

## C++ Equivalent
Template metaprogramming, CRTP (Curiously Recurring Template Pattern), and type traits.

## Files

| File | Description |
|---|---|
| `metaclass.py` | Core implementation: `SingletonMeta`, `RegistryMeta`, `AbstractMeta`, `__init_subclass__` example |
| `example_1.py` | Plugin registry using `RegistryMeta` |
| `example_2.py` | ORM-style model field registry |
| `tests/test_metaclass.py` | pytest suite |

## Run

```bash
python metaclass.py                 # demo
python -m pytest tests/ -v          # tests
```

## Key Concepts

- `type` — the default metaclass; every class is an instance of `type`
- `SingletonMeta` — thread-safe singleton via metaclass `__call__`
- `RegistryMeta` — auto-registers every concrete subclass by name
- `__init_subclass__` — hook called on the parent class when a subclass is defined; avoids a full metaclass
