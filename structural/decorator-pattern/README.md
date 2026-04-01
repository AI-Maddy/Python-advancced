# Decorator Pattern (GoF Structural)

Attaches additional responsibilities to an object dynamically via composition, without modifying its class. Decorators wrap a component and add to its behaviour, stacking arbitrarily.

Note: this is the GoF structural Decorator, which is distinct from Python's `@decorator` syntax (covered in `python-idioms/decorator-function-idiom`).

## C++ Equivalent
Abstract `Component` base; `Decorator` holds a `Component*` and forwards calls, adding behaviour before/after.

## Files

| File | Description |
|---|---|
| `decorator.py` | Core implementation: `Beverage` component ABC, `Espresso`/`HouseBlend` concretions, `MilkDecorator`, `SugarDecorator`, `VanillaDecorator` |
| `example_1.py` | Coffee shop beverage customisation |
| `example_2.py` | Text formatting decorators (bold, italic, underline) |
| `tests/test_decorator.py` | pytest suite |

## Run

```bash
python decorator.py                 # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Beverage` — component ABC with `description()` and `cost()`
- `Espresso`, `HouseBlend` — concrete base beverages
- `BeverageDecorator` — abstract decorator that wraps a `Beverage`
- `MilkDecorator`, `SugarDecorator`, `VanillaDecorator` — concrete decorators
