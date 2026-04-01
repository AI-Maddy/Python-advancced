# Memento Pattern

Lets you save and restore the previous state of an object without revealing the details of its implementation. The caretaker stores snapshots; the originator creates and restores them.

## C++ Equivalent
Inner class or `friend` class holding a private copy of the originator's state; stored in a `std::stack` by the caretaker.

## Files

| File | Description |
|---|---|
| `memento_pattern.py` | Core implementation: `Memento` frozen dataclass, `Originator`, `Caretaker` |
| `example_1.py` | Text editor with undo history |
| `example_2.py` | Game save/load state |
| `example_3.py` | Configuration manager with rollback |
| `tests/test_memento_pattern.py` | pytest suite |

## Run

```bash
python memento_pattern.py           # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Memento` — `@dataclass(frozen=True)` snapshot holding `state` and `timestamp`
- `Originator` — creates mementos via `save()` and restores them via `restore(memento)`
- `Caretaker` — maintains a stack of mementos; calls `save()`/`undo()`
