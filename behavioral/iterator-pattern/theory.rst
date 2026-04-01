==========================================
Iterator Pattern — Python Guide
==========================================

Overview
--------
The Iterator pattern provides a way to access the elements of an aggregate
object sequentially without exposing its underlying representation.

Intent
------
Decouple traversal algorithms from the collections they traverse.

Structure
---------
.. code-block:: text

    Client ──► Iterator (ABC / protocol)
                    │
        ┌───────────┼──────────┐
    InorderIter  PreorderIter  PostorderIter
                    │
               TreeNode (Aggregate)

Participants
------------
- **Iterator (ABC)** — declares ``__iter__`` and ``__next__``.
- **ConcreteIterator** — implements traversal logic; tracks cursor position.
- **Aggregate** — provides ``__iter__`` that returns a ConcreteIterator.

Python-specific Notes
---------------------
- Python's **iterator protocol** (``__iter__`` / ``__next__``) makes any
  class natively iterable with ``for``, ``list()``, ``sum()``, etc.
- The simplest iterator is a **generator function** using ``yield``.
- ``collections.abc.Iterator`` can be used for ``isinstance`` checks.
- Iterators should be **lazy** — compute values on demand to handle large
  or infinite sequences.
- **Generator expressions** are one-liners: ``(x*2 for x in range(10))``.

When to Use
-----------
- Accessing an aggregate object's contents without exposing its
  internal representation.
- Supporting multiple simultaneous traversals.
- Providing a uniform interface for traversing different aggregates.

Pitfalls
--------
- Once exhausted, a standard iterator cannot be reset (create a new one).
- ``for`` loops already consume iterators — don't iterate twice without
  recreating.
- Concurrent modification of the underlying collection during iteration
  can cause issues.

Related Patterns
----------------
- **Composite** — iterators often traverse composite structures.
- **Memento** — can save iterator position for later resumption.
- **Factory Method** — aggregate can use a factory to return the
  appropriate iterator subclass.
