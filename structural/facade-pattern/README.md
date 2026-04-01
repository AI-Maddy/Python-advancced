# Facade Pattern

Provides a simplified interface to a complex subsystem, hiding its internals from clients. The facade delegates client calls to the appropriate subsystem objects.

## C++ Equivalent
A class that wraps multiple subsystem objects and exposes a small, cohesive public API, hiding the orchestration complexity.

## Files

| File | Description |
|---|---|
| `facade.py` | Core implementation: `Amplifier`, `DVDPlayer`, `Projector`, `Lights` subsystems; `HomeTheaterFacade` |
| `example_1.py` | Home theater — `watch_movie()` / `end_movie()` hides 8+ subsystem calls |
| `example_2.py` | E-commerce order facade (inventory, payment, shipping, notification) |
| `tests/test_facade.py` | pytest suite |

## Run

```bash
python facade.py                    # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Amplifier`, `DVDPlayer`, `Projector`, `Lights` — complex subsystem classes
- `HomeTheaterFacade` — exposes `watch_movie(title)` and `end_movie()` as the simplified interface
