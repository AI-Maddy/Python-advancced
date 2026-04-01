# Observer Pattern

Defines a one-to-many dependency so that when one object changes state, all its dependents are notified and updated automatically.

## C++ Equivalent
`std::function` callbacks, virtual `Observer` interface, or signal/slot libraries (Qt, Boost.Signals2).

## Files

| File | Description |
|---|---|
| `observer_pattern.py` | Core implementation: `Observer` ABC, `Subject` with event-keyed subscriber list |
| `example_1.py` | Stock price alert system |
| `example_2.py` | UI event system (click, hover, keypress) |
| `example_3.py` | Sensor data pipeline with recorder, anomaly detector, and display |
| `tests/test_observer_pattern.py` | pytest suite |

## Run

```bash
python observer_pattern.py          # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Observer` — ABC with `update(event, data)` method
- `Subject` — maintains an event-keyed subscriber dict; `attach()`, `detach()`, `notify()`
