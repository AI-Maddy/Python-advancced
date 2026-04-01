# Builder Pattern

Separates the construction of a complex object from its representation, allowing the same construction process to create different representations. A Director orchestrates builder steps; clients may also call steps directly.

## C++ Equivalent
Abstract `Builder` with virtual step methods; a `Director` class calls steps in order; the client calls `getResult()` when done.

## Files

| File | Description |
|---|---|
| `builder.py` | Core implementation: `House` dataclass product, `HouseBuilder` ABC, `Director` |
| `example_1.py` | Luxury and economy house construction via director |
| `example_2.py` | SQL query builder with fluent interface |
| `tests/test_builder.py` | pytest suite |

## Run

```bash
python builder.py                   # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `House` — `@dataclass` product (walls, roof, garden, garage, pool, floors, windows)
- `HouseBuilder` — ABC with step methods returning `self` for fluent chaining
- `Director` — orchestrates builder steps for predefined house types
