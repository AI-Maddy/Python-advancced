# Factory Method Pattern

Defines an interface for creating an object but lets subclasses decide which class to instantiate. Decouples the creator from the concrete products.

## C++ Equivalent
Abstract `Creator` with virtual `createProduct()` method; concrete creators override it to produce different product types.

## Files

| File | Description |
|---|---|
| `factory_method.py` | Core implementation: `Vehicle` ABC, `Car`, `Truck`, `Motorcycle`, `VehicleCreator` hierarchy |
| `example_1.py` | Vehicle factory — car, truck, and motorcycle creators |
| `example_2.py` | UI button factory for different platforms |
| `tests/test_factory_method.py` | pytest suite |

## Run

```bash
python factory_method.py            # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Vehicle` — ABC product with `describe()` and `max_speed_kmh()`
- `Car`, `Truck`, `Motorcycle` — concrete products
- `VehicleCreator` — abstract creator with `factory_method()` and shared business logic
