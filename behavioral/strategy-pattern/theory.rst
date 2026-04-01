==========================================
Strategy Pattern — Python Guide
==========================================

Overview
--------
The Strategy pattern defines a family of algorithms, encapsulates each one,
and makes them interchangeable, letting the algorithm vary independently from
the clients that use it.

Intent
------
Swap algorithms (or behaviours) at runtime without modifying the context class.

Structure
---------
.. code-block:: text

    Context ──── strategy: Strategy (ABC)
                     │
          ┌──────────┼──────────┐
    ConcreteA   ConcreteB   ConcreteC

Participants
------------
- **Strategy (ABC)** — declares the algorithm interface (e.g. ``sort``).
- **ConcreteStrategy** — implements the algorithm.
- **Context** — holds a reference to a strategy; delegates work to it.

Python-specific Notes
---------------------
- ABCs give a formal interface contract; ``isinstance`` checks work cleanly.
- Because Python functions are first-class objects, simple strategies can be
  plain callables rather than classes — useful when no state is needed.
- ``@dataclass`` works well for strategies that hold configuration (e.g.
  compression level, sort key).
- Type aliases like ``SortFn = Callable[[list], list]`` document callable
  strategies without needing a full ABC.

When to Use
-----------
- Many related classes differ only in behaviour.
- You need different variants of an algorithm.
- An algorithm uses data the client shouldn't know about.
- A class defines many behaviours using conditional statements.

Pitfalls
--------
- Too many small strategy classes can increase complexity — consider using
  plain functions or ``functools.partial`` for simple cases.
- Context and strategy must agree on a clear interface contract.

Related Patterns
----------------
- **Template Method** — uses inheritance instead of composition for varying
  algorithm steps.
- **Command** — a command can wrap a strategy.
- **Decorator** — adds behaviour; Strategy replaces behaviour.
