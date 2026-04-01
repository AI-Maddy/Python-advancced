# Chain of Responsibility Pattern

Passes requests along a handler chain. Each handler either processes the request or forwards it to the next handler. The sender is decoupled from the receiver — it does not know which handler will process the request.

## C++ Equivalent
Linked list of handler objects with a virtual `handle(request)` method; each node either processes or calls the next.

## Files

| File | Description |
|---|---|
| `chain_of_responsibility_pattern.py` | Core implementation: `Handler` ABC with `set_next()` fluent chaining |
| `example_1.py` | Log-level filtering chain (DEBUG → INFO → WARNING → ERROR) |
| `example_2.py` | HTTP request middleware chain (auth → rate limit → handler) |
| `example_3.py` | Purchase approval chain (team lead → manager → director) |
| `tests/test_chain_of_responsibility_pattern.py` | pytest suite |

## Run

```bash
python chain_of_responsibility_pattern.py   # demo
python -m pytest tests/ -v                  # tests
```

## Key Classes

- `Handler` — ABC with `set_next(handler)` and abstract `handle(request)`
- `set_next()` returns the next handler, enabling fluent chaining: `low.set_next(medium).set_next(high)`
