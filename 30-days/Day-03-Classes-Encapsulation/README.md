# Day 03 — Classes and Encapsulation

Learn Python's class system: constructors, instance vs class attributes, properties for encapsulation, name mangling, and the essential dunder methods.

## C++ Equivalent
Day 03 of the C++ OOP course (classes, access specifiers, constructors, `this` pointer).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: `__init__`, `self`, properties, name mangling, dunder methods |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day03.py` | pytest suite |

## Key Concepts

- `__init__`, `self`, instance vs class attributes
- `@property`, `@<prop>.setter`, `@<prop>.deleter`
- Name mangling: `__private` vs `_protected` convention
- `__repr__`, `__str__`, `__eq__`, `__hash__`
- `@staticmethod` vs `@classmethod`

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
