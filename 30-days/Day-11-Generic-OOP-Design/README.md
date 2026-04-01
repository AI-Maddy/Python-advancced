# Day 11 — Generic OOP Design

Design reusable generic data structures and class hierarchies. Covers variance (covariant, contravariant), generic containers, and combining `Generic[T]` with ABCs.

## C++ Equivalent
Day 11 of the C++ OOP course (generic containers, template specialisation, `enable_if`, variance concepts).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: generic stack, queue, result type, covariance vs contravariance |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day11.py` | pytest suite |

## Key Concepts

- Generic containers: `Stack[T]`, `Queue[T]`, `Result[T, E]`
- `Generic[T]` combined with `ABC`
- Variance: `Covariant[T_co]` vs `Contravariant[T_contra]`
- `TypeVar` with `covariant=True` or `contravariant=True`
- Practical patterns: repository, event bus, typed builder

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
