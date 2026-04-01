Day 04 — Dataclasses, Slots, and Constructors
===============================================

Why This Day Matters
--------------------

Manually writing ``__init__``, ``__repr__``, and ``__eq__`` for every data
class is tedious and error-prone.  ``@dataclass`` eliminates that boilerplate
while making the intent explicit.  Knowing when to use ``frozen=True``,
``slots=True``, or ``NamedTuple`` determines both correctness and performance.


@dataclass — What Gets Generated
----------------------------------

.. code-block:: python

    @dataclass
    class Point:
        x: float
        y: float

    # Equivalent to writing manually:
    class Point:
        def __init__(self, x: float, y: float) -> None:
            self.x = x
            self.y = y
        def __repr__(self) -> str:
            return f"Point(x={self.x!r}, y={self.y!r})"
        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Point): return NotImplemented
            return (self.x, self.y) == (other.x, other.y)

Generated methods respect ``field(repr=False)``, ``field(compare=False)``, etc.


The Mutable Default Trap — Why field() Exists
----------------------------------------------

.. code-block:: python

    # WRONG: list shared across all instances
    @dataclass
    class Bad:
        items: list[str] = []   # SyntaxError / ValueError at class time

    # CORRECT: new list per instance
    @dataclass
    class Good:
        items: list[str] = field(default_factory=list)

``default_factory`` is called with no arguments for each new instance.
Use it for any mutable default (``list``, ``dict``, ``set``).


__post_init__ — Validation Hook
---------------------------------

.. code-block:: python

    @dataclass
    class Student:
        name: str
        grade: float

        def __post_init__(self) -> None:
            if not self.name:
                raise ValueError("name cannot be empty")
            if not (0 <= self.grade <= 100):
                raise ValueError(f"grade must be 0-100, got {self.grade}")

``__post_init__`` runs after the generated ``__init__`` assigns all fields.
Use it for cross-field validation and derived field initialisation.


frozen=True — Immutable Dataclasses
--------------------------------------

.. code-block:: python

    @dataclass(frozen=True)
    class Config:
        host: str
        port: int

    c = Config("localhost", 8080)
    c.host = "other"   # raises FrozenInstanceError

- Generates ``__hash__`` (required for dict keys / set elements)
- Prevents attribute assignment after construction
- C++ equivalent: class with all ``const`` members

**Trade-off:** frozen instances cannot be modified in-place; use ``dataclasses.replace()``
to create modified copies.


slots=True — Memory Optimisation (Python 3.10+)
-------------------------------------------------

.. code-block:: python

    @dataclass(slots=True)
    class Particle:
        x: float
        y: float
        z: float

- Uses ``__slots__`` instead of per-instance ``__dict__``
- ~30% less memory per instance
- Faster attribute access
- Prevents adding new attributes dynamically
- Cannot be used with some metaclasses or multiple inheritance


NamedTuple vs dataclass
------------------------

+--------------------+---------------------+-------------------------------+
| Feature            | NamedTuple          | @dataclass                    |
+====================+=====================+===============================+
| Mutability         | Immutable           | Mutable by default            |
+--------------------+---------------------+-------------------------------+
| Memory             | Tuple (low)         | Object (higher)               |
+--------------------+---------------------+-------------------------------+
| Indexable          | Yes (``t[0]``)      | No                            |
+--------------------+---------------------+-------------------------------+
| Inheritance        | Limited             | Full                          |
+--------------------+---------------------+-------------------------------+
| Introspection      | ``_fields``         | ``dataclasses.fields()``      |
+--------------------+---------------------+-------------------------------+

Use ``NamedTuple`` for simple, immutable value objects where tuple semantics
are useful (unpacking, CSV rows).  Use ``@dataclass`` for richer objects.


Self-Check Questions
--------------------

**Q1: Why can't you use** ``items: list = []`` **as a default in a dataclass?**

Python evaluates default values once at class definition time.  A mutable
default would be shared across all instances — modifying one instance's list
would affect all others.  ``field(default_factory=list)`` creates a fresh
list for each instance.

**Q2: What does** ``frozen=True`` **add to a dataclass?**

It generates ``__hash__`` (so the instance can be used in sets and as dict
keys) and raises ``FrozenInstanceError`` on any attempt to assign to a field
after construction.  It is the dataclass equivalent of a ``const`` object.

**Q3: When should you use** ``@classmethod`` **factory methods?**

When you have multiple ways to construct an object from different input
formats (e.g., from degrees vs radians, from ISO string vs date parts).
Named constructors make the intent explicit without overloading ``__init__``
(Python does not support constructor overloading).

**Q4: What is the difference between a** ``ClassVar`` **and a regular field?**

A ``ClassVar[T]`` annotation tells the dataclass machinery to skip that
attribute — it is a class variable, not an instance field.  It will not
appear in ``__init__``, ``__repr__``, or ``fields()``.
