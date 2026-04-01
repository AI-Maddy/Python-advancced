Day 18 — SOLID Principles
===========================

S — Single Responsibility Principle
-------------------------------------

A class should have only **one reason to change**.

* Split "God classes" into focused collaborators.
* Ask: "What might force this class to change?" — if more than one answer, split.

O — Open/Closed Principle
---------------------------

Software entities should be **open for extension** but **closed for modification**.

* Use Protocols / ABCs to define extension points.
* Add new behaviour by writing a new class, not by editing existing code.
* Python's duck typing + Protocols make this natural.

L — Liskov Substitution Principle
------------------------------------

Subtypes must be **substitutable** for their base type without breaking program
correctness.

Rules for LSP-safe subclasses:

* Pre-conditions may not be strengthened.
* Post-conditions may not be weakened.
* Invariants of the base class must be preserved.

The classic Rectangle/Square violation: ``Square.width = x`` silently changes
``height``, breaking ``area = width * height`` postcondition.

Fix: use a flat hierarchy where both share a ``Shape`` abstract base.

.. code-block:: python

    class Shape(ABC):
        @abstractmethod
        def area(self) -> float: ...

    class Rectangle(Shape): ...   # independent width/height
    class Square(Shape): ...      # single side

I — Interface Segregation Principle
-------------------------------------

Clients should **not be forced to depend on methods they don't use**.

* Prefer narrow Protocols over fat ABCs.
* A ``Robot`` should not implement ``eat()`` just because it shares a ``Worker``
  interface with ``Human``.

D — Dependency Inversion Principle
------------------------------------

* High-level modules should **not** depend on low-level modules.
* Both should depend on **abstractions** (Protocols or ABCs).
* Abstractions should not depend on details; details depend on abstractions.

In Python: inject dependencies via ``__init__``; type-hint against Protocols.

.. code-block:: python

    class MessageSender(Protocol):
        def send(self, to: str, body: str) -> None: ...

    class NotificationService:
        def __init__(self, sender: MessageSender) -> None:
            self._sender = sender   # inject, never instantiate

Summary Table
-------------

.. list-table::
   :header-rows: 1
   :widths: 5 20 30

   * - Letter
     - Name
     - Python Idiom
   * - S
     - Single Responsibility
     - Small focused classes / dataclasses
   * - O
     - Open/Closed
     - Protocol extension points
   * - L
     - Liskov Substitution
     - Flat hierarchies, honour contracts
   * - I
     - Interface Segregation
     - Narrow Protocols, not fat ABCs
   * - D
     - Dependency Inversion
     - Inject Protocol, never import concrete
