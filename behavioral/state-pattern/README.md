# State Pattern

Lets an object alter its behaviour when its internal state changes. The object will appear to change its class. Instead of large `if`/`elif` chains, each state is a separate class that handles the context's behaviour.

## C++ Equivalent
Virtual `State` base class; the context holds a `unique_ptr<State>` and swaps it on transitions.

## Files

| File | Description |
|---|---|
| `state_pattern.py` | Core implementation: `State` ABC, `TrafficLight` context, `RedState`, `GreenState`, `YellowState` |
| `example_1.py` | Traffic light state machine |
| `example_2.py` | Vending machine states (idle, has money, dispensing) |
| `example_3.py` | Document workflow states (draft, review, published) |
| `tests/test_state_pattern.py` | pytest suite |

## Run

```bash
python state_pattern.py             # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `State` — ABC with `handle(context)` and `__repr__`
- `TrafficLight` — context that delegates to the current state
- `RedState`, `GreenState`, `YellowState` — concrete states
