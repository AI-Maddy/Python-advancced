# Prototype Pattern

Creates new objects by cloning an existing instance (the prototype) rather than constructing from scratch. A registry maps names to prototype instances so clients can clone named objects without knowing concrete types.

## C++ Equivalent
Virtual `clone()` method using `copy constructor` or `new DerivedClass(*this)`; a prototype registry maps keys to base-class pointers.

## Files

| File | Description |
|---|---|
| `prototype.py` | Core implementation: `Prototype` ABC with `clone()`, `Circle`, `Rectangle`, `ShapeRegistry` |
| `example_1.py` | Shape registry with named prototypes |
| `example_2.py` | Game enemy spawner using prototype cloning |
| `tests/test_prototype.py` | pytest suite |

## Run

```bash
python prototype.py                 # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Prototype` — ABC with abstract `clone() -> Self`
- `Circle`, `Rectangle` — concrete prototypes using `copy.deepcopy`
- `ShapeRegistry` — maps string keys to prototype instances; `clone(name)` returns a deep copy
