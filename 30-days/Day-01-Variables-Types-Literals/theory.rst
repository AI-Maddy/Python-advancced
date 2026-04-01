Day 01 — Variables, Types, and Literals
========================================

Why This Day Matters
--------------------

Types are the vocabulary of a program. Understanding Python's type system —
what it shares with C++ and where it diverges — lets you write correct,
readable code and reason about the implicit contracts in your interfaces.


Python Built-in Types
----------------------

+------------+------------------+-------------------------------------------+
| Type       | C++ equivalent   | Key differences                           |
+============+==================+===========================================+
| ``int``    | ``long long``    | **Arbitrary precision** — never overflows |
+------------+------------------+-------------------------------------------+
| ``float``  | ``double``       | IEEE 754, 64-bit — identical behaviour    |
+------------+------------------+-------------------------------------------+
| ``complex``| ``std::complex`` | Built-in, not a library type              |
+------------+------------------+-------------------------------------------+
| ``bool``   | ``bool``         | Subtype of ``int``; True==1, False==0     |
+------------+------------------+-------------------------------------------+
| ``str``    | ``std::string``  | **Unicode** (UTF-8 decode); immutable     |
+------------+------------------+-------------------------------------------+
| ``bytes``  | ``std::string``  | Raw bytes; use for binary/network data    |
+------------+------------------+-------------------------------------------+
| ``None``   | ``nullptr``      | Singleton; always test with ``is``        |
+------------+------------------+-------------------------------------------+

The most important difference from C++: Python ``int`` never overflows.
``10 ** 1000`` is a valid Python integer.


Dynamic vs Static Typing
--------------------------

.. code-block:: python

    # Python: variable is a label; type lives on the object
    x = 42          # x points to an int object
    x = "hello"     # x now points to a str object — perfectly legal

    # C++ equivalent would be a compile error:
    # int x = 42;
    # x = "hello";   // ERROR: cannot assign string to int

Type annotations are optional but strongly recommended (PEP 526):

.. code-block:: python

    age: int = 25            # annotated
    name: str = "Alice"
    price: float = 9.99

Annotations are **not enforced at runtime** by default.  Run ``mypy --strict``
or ``pyright`` to get compile-time-like checking.


The bool / int Relationship
-----------------------------

.. code-block:: python

    isinstance(True, int)   # True — bool IS a subtype of int
    True + True             # 2
    True * 5                # 5

This surprises C++ programmers.  It is a deliberate Python design choice that
enables uses like ``sum(x > 0 for x in lst)`` to count truthy values.

**Always check for** ``bool`` **before** ``int`` **in** ``isinstance`` **chains:**

.. code-block:: python

    if isinstance(value, bool):   # must come first!
        ...
    elif isinstance(value, int):
        ...


is vs ==
---------

.. code-block:: python

    a = [1, 2, 3]
    b = [1, 2, 3]   # same value, different object

    a == b      # True  — value equality (__eq__)
    a is b      # False — identity (same memory address)

    # is is correct for None:
    x = None
    x is None     # True  — idiomatic
    x == None     # True  — but == can be overridden; don't use for None

**Rule:** Use ``is`` for ``None`` (and ``True``/``False`` when exact singleton
check matters).  Use ``==`` for value comparison.


f-strings (PEP 498 / PEP 701)
-------------------------------

.. code-block:: python

    name = "Python"
    pi = 3.14159

    # Format specifications after the colon
    f"{pi:.2f}"          # "3.14"    — 2 decimal places
    f"{pi:.2e}"          # "3.14e+00" — scientific notation
    f"{42:#010x}"        # "0x0000002a" — hex with zero-pad
    f"{'left':<10}"      # "left      " — left-align in 10 chars
    f"{'right':>10}"     # "     right" — right-align
    f"{'center':^10}"    # "  center  " — centre

    # Debug format (Python 3.8+)
    x = 42
    f"{x=}"             # "x=42"


Arbitrary-Precision Integers
------------------------------

C++ fixed-width integers overflow silently::

    // C++: undefined behaviour
    int x = INT_MAX;
    int y = x + 1;   // UB: wrap-around on most platforms

Python integers grow as needed::

    # Python: just works
    googol = 10 ** 100
    factorial_100 = 1
    for i in range(1, 101):
        factorial_100 *= i
    # factorial_100 has 158 digits — no overflow


Self-Check Questions
--------------------

**Q1: Why does** ``isinstance(True, int)`` **return** ``True`` **in Python?**

Because ``bool`` is a subclass of ``int``.  ``True`` and ``False`` are
instances of ``bool``, which inherits from ``int``.  This is why you must
check for ``bool`` before ``int`` in type-dispatch logic.

**Q2: What is the difference between** ``is`` **and** ``==``**?**

``is`` checks **identity** — whether two names refer to the exact same object
(same ``id()``).  ``==`` checks **equality** — whether two objects have the
same value (via ``__eq__``).  Use ``is`` for ``None``; use ``==`` for values.

**Q3: Why doesn't Python have** ``int32_t`` **or** ``uint64_t``**?**

Python's ``int`` is arbitrary precision — the runtime grows the underlying
storage as needed.  For low-level bit manipulation or interfacing with C
libraries, use the ``ctypes`` module or ``struct`` for fixed-width types, or
use ``numpy`` arrays for typed numeric arrays.

**Q4: When should you use** ``bytes`` **instead of** ``str``**?**

Use ``bytes`` for binary data (network packets, file I/O, cryptography) and
``str`` for human-readable text.  Always decode bytes to str at the boundary
of your program (reading a file: ``open(path, encoding="utf-8")``) and encode
str to bytes when writing binary output.
