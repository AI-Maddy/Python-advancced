# Composite Pattern

Composes objects into tree structures to represent part-whole hierarchies. Clients treat individual objects (leaves) and compositions (composites) uniformly through a common component interface.

## C++ Equivalent
Abstract `Component` with virtual `operation()`; `Leaf` and `Composite` subclasses; `Composite` holds a `vector<Component*>`.

## Files

| File | Description |
|---|---|
| `composite.py` | Core implementation: `Component` ABC, `File` (leaf), `Directory` (composite) |
| `example_1.py` | File system tree with size calculation |
| `example_2.py` | UI widget hierarchy (panels containing buttons and labels) |
| `tests/test_composite.py` | pytest suite |

## Run

```bash
python composite.py                 # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Component` — ABC with `operation()`, `size()`, `add()`, `remove()`, `children`
- `File` — leaf: implements `operation()` and `size()`; raises on `add()`/`remove()`
- `Directory` — composite: delegates `operation()` and `size()` to children recursively
