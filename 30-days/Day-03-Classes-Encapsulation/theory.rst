Day 03 — Classes and Encapsulation
====================================

Why This Day Matters
--------------------

A class establishes an **invariant** — a guarantee about its internal state
that holds at all observable points.  Encapsulation is the mechanism that
prevents external code from violating that invariant.  Python's encapsulation
model is built on convention, not enforcement — understanding why matters.


Python vs C++ Encapsulation
-----------------------------

+---------------------+---------------------+--------------------------------+
| Concept             | C++                 | Python                         |
+=====================+=====================+================================+
| Public member       | ``public:``         | No prefix (``self.x``)         |
+---------------------+---------------------+--------------------------------+
| Protected member    | ``protected:``      | Single underscore (``_x``)     |
+---------------------+---------------------+--------------------------------+
| Private member      | ``private:``        | Double underscore (``__x``)    |
+---------------------+---------------------+--------------------------------+
| Enforcement         | Compile-time error  | Convention only (name mangling)|
+---------------------+---------------------+--------------------------------+
| Getter/setter       | Methods             | ``@property``                  |
+---------------------+---------------------+--------------------------------+

In Python, ``__x`` is **name-mangled** to ``_ClassName__x``, making it
inconvenient (but not impossible) to access from outside.  The real
protection is team convention and code review.


@property — Computed Attributes
---------------------------------

.. code-block:: python

    class Circle:
        def __init__(self, radius: float) -> None:
            self.radius = radius   # calls the setter

        @property
        def radius(self) -> float:
            return self._radius

        @radius.setter
        def radius(self, value: float) -> None:
            if value < 0:
                raise ValueError("radius must be non-negative")
            self._radius = value

        @property
        def area(self) -> float:          # read-only computed property
            return math.pi * self._radius ** 2

``@property`` turns a method into an attribute-access syntax.  This lets
you add validation later without changing the API (unlike exposing a plain
``self.radius`` attribute, which cannot validate).


__repr__ and __str__
---------------------

.. code-block:: python

    def __repr__(self) -> str:
        """Machine-readable. Should ideally be eval()-able."""
        return f"Point(x={self.x!r}, y={self.y!r})"

    def __str__(self) -> str:
        """Human-readable. Used by print() and str()."""
        return f"({self.x}, {self.y})"

- ``repr(obj)`` → ``__repr__``; used in REPL, containers, f-string ``{x!r}``
- ``str(obj)`` → ``__str__``; used by ``print()``, f-string ``{x}``
- If only ``__repr__`` is defined, ``str()`` falls back to it.


__eq__ and __hash__
--------------------

.. code-block:: python

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MyClass):
            return NotImplemented  # not False — lets Python try the other side
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

**Rule:** If you define ``__eq__``, you MUST define ``__hash__``, or the class
becomes unhashable (cannot be used in sets or as dict keys).  Return
``NotImplemented`` (not ``False``) when the types are incompatible — this
lets Python try the reverse operation.


@classmethod vs @staticmethod
-------------------------------

.. code-block:: python

    class Temperature:
        @classmethod
        def from_fahrenheit(cls, f: float) -> "Temperature":
            """Named constructor — cls is the class (supports inheritance)."""
            return cls((f - 32) * 5 / 9)

        @staticmethod
        def is_valid_celsius(value: float) -> bool:
            """Utility function — no access to class or instance."""
            return value >= -273.15

- ``@classmethod``: receives ``cls`` as first arg.  Used for factory methods,
  alternative constructors.  Works correctly with inheritance (subclasses
  get the subclass as ``cls``).
- ``@staticmethod``: receives no implicit first arg.  Used for utility
  functions logically related to the class but not needing class/instance.


Instance vs Class Attributes
-------------------------------

.. code-block:: python

    class Dog:
        species = "Canis lupus familiaris"   # class attribute (shared)

        def __init__(self, name: str) -> None:
            self.name = name                  # instance attribute (per-object)

    Dog.species     # access on class
    Dog("Rex").name # access on instance

If an instance has an attribute with the same name as a class attribute,
the instance attribute shadows it (Python's attribute lookup: instance
dict → class dict → base class dicts).


Self-Check Questions
--------------------

**Q1: What is name mangling and does it truly make attributes private?**

Name mangling transforms ``__x`` to ``_ClassName__x`` at compile time.  It
makes accidental access from outside unlikely but does not prevent intentional
access.  Python's philosophy: "we're all consenting adults here" — trust
the programmer, use convention.

**Q2: When should you use** ``@property`` **vs a plain attribute?**

Start with a plain attribute.  Add ``@property`` when you need to:
(1) validate on assignment, (2) compute the value from other state, or
(3) add side effects to reads/writes.  Changing from plain to property is
backward-compatible — callers use the same ``obj.x`` syntax regardless.

**Q3: Why return** ``NotImplemented`` **from** ``__eq__`` **instead of** ``False``**?**

``NotImplemented`` tells Python "I don't know how to compare these".  Python
then tries the reverse: ``other.__eq__(self)``.  Returning ``False`` would
silently make the comparison always false, which is wrong when comparing
against a compatible type defined in another module.

**Q4: What is the "Tell, Don't Ask" principle?**

Instead of getting a value from an object, checking it externally, and then
calling a method based on the check — ask the object to perform the operation.
It encapsulates the decision logic where the invariant is known:

.. code-block:: python

    # ASK (bad)
    if account.balance >= amount:
        account.set_balance(account.balance - amount)

    # TELL (good)
    account.withdraw(amount)   # returns False if insufficient
