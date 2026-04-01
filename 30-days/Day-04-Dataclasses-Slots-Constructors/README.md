# Day 04 — Dataclasses, Slots, and Constructors

Use `@dataclass` to eliminate boilerplate, `__slots__` for memory efficiency, and `@classmethod` for named alternative constructors.

## C++ Equivalent
Day 04 of the C++ OOP course (Rule of Zero, aggregate initialisation, named constructors, struct layout).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: `@dataclass`, `frozen=True`, `slots=True`, `field()`, `__post_init__`, `@classmethod` factories |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day04.py` | pytest suite |

## Key Concepts

- `@dataclass` — auto `__init__`, `__repr__`, `__eq__`
- `@dataclass(frozen=True)` — immutable value objects with `__hash__`
- `@dataclass(slots=True)` — memory-efficient layout (Python 3.10+)
- `field(default_factory=...)`, `__post_init__`, `InitVar`
- `@classmethod` as named constructor (`from_string`, `from_dict`)
- `dataclasses.asdict`, `dataclasses.replace`

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
