# Mediator Pattern

Defines an object that encapsulates how a set of objects interact. Promotes loose coupling by keeping objects from referring to each other explicitly, avoiding the "star topology" of direct object-to-object references.

## C++ Equivalent
Central coordinator object that all participants hold a pointer to; participants call `mediator->notify()` instead of calling peers directly.

## Files

| File | Description |
|---|---|
| `mediator_pattern.py` | Core implementation: `Mediator` ABC, `User` colleague, `ChatRoom` concrete mediator |
| `example_1.py` | Chat room with multiple users |
| `example_2.py` | Air traffic control tower coordinating aircraft |
| `example_3.py` | GUI component mediator (form fields that enable/disable each other) |
| `tests/test_mediator_pattern.py` | pytest suite |

## Run

```bash
python mediator_pattern.py          # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Mediator` — ABC with `notify(sender, event, data)`
- `User` — colleague that holds a reference to the mediator, not to other users
- `ChatRoom` — concrete mediator that routes messages between users
