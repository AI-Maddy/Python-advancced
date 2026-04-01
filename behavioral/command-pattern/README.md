# Command Pattern

Turns a request into a stand-alone object that contains all information about the request. This lets you parameterise methods with different requests, delay or queue execution, and implement undoable operations.

## C++ Equivalent
Abstract `Command` class with virtual `execute()`/`undo()`, stored in a `std::stack` for undo history.

## Files

| File | Description |
|---|---|
| `command_pattern.py` | Core implementation: `Command` ABC, `TextEditor` receiver, `CommandHistory` invoker |
| `example_1.py` | Text editor with undo/redo |
| `example_2.py` | Smart home device command queue |
| `example_3.py` | Database transaction commands |
| `tests/test_command_pattern.py` | pytest suite |

## Run

```bash
python command_pattern.py           # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Command` — ABC with `execute()` and `undo()` abstract methods
- `TextEditor` — receiver that owns the mutable text buffer
- `CommandHistory` — invoker that maintains an undo stack
- `InsertCommand`, `DeleteCommand`, `ReplaceCommand` — concrete commands
