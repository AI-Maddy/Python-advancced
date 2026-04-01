"""
Day 30 — Review, Cert-Prep & Next Steps
=========================================
Complete Python OOP cheat-sheet, interview Q&A,
Python vs C++ comparison, dunder quick-reference,
and recommended next steps.
"""
from __future__ import annotations

# ===========================================================================
# PYTHON OOP CHEAT-SHEET (as runnable code + comments)
# ===========================================================================

# ─── Classes & Instances ───────────────────────────────────────────────────
class MyClass:
    class_var: int = 0           # shared by all instances
    __slots__ = ("x", "y")      # saves memory, no __dict__

    def __init__(self, x: int, y: int) -> None:
        self.x = x              # instance variable
        self.y = y

    def method(self) -> str:    # regular method
        return f"({self.x}, {self.y})"

    @classmethod
    def from_tuple(cls, t: tuple[int, int]) -> "MyClass":
        return cls(*t)          # alternative constructor

    @staticmethod
    def validate(x: int) -> bool:
        return x >= 0

    def __repr__(self) -> str:
        return f"MyClass({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MyClass):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


# ─── Inheritance ──────────────────────────────────────────────────────────
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def speak(self) -> str: ...   # must override in subclass

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.name!r})"

class Dog(Animal):
    def speak(self) -> str:
        return "Woof"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow"


# ─── Protocols (structural subtyping) ─────────────────────────────────────
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return "O"

def render(shape: Drawable) -> str:
    return shape.draw()


# ─── Dataclasses ──────────────────────────────────────────────────────────
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float

@dataclass(frozen=True)       # immutable value object
class ImmutablePoint:
    x: float
    y: float


# ─── Properties & Descriptors ─────────────────────────────────────────────
class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32


# ─── Context Managers ─────────────────────────────────────────────────────
class ManagedResource:
    def __enter__(self) -> "ManagedResource":
        print("Resource opened")
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> bool:
        print("Resource closed")
        return False  # don't suppress exceptions


# ─── Iterators & Generators ───────────────────────────────────────────────
from collections.abc import Iterator

class CountUp:
    def __init__(self, limit: int) -> None:
        self._limit = limit
        self._current = 0

    def __iter__(self) -> "CountUp":
        return self

    def __next__(self) -> int:
        if self._current >= self._limit:
            raise StopIteration
        val = self._current
        self._current += 1
        return val

def countdown(n: int) -> Iterator[int]:
    while n >= 0:
        yield n
        n -= 1


# ─── Decorators ───────────────────────────────────────────────────────────
import functools
from collections.abc import Callable
from typing import TypeVar

F = TypeVar("F", bound=Callable[..., object])

