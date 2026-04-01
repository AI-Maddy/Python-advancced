# Mixin Idiom

Mixins are classes that provide reusable behaviour through multiple inheritance without being intended as standalone base classes. Python's MRO (Method Resolution Order) and `super()` make cooperative multiple inheritance predictable.

## C++ Equivalent
CRTP (Curiously Recurring Template Pattern) for static mixins; multiple inheritance with virtual bases for dynamic mixins.

## Files

| File | Description |
|---|---|
| `mixin_idiom.py` | Core implementation: `LoggingMixin`, `ValidationMixin`, `SerializationMixin` with MRO-safe `super()` |
| `example_1.py` | Domain model classes composed from multiple mixins |
| `example_2.py` | Repository class with caching and logging mixins |
| `tests/test_mixin_idiom.py` | pytest suite |

## Run

```bash
python mixin_idiom.py               # demo
python -m pytest tests/ -v          # tests
```

## Key Concepts

- MRO — `ClassName.__mro__` shows the resolution order; Python uses C3 linearisation
- `super()` — cooperative; calls the next class in the MRO, not necessarily the direct parent
- `LoggingMixin` — adds `logger` property and `log(level, message)` helper
- `ValidationMixin` — adds `validate()` hook driven by a `_rules()` method
- `SerializationMixin` — adds `to_json()` / `from_json()` via `__dict__`
