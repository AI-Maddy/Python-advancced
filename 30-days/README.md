# 30-Day Python OOP Course

A structured 31-day programme (Day 00 through Day 30) that builds Python OOP skills from the ground up, ported from the equivalent C++ OOP curriculum. Days 00–15 cover core language features; days 16–23 cover advanced OOP and tooling; days 24–26 are mini-projects; days 27–30 cover refactoring, review, and next steps.

## Day Index

| Day | Directory | Topic |
|---|---|---|
| 00 | `Day-00-Setup-And-Basics` | Python installation, venv, pip, REPL, `__name__` |
| 01 | `Day-01-Variables-Types-Literals` | Built-in types, dynamic typing, f-strings |
| 02 | `Day-02-Functions-Lambdas-Closures` | Functions, lambdas, closures, `*args`/`**kwargs` |
| 03 | `Day-03-Classes-Encapsulation` | `__init__`, properties, name mangling, dunder methods |
| 04 | `Day-04-Dataclasses-Slots-Constructors` | `@dataclass`, `__slots__`, named constructors |
| 05 | `Day-05-Context-Managers-RAII` | `__enter__`/`__exit__`, `@contextmanager`, RAII |
| 06 | `Day-06-Inheritance-Polymorphism` | Single/multiple inheritance, MRO, `super()` |
| 07 | `Day-07-ABCs-Protocols-Duck-Typing` | `ABC`, `@abstractmethod`, `Protocol`, duck typing |
| 08 | `Day-08-Advanced-OOP-Patterns` | Mixins, class decorators, `__init_subclass__` |
| 09 | `Day-09-Generics-TypeVar-Generic` | `TypeVar`, `Generic[T]`, generic classes |
| 10 | `Day-10-Type-Hints-Annotated-TypeGuard` | `Annotated`, `TypeGuard`, `Literal`, `Final` |
| 11 | `Day-11-Generic-OOP-Design` | Generic containers, variance, covariance |
| 12 | `Day-12-Iterators-Generators` | `__iter__`/`__next__`, `yield`, generator pipelines |
| 13 | `Day-13-Decorators-In-Depth` | Decorator factories, class-based decorators, stacking |
| 14 | `Day-14-Descriptors-Properties` | `__get__`/`__set__`/`__set_name__`, `@property` |
| 15 | `Day-15-Error-Handling-Custom-Exceptions` | Exception hierarchy, custom exceptions, `__cause__` |
| 16 | `Day-16-Modules-Packages-Imports` | `__init__.py`, relative imports, namespace packages |
| 17 | `Day-17-Design-Patterns-OOP` | Survey of GoF patterns in Python |
| 18 | `Day-18-SOLID-Principles` | SRP, OCP, LSP, ISP, DIP with Python examples |
| 19 | `Day-19-Testing-Pytest-TDD` | `pytest`, fixtures, parametrize, TDD workflow |
| 20 | `Day-20-Metaclasses-Class-Internals` | `type`, `__new__`, `__init_subclass__`, metaclasses |
| 21 | `Day-21-Functools-Operator-Itertools` | `lru_cache`, `partial`, `reduce`, `chain`, `groupby` |
| 22 | `Day-22-Performance-Profiling-OOP` | `timeit`, `cProfile`, `__slots__`, memory profiling |
| 23 | `Day-23-Async-Coroutines-Intro` | `async def`, `await`, `asyncio.gather`, coroutines |
| 24 | `Day-24-Mini-Project-1-Bank-System` | OOP mini-project: bank account system |
| 25 | `Day-25-Mini-Project-2-Shape-Editor` | OOP mini-project: shape editor with visitor |
| 26 | `Day-26-Mini-Project-3-Game-Entities` | OOP mini-project: game entity/component system |
| 27 | `Day-27-Refactoring-Legacy-Code` | Extract class, replace conditional with polymorphism |
| 28 | `Day-28-Code-Review-Common-Pitfalls` | Anti-patterns, mutable defaults, late binding closures |
| 29 | `Day-29-Advanced-Topics-Deep-Dive` | `__slots__` edge cases, `weakref`, `pickle`, `enum` |
| 30 | `Day-30-Review-Cert-Prep-Next-Steps` | Cheat sheet, interview Q&A, next steps |

## Directory Layout

Each day directory contains:

```
Day-NN-Topic/
    lesson.py       # Full lesson with all concepts demonstrated
    exercises.py    # Exercises with TODO markers
    solutions.py    # Complete solutions
    theory.rst      # Concise theory notes
    tests/
        test_dayNN.py
```

Note: not all days have a `tests/` directory (early days and mini-projects may use different test file names).

## Run

```bash
# Run a specific day
python -m pytest 30-days/Day-03-Classes-Encapsulation/ -v

# Run all 30-day tests
python -m pytest 30-days/ -q

# Run the lesson interactively
python 30-days/Day-03-Classes-Encapsulation/lesson.py
```
