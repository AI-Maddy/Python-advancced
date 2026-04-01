# Bridge Pattern

Decouples an abstraction from its implementation so that the two can vary independently. The abstraction delegates implementation work to a contained implementation object.

## C++ Equivalent
Abstract `Abstraction` holds a pointer to an abstract `Implementor`; both hierarchies evolve independently without a combinatorial explosion of subclasses.

## Files

| File | Description |
|---|---|
| `bridge.py` | Core implementation: `Renderer` implementation ABC, `Shape` abstraction ABC, concrete renderers and shapes |
| `example_1.py` | Shapes rendered via vector, raster, and ASCII renderers |
| `example_2.py` | Messaging abstraction bridged to email, SMS, and push notification implementations |
| `tests/test_bridge.py` | pytest suite |

## Run

```bash
python bridge.py                    # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Renderer` — implementation ABC with `render_circle()` and `render_rectangle()`
- `VectorRenderer`, `RasterRenderer`, `AsciiRenderer` — concrete implementations
- `Shape` — abstraction ABC that holds a `Renderer` reference
- `Circle`, `Rectangle` — refined abstractions
