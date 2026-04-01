==========================================
Visitor Pattern — Python Guide
==========================================

Overview
--------
The Visitor pattern lets you add further operations to objects without
modifying them, by separating the algorithm from the object structure.

Intent
------
Define a new operation on elements of an object structure without changing
the element classes.

Structure
---------
.. code-block:: text

    Shape (ABC) ──── accept(Visitor) ──► Visitor (ABC)
        │                                      │
    ┌───┴────┐                    ┌─────────────┼──────────────┐
  Circle  Rectangle  Triangle  AreaCalc  PerimeterCalc  SVGRenderer
      │
  accept(v) → v.visit_circle(self)   ← double-dispatch

Participants
------------
- **Visitor (ABC)** — declares ``visit_*`` for each concrete element type.
- **ConcreteVisitor** — implements each visit method with the specific logic.
- **Element (Shape ABC)** — declares ``accept(visitor)``; calls the correct
  ``visit_*`` method on the visitor (double-dispatch).
- **ConcreteElement** — implements ``accept`` by calling
  ``visitor.visit_<self_type>(self)``.

Python-specific Notes
---------------------
- ``functools.singledispatchmethod`` (Python 3.8+) provides an alternative:
  the visitor's ``visit`` method dispatches on the argument type without
  needing ``accept`` on each element.
- The classic ABC approach here enforces at compile time that all element
  types are handled.
- Type hints make it easy to see what each visitor expects/returns.

When to Use
-----------
- An object structure contains many classes of objects with differing
  interfaces, and you want to perform operations that depend on their
  concrete classes.
- Many distinct and unrelated operations need to be performed on objects
  without polluting their classes.
- The object structure rarely changes but new operations are added often.

Pitfalls
--------
- Adding a new element type requires updating ALL visitors — high coupling.
- Can be overkill for simple structures (use ``isinstance`` chains instead).

Related Patterns
----------------
- **Composite** — visitors often traverse composite structures.
- **Iterator** — can be used to walk the structure; visitor processes nodes.
- **Interpreter** — visitor can interpret nodes in a grammar.
