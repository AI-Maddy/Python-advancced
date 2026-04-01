# Day 10 — Type Hints, Annotated, and TypeGuard

Advanced type system features: `Annotated` for metadata-bearing types, `TypeGuard` for narrowing, `Literal` for exact values, and `Final` for constants.

## C++ Equivalent
Day 10 of the C++ OOP course (`const`, `constexpr`, type traits, `std::is_same`).

## Files

| File | Description |
|---|---|
| `lesson.py` | Full lesson: `Annotated`, `TypeGuard`, `Literal`, `Final`, `TypeAlias`, `Never` |
| `exercises.py` | Exercises with TODO markers |
| `solutions.py` | Complete solutions |
| `theory.rst` | Concise theory notes |
| `tests/test_day10.py` | pytest suite |

## Key Concepts

- `Annotated[T, metadata]` — attach validators or documentation to a type
- `TypeGuard[T]` — narrow the type of a variable inside an `if` block
- `Literal["a", "b"]` — restrict to exact values
- `Final` — prevent reassignment; equivalent to `const`
- `TypeAlias` — explicit type alias declaration
- `overload` — declare multiple signatures for one function

## Run

```bash
python lesson.py                    # run the lesson
python -m pytest tests/ -v          # run tests
```
