==========================================
Command Pattern — Python Guide
==========================================

Overview
--------
The Command pattern encapsulates a request as an object, thereby letting you
parameterise clients with different requests, queue or log requests, and
support undoable operations.

Intent
------
Turn method calls into first-class objects so they can be stored, passed,
queued, and reversed.

Structure
---------
.. code-block:: text

    Client ──► CommandHistory (Invoker) ──► Command (ABC)
                                               │
                                   ┌───────────┼───────────┐
                              InsertCmd   DeleteCmd   ReplaceCmd
                                   │
                              TextEditor (Receiver)

Participants
------------
- **Command (ABC)** — declares ``execute()`` and ``undo()``.
- **ConcreteCommand** — binds a Receiver action to the Command interface;
  stores state needed for undo.
- **Receiver** — knows how to perform the operations (e.g. ``TextEditor``).
- **Invoker** — holds and executes commands; manages the undo stack.
- **Client** — creates ConcreteCommand objects and sets the receiver.

Python-specific Notes
---------------------
- ``@dataclass`` is ideal for command objects: receiver + parameters become
  constructor arguments; undo state is stored as ``field(init=False)``.
- For simple one-off commands, a ``functools.partial`` or lambda (wrapped in
  a thin adapter) can replace a full class.
- Python's ``list`` serves perfectly as an undo stack (``append``/``pop``).
- Consider ``collections.deque(maxlen=N)`` to cap history size.

When to Use
-----------
- Parameterising objects with operations.
- Operations need to be queued, logged, or scheduled.
- You need reversible operations (undo/redo).
- You want to structure a system around high-level operations built from
  primitive operations (macro recording).

Pitfalls
--------
- Command objects can proliferate; keep them focused.
- Undo can be complex if commands have side effects outside the receiver.
- For purely functional data, a snapshot approach (Memento) may be simpler.

Related Patterns
----------------
- **Memento** — used to capture state for undo inside a command.
- **Composite** — MacroCommand is a Composite of commands.
- **Strategy** — both encapsulate algorithms; Strategy focuses on
  interchangeability, Command on encapsulating requests.
