==========================================
Template Method Pattern — Python Guide
==========================================

Overview
--------
The Template Method pattern defines the skeleton of an algorithm in an
operation, deferring some steps to subclasses.  Subclasses can redefine
certain steps of the algorithm without changing its structure.

Intent
------
Define a fixed algorithm structure with variable implementation steps, using
inheritance to customise specific steps.

Structure
---------
.. code-block:: text

    DataProcessor (ABC)
        │
        ├── process()            ← template method (final skeleton)
        │     ├── before_process()   (optional hook)
        │     ├── read()             (abstract)
        │     ├── transform()        (abstract)
        │     ├── write()            (abstract)
        │     └── after_process()    (optional hook)
        │
        ├── CSVProcessor
        ├── JSONProcessor
        └── XMLProcessor

Participants
------------
- **AbstractClass** — defines the template method and abstract step hooks.
- **ConcreteClass** — implements the abstract steps.
- **Hooks** — optional steps with default (no-op) implementations.

Python-specific Notes
---------------------
- The template method should be a concrete method on the ABC (not abstract).
- Use ``typing.final`` (Python 3.8+) on the template method to signal it
  should not be overridden.
- Python ABCs allow mixing abstract and concrete methods naturally.
- ``@dataclass`` can hold pipeline inputs/outputs to avoid constructor sprawl.

When to Use
-----------
- Several classes share the same algorithm structure, differing only in
  specific steps.
- Avoiding code duplication in subclasses while letting them customise
  behaviour.
- Controlling which parts of an algorithm subclasses may override.

Pitfalls
--------
- Deep inheritance hierarchies make it hard to understand which methods
  are called — prefer composition (Strategy) for complex cases.
- Clients can only vary the fixed points (hooks); too many hooks reduce
  clarity.

Related Patterns
----------------
- **Strategy** — uses composition instead of inheritance to vary algorithms.
- **Factory Method** — a specialisation of Template Method for object
  creation.
- **Hook Method** — a variant where hooks have default implementations.