def log_calls(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper  # type: ignore[return-value]


# ===========================================================================
# INTERVIEW Q&A — 20 Common Questions
# ===========================================================================

INTERVIEW_QA = """
PYTHON OOP INTERVIEW Q&A
=========================

Q1: What is the difference between a class and an instance?
A:  A class is a blueprint (type); an instance is a concrete object created
    from that blueprint.  'class Dog' defines the type; Dog() creates an instance.

Q2: What are __new__ and __init__ and how do they differ?
A:  __new__ creates the object (returns it); __init__ initialises it.
    __new__ is called first; you rarely override it except in metaclasses
    or immutable types like str/tuple.

Q3: What is the MRO (Method Resolution Order)?
A:  The order Python searches for methods in the inheritance hierarchy.
    Computed with the C3 linearization algorithm.
    View it with ClassName.__mro__ or help(ClassName).

Q4: What is the difference between @classmethod and @staticmethod?
A:  @classmethod receives the class (cls) as the first argument — useful
    for alternative constructors.  @staticmethod receives no implicit first
    argument — just a namespace function.

Q5: What is the difference between == and is?
A:  == tests value equality (__eq__); is tests object identity (same memory
    address).  Never use 'is' to compare strings, numbers, or None except
    for 'x is None'.

Q6: What is duck typing?
A:  "If it walks like a duck and quacks like a duck, it's a duck."
    Python checks behaviour (method/attribute presence) not explicit type.
    Protocols formalise this at the type-checking level.

Q7: What is a descriptor?
A:  An object that defines __get__, __set__, or __delete__.  Properties
    are descriptors.  Descriptors enable computed attributes and validation.

Q8: What are __slots__?
A:  A class-level attribute that replaces per-instance __dict__ with
    fixed-size slots.  Reduces memory; prevents adding arbitrary attributes.

Q9: What is a metaclass?
A:  The class of a class.  type is the default metaclass.  Custom metaclasses
    intercept class creation to add behaviour (validation, registration).

Q10: What is the difference between a shallow and deep copy?
A:  Shallow copy (copy.copy): new container, shared inner objects.
    Deep copy (copy.deepcopy): fully independent recursive copy.

Q11: What is __all__ and why use it?
A:  A list of public names exported by 'from module import *'.  Documents
    the public API and prevents accidental export of internal names.

Q12: What is the difference between Abstract Base Classes and Protocols?
A:  ABC enforces via inheritance (isinstance checks, __abstractmethods__).
    Protocol uses structural subtyping — no inheritance required; checked
    statically by type checkers.  Protocol is preferred for Python 3.8+.

Q13: What is the GIL and when does it matter?
A:  The Global Interpreter Lock prevents multiple threads from executing
    Python bytecode simultaneously.  Matters for CPU-bound multi-threading
    (use multiprocessing instead).  I/O-bound threads still benefit from
    threading (GIL released during I/O).

Q14: When should you use asyncio vs threading vs multiprocessing?
A:  asyncio: I/O-bound with async libraries (high concurrency, low overhead).
    threading: I/O-bound with blocking libs, moderate concurrency.
    multiprocessing: CPU-bound (bypasses GIL).

Q15: What is a generator and when would you use it?
A:  A function with yield.  Produces values lazily (one at a time), saving
    memory.  Use for large datasets, infinite sequences, or pipelines.

Q16: Explain the difference between __str__ and __repr__.
A:  __repr__ is the 'developer' representation (unambiguous, ideally eval-able).
    __str__ is the 'user' representation (readable).
    print() and str() call __str__; repr() calls __repr__.

Q17: What is multiple inheritance and what problem does super() solve?
A:  A class can inherit from multiple bases.  Without super(), calling
    parent __init__ directly may skip classes in the MRO.  super() follows
    the C3 MRO cooperatively.

Q18: What is the Liskov Substitution Principle?
A:  A subtype must be usable wherever its base type is expected without
    breaking correctness.  Square-extends-Rectangle violates LSP because
    Square overrides width/height setters in a way that breaks Rectangle's
    postconditions.

Q19: What are context managers and the contextlib module?
A:  Objects with __enter__/__exit__ used with 'with' statements.
    contextlib.contextmanager turns a generator into a context manager.

Q20: What is the difference between a property and a slot?
A:  A property is a descriptor that computes a value on access (getter/setter).
    A slot is a fixed memory location for an instance attribute (no computation).
    They can coexist: a class can have both slots (for storage) and properties
    (for computed attributes).
"""


# ===========================================================================
# PYTHON VS C++ OOP COMPARISON TABLE
# ===========================================================================

CPP_VS_PYTHON = """
Python vs C++ OOP — Quick Reference
=====================================

Feature              Python                    C++
─────────────────────────────────────────────────────────────────────
Inheritance          class B(A):               class B : public A {
Multiple inherit.    class C(A, B):            class C : public A, public B {
Abstract class       ABC + @abstractmethod     pure virtual: void f() = 0;
Interface            Protocol (structural)     pure abstract class / concept
Access control       Convention (_private)     private: / protected: / public:
Constructor          __init__(self)            ClassName(args)
Destructor           __del__(self)             ~ClassName()
Operator overload    __add__, __eq__, etc.     operator+, operator==, etc.
Class method         @classmethod              static method (no implicit this)
Static method        @staticmethod             static method
Properties           @property / descriptor    getter/setter methods
Virtual method       All methods virtual       virtual keyword needed
RAII                 with statement            Constructor/Destructor
Memory management    Garbage collected (GC)    Manual (new/delete) or RAII
Type checking        Runtime + mypy            Compile-time
Templates            Generics (TypeVar)        template<typename T>
Metaclass            type / custom Meta        N/A (closest: template metaprog.)
Enum                 enum.Enum                 enum class
Dataclass            @dataclass                struct / aggregate init (C++20)
"""


# ===========================================================================
# DUNDER METHOD QUICK REFERENCE
# ===========================================================================

DUNDER_REFERENCE = """
Dunder (Magic) Method Quick Reference
=======================================

OBJECT LIFECYCLE
  __new__(cls, ...)    → create instance (called before __init__)
  __init__(self, ...)  → initialise instance
  __del__(self)        → called when object is garbage collected

REPRESENTATION
  __repr__(self) → str  developer string (eval-able)
  __str__(self)  → str  user-friendly string
  __format__(self, spec) → str  format() and f-strings
  __bytes__(self) → bytes

COMPARISON  (also use @total_ordering)
  __eq__(self, other)  ==
  __ne__(self, other)  !=
  __lt__(self, other)  <
  __le__(self, other)  <=
  __gt__(self, other)  >
  __ge__(self, other)  >=
  __hash__(self)       hash()  (define with __eq__ or set to None)

ARITHMETIC
  __add__, __radd__, __iadd__   +
  __sub__, __mul__, __truediv__, __floordiv__, __mod__, __pow__
  __neg__, __pos__, __abs__

CONTAINER PROTOCOL
  __len__(self) → int
  __getitem__(self, key)
  __setitem__(self, key, value)
  __delitem__(self, key)
  __contains__(self, item) → bool   (in operator)
  __iter__(self) → iterator
  __next__(self)
  __reversed__(self)
  __missing__(self, key)            (dict subclass only)

CALLABLE
  __call__(self, *args, **kwargs)

CONTEXT MANAGER
  __enter__(self) → self_or_resource
  __exit__(self, exc_type, exc_val, exc_tb) → bool

ASYNC CONTEXT MANAGER
  __aenter__(self)
  __aexit__(self, ...)

ASYNC ITERATOR
  __aiter__(self)
  __anext__(self)   (raise StopAsyncIteration when done)

ATTRIBUTE ACCESS
  __getattr__(self, name)           called only when normal lookup fails
  __getattribute__(self, name)      called for EVERY attribute access
  __setattr__(self, name, value)
  __delattr__(self, name)
  __dir__(self) → list[str]

DESCRIPTOR PROTOCOL
  __get__(self, obj, objtype=None)
  __set__(self, obj, value)
  __delete__(self, obj)
  __set_name__(self, owner, name)   called at class creation time

CLASS CREATION
  __init_subclass__(cls, **kwargs)  hook for subclass registration
  __class_getitem__(cls, item)      supports Generic[T] syntax

PICKLE / COPY
  __getstate__(self) → dict
  __setstate__(self, state)
  __copy__(self)
  __deepcopy__(self, memo)
  __reduce__(self) / __reduce_ex__(self, protocol)
"""


# ===========================================================================
# WHAT'S NEXT — Ecosystem & Advanced Topics
# ===========================================================================

NEXT_STEPS = """
What to Learn Next
===================

1. PYDANTIC (v2) — data validation with Python type hints
   - BaseModel, Field, validators
   - JSON schema generation
   - FastAPI integration
   - pip install pydantic

2. ATTRS — more flexible alternative to dataclasses
   - @attrs.define, converters, validators
   - Smaller footprint than dataclasses for some patterns
   - pip install attrs

3. SQLALCHEMY ORM — industry-standard Python ORM
   - DeclarativeBase, Mapped, relationship
   - Session, async sessions
   - Alembic for migrations
   - pip install sqlalchemy

4. FASTAPI — modern async web framework
   - Path operations, dependency injection
   - Automatic OpenAPI docs
   - Integrates with pydantic for validation
   - pip install fastapi uvicorn

5. HYPOTHESIS — property-based testing
   - @given, strategies
   - Finds edge cases automatically
   - pip install hypothesis

6. MYPY / PYRIGHT — static type checking
   - Run: mypy src/ --strict
   - CI integration

7. ASYNCIO ADVANCED
   - asyncio.TaskGroup (Python 3.11+)
   - anyio for cross-backend async
   - aiohttp, httpx for async HTTP

RECOMMENDED READING
====================

* "Fluent Python" — Luciano Ramalho (2nd edition, 2022)
  Best deep-dive into Python's data model and internals.

* "Python Cookbook" — David Beazley & Brian Jones (3rd edition)
  Practical recipes for advanced Python.

* "Architecture Patterns with Python" — Harry Percival & Bob Gregory
  DDD, ports/adapters, event-driven architecture in Python.

* "Clean Code" — Robert C. Martin
  Language-agnostic; principles apply perfectly to Python.

* Python docs:
  https://docs.python.org/3/reference/datamodel.html
  https://docs.python.org/3/library/typing.html
"""


# ===========================================================================
# Main — Print everything
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 30 — Review, Cert-Prep & Next Steps")
    print("=" * 60)

    # Run quick cheat-sheet demos
    print("\n--- Cheat-sheet demos ---")
    mc = MyClass(3, 4)
    print(f"MyClass: {mc}")
    print(f"from_tuple: {MyClass.from_tuple((5, 6))}")
    print(f"validate(10): {MyClass.validate(10)}")

    dog = Dog("Buddy")
    print(f"Dog speaks: {dog.speak()}")

    print(f"render(Circle): {render(Circle())}")

    p = Point(1.0, 2.0)
    print(f"Point: {p}")

    t = Temperature(100.0)
    print(f"100°C = {t.fahrenheit}°F")

    for n in countdown(5):
        print(n, end=" ")
    print()

    @log_calls
    def add(a: int, b: int) -> int:
        return a + b

    add(2, 3)

    # Print reference texts
    print(INTERVIEW_QA)
    print(CPP_VS_PYTHON)
    print(DUNDER_REFERENCE)
    print(NEXT_STEPS)
