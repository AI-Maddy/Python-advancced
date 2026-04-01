# Visitor Pattern

Represents an operation to be performed on elements of an object structure. Lets you define a new operation without changing the classes of the elements on which it operates (double-dispatch).

## C++ Equivalent
Virtual `accept(Visitor&)` on each element; the visitor has overloaded `visit()` methods — classic double-dispatch in C++.

## Files

| File | Description |
|---|---|
| `visitor_pattern.py` | Core implementation: `Visitor` ABC, `Shape` element ABC, `Circle`, `Rectangle`, `Triangle` |
| `example_1.py` | Area and perimeter calculation visitors on a shape tree |
| `example_2.py` | XML serialisation visitor |
| `example_3.py` | Tax calculation visitor on an order item hierarchy |
| `tests/test_visitor_pattern.py` | pytest suite |

## Run

```bash
python visitor_pattern.py           # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Visitor` — ABC with `visit_circle()`, `visit_rectangle()`, `visit_triangle()` abstract methods
- `Shape` — ABC with abstract `accept(visitor)` method
- `AreaCalculator`, `PerimeterCalculator` — concrete visitors
- `Circle`, `Rectangle`, `Triangle` — concrete elements
