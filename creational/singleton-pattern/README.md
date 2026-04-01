# Singleton Pattern

Ensures a class has only one instance and provides a global access point to it. Three idiomatic Python implementations are shown: metaclass, module-level singleton, and decorator.

## C++ Equivalent
Static private instance with `getInstance()` static method; constructor is private.

## Files

| File | Description |
|---|---|
| `singleton.py` | Core implementation: `SingletonMeta` metaclass, `DatabasePool`, `@singleton` decorator |
| `example_1.py` | Application configuration singleton |
| `example_2.py` | Logger singleton with thread safety |
| `tests/test_singleton.py` | pytest suite |

## Run

```bash
python singleton.py                 # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `SingletonMeta` — thread-safe metaclass using `threading.Lock`
- `DatabasePool` — example singleton using `SingletonMeta`
- `@singleton` — decorator-based approach for lightweight use cases
