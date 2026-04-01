==========================================
Memento Pattern — Python Guide
==========================================

Overview
--------
The Memento pattern lets you save and restore the previous state of an object
without revealing the details of its implementation.

Intent
------
Capture an object's internal state so it can be restored later, without
violating encapsulation.

Structure
---------
.. code-block:: text

    Caretaker ──── save() / undo() ──► Originator
                                            │
                                       save() → Memento (frozen)
                                       restore(memento)

Participants
------------
- **Memento** — stores a snapshot of Originator state; immutable.
- **Originator** — creates and consumes Mementos.
- **Caretaker** — holds Mementos; never reads their contents.

Python-specific Notes
---------------------
- Use ``@dataclass(frozen=True)`` or ``NamedTuple`` to make Mementos
  immutable — this prevents accidental mutation of saved state.
- ``copy.deepcopy`` ensures snapshots are independent of future mutations.
- The Caretaker pattern maps directly to a Python ``list`` used as a stack
  (``append`` to save, ``pop`` to restore).
- For bounded history, use ``collections.deque(maxlen=N)``.
- Serialising a Memento (via ``json`` or ``pickle``) enables persistent
  undo across sessions.

When to Use
-----------
- A snapshot of an object's state must be saved to be restored later.
- A direct interface to obtaining the state would expose implementation
  details and break encapsulation.

Pitfalls
--------
- Mementos can consume significant memory for large objects — consider
  incremental/delta snapshots.
- Caretakers must not modify or inspect mementos (encapsulation rule).

Related Patterns
----------------
- **Command** — commands can use Mementos to support undo.
- **Prototype** — cloning can replace Mementos for simple cases.
- **Iterator** — can use Mementos to track iteration position.
