# Day 08 — Advanced OOP Patterns

Mixins, class decorators, `__init_subclass__`, and other advanced techniques for composing class behaviour without deep inheritance hierarchies.

## C++ Equivalent
Day 08 of the C++ OOP course (CRTP, policy-based design, mixin templates).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: mixins, class decorators, `__init_subclass__`, `__set_name__` |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day08.py` | pytest suite |

## Key Concepts

- Mixins — reusable behaviour classes not meant to stand alone
- Class decorators — transform a class at definition time
- `__init_subclass__` — hook called on the parent when a new subclass is defined
- `__set_name__` — descriptor hook called when the descriptor is assigned to a class attribute
- Composition vs inheritance trade-offs

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
