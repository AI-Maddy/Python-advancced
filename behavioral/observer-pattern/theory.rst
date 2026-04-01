==========================================
Observer Pattern — Python Guide
==========================================

Overview
--------
The Observer pattern (also called Publish/Subscribe) defines a one-to-many
dependency so that when a *Subject* changes state, all registered *Observers*
are notified automatically.

Intent
------
Decouple event producers from event consumers so that adding new consumers
never requires changing the producer.

Structure
---------
.. code-block:: text

    Subject ──── attach(Observer) ──►  Observer (ABC)
       │          detach(Observer)          │
       └── notify(event, data) ──────►  update(event, data)

    ConcreteSubject         ConcreteObserver
    (e.g. StockMarket)      (e.g. AlertSystem)

Participants
------------
- **Observer (ABC)** — declares the ``update(event, data)`` interface.
- **Subject** — maintains the observer list; provides ``attach``, ``detach``,
  and ``notify``.
- **ConcreteObserver** — implements reaction logic.

Python-specific Notes
---------------------
- Use ``ABC`` + ``@abstractmethod`` for the ``Observer`` interface.
- ``Subject`` stores observers in a ``dict[str, list[Observer]]`` keyed by
  event name; an empty-string key acts as a wildcard.
- ``@dataclass`` is ideal for simple concrete observers that hold state.
- Python's ``__call__`` protocol or ``functools.partial`` can serve as
  lightweight observers (functions as observers).
- For thread-safety, protect the observer list with ``threading.Lock``.

When to Use
-----------
- When a change in one object requires updating others without knowing how
  many objects need to change.
- When objects should be able to notify others without making assumptions
  about those objects.

Pitfalls
--------
- Forgetting to detach observers causes memory leaks (use ``weakref`` for
  long-lived subjects with short-lived observers).
- Cascading notifications can be hard to debug — keep notification logic
  simple.
- Observer update order should not be relied upon.

Related Patterns
----------------
- **Mediator** — centralises communication between many objects.
- **Event Bus** — a variant where a central broker routes messages.
- **Strategy** — observers can themselves use strategies for their reaction
  logic.
