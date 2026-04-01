# Flyweight Pattern

Minimises memory usage by sharing as much data as possible between similar objects. Separates intrinsic (shared, immutable) state from extrinsic (per-use, caller-supplied) state.

## C++ Equivalent
A factory that returns shared `const` objects; clients pass extrinsic state at call time rather than storing it in each object.

## Files

| File | Description |
|---|---|
| `flyweight.py` | Core implementation: `CharacterStyle` frozen dataclass (intrinsic), `FlyweightFactory` cache |
| `example_1.py` | Character rendering — font/color/size shared, position supplied per render call |
| `example_2.py` | Game particle system — particle type shared, position/velocity per particle |
| `tests/test_flyweight.py` | pytest suite |

## Run

```bash
python flyweight.py                 # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `CharacterStyle` — `@dataclass(frozen=True)` holding `font`, `color`, `size` (intrinsic state)
- `CharacterStyle.render(char, x, y)` — combines intrinsic style with extrinsic position
- `FlyweightFactory` — creates and caches `CharacterStyle` instances; reports cache size
