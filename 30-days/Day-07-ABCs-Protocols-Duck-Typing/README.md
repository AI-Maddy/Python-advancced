# Day 07 — ABCs, Protocols, and Duck Typing

Define explicit interfaces with `abc.ABC`, use structural subtyping with `typing.Protocol`, and understand when duck typing is the better choice.

## C++ Equivalent
Day 07 of the C++ OOP course (pure virtual interfaces, C++20 Concepts, type erasure).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: `ABC`, `@abstractmethod`, `Protocol`, `@runtime_checkable`, duck typing examples |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day07.py` | pytest suite |

## Key Concepts

- `abc.ABC` + `@abstractmethod` — nominal subtyping; subclasses must inherit and implement
- `typing.Protocol` — structural subtyping; no inheritance needed
- `@runtime_checkable` — allows `isinstance()` checks against a Protocol
- Duck typing — "if it walks like a duck…"; rely on method presence, not type
- `collections.abc` — `Iterable`, `Iterator`, `Sequence`, `Mapping`

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
