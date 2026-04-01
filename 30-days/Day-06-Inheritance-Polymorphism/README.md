# Day 06 — Inheritance and Polymorphism

Python's inheritance model: single and multiple inheritance, the MRO, `super()`, method overriding, and polymorphism through duck typing.

## C++ Equivalent
Day 06 of the C++ OOP course (`virtual`, inheritance hierarchies, `override`, `final`, vtable).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: single inheritance, multiple inheritance, MRO, `super()`, polymorphism |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day06.py` | pytest suite |

## Key Concepts

- Single and multiple inheritance
- MRO — `ClassName.__mro__`, C3 linearisation
- `super()` — cooperative multiple inheritance
- Method overriding — all methods are effectively `virtual`
- Polymorphism via duck typing and ABCs
- `isinstance()`, `issubclass()`

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
