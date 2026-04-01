Day 07 — ABCs, Protocols, and Duck Typing
==========================================

Why This Day Matters
--------------------

Python offers three distinct approaches to typing interfaces: duck typing
(structural, implicit), ABCs (nominal, explicit hierarchy), and Protocols
(structural, explicit, statically checked).  Choosing the right approach
determines API clarity, testability, and type-checker integration.


Duck Typing
-----------

Python's default is duck typing — if an object has the right methods and
attributes, it works, regardless of its declared type:

.. code-block:: python

    def quack(obj):
        return obj.quack()   # no type check — any object with quack() works

Duck typing is flexible but provides no static guarantees.  Use it for
simple scripts and internal code; use Protocols for public APIs.


ABCs — Nominal Subtyping
--------------------------

.. code-block:: python

    from abc import ABC, abstractmethod

    class Shape(ABC):
        @abstractmethod
        def area(self) -> float: ...

        def describe(self) -> str:           # concrete method
            return f"area={self.area():.2f}"

    class Circle(Shape):
        def area(self) -> float: ...        # MUST implement

    Shape()     # TypeError: Can't instantiate abstract class

ABCs enforce that subclasses implement specific methods.  They also allow
sharing concrete implementations across the hierarchy.


Protocols — Structural Subtyping (PEP 544)
-------------------------------------------

.. code-block:: python

    from typing import Protocol, runtime_checkable

    @runtime_checkable
    class Drawable(Protocol):
        def draw(self) -> str: ...

    class SVGCircle:
        def draw(self) -> str:
            return "<circle/>"

    isinstance(SVGCircle(), Drawable)   # True — no inheritance needed!

Protocols allow static type checkers (mypy, pyright) to verify structural
compatibility without any inheritance relationship.  ``@runtime_checkable``
adds ``isinstance()`` support (only checks method existence, not signatures).


ABCs vs Protocols — Decision Guide
------------------------------------

+---------------------------+-------------------+-----------------------+
| When to use               | ABC               | Protocol              |
+===========================+===================+=======================+
| Shared implementation     | Yes               | No                    |
+---------------------------+-------------------+-----------------------+
| Formal is-a hierarchy     | Yes               | No                    |
+---------------------------+-------------------+-----------------------+
| Third-party classes       | No (can't inherit)| Yes                   |
+---------------------------+-------------------+-----------------------+
| Static type checking      | Both work         | Preferred             |
+---------------------------+-------------------+-----------------------+
| isinstance() at runtime   | Yes               | With @runtime_checkable|
+---------------------------+-------------------+-----------------------+

Rule: **Protocols for public API type hints; ABCs for framework base classes.**


__subclasshook__ — Virtual Subclasses
---------------------------------------

.. code-block:: python

    class Closeable(ABC):
        @classmethod
        def __subclasshook__(cls, C: type) -> bool:
            if cls is Closeable:
                if any("close" in B.__dict__ for B in C.__mro__):
                    return True
            return NotImplemented

    class FileHandle:
        def close(self): ...

    isinstance(FileHandle(), Closeable)   # True — via __subclasshook__

Also: ``ABC.register(cls)`` explicitly registers a class as virtual subclass.


collections.abc
----------------

The standard library provides ABCs for built-in types:

.. code-block:: python

    from collections.abc import Sequence, Mapping, Iterable, Iterator

    isinstance([1,2,3], Sequence)   # True
    isinstance({}, Mapping)          # True
    isinstance(iter([]), Iterator)   # True

Use these to annotate functions that accept any sequence or mapping,
not just specific ``list`` or ``dict`` types.


Self-Check Questions
--------------------

**Q1: What is the difference between nominal and structural subtyping?**

Nominal: a class is a subtype if it explicitly inherits (``class Dog(Animal)``).
Structural: a class is a subtype if it has the required attributes/methods,
regardless of inheritance.  Python's ``Protocol`` is structural; ``ABC`` is nominal.

**Q2: When does** ``@runtime_checkable`` **not help?**

``@runtime_checkable`` only checks that the methods *exist* at runtime — it
does not check signatures or return types.  ``isinstance(obj, MyProtocol)``
can return ``True`` even if the method has the wrong signature.  Signature
verification is only done by static type checkers.

**Q3: Can you mix ABCs and Protocols?**

Yes.  A class can inherit from ABCs (for shared implementation) and a
separate Protocol can describe the minimal interface for external callers.
The ABC is for the implementors; the Protocol is for the consumers.

**Q4: What is** ``ABC.register(SomeClass)`` **and when would you use it?**

``register()`` declares ``SomeClass`` as a virtual subclass of the ABC,
making ``isinstance(obj, MyABC)`` return ``True`` for instances of ``SomeClass``
without any inheritance.  Use it when you cannot modify the class being
registered (third-party or legacy code) but need it to satisfy an interface.
