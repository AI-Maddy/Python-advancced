# Protocol Idiom

`typing.Protocol` enables structural subtyping (duck typing with static checks). Classes satisfy a Protocol implicitly — no inheritance required. Equivalent to C++ Concepts or type erasure.

## C++ Equivalent
C++20 Concepts (`requires` clauses); type erasure with `std::any` or technique of wrapping in an ABC.

## Files

| File | Description |
|---|---|
| `protocol_idiom.py` | Core implementation: `Drawable`, `Serializable` protocols with `@runtime_checkable` |
| `example_1.py` | Duck-typed renderer accepting any `Drawable` without inheritance |
| `example_2.py` | Generic serialisation pipeline using `Serializable` protocol |
| `tests/test_protocol_idiom.py` | pytest suite |

## Run

```bash
python protocol_idiom.py            # demo
python -m pytest tests/ -v          # tests
```

## Key Concepts

- `Protocol` — defines an interface by method signatures; no inheritance from the protocol needed
- `@runtime_checkable` — enables `isinstance(obj, MyProtocol)` checks at runtime
- Structural subtyping — a class matches a Protocol if it has the required methods, regardless of its base classes
- Contrast with `ABC` — ABCs use nominal subtyping (must explicitly inherit or register)
