==========================================
State Pattern — Python Guide
==========================================

Overview
--------
The State pattern allows an object to alter its behaviour when its internal
state changes.  The object will appear to change its class.

Intent
------
Eliminate large ``if``/``elif`` chains by distributing state-specific
behaviour into separate state classes.

Structure
---------
.. code-block:: text

    Context ──── state: State (ABC)
                     │
          ┌──────────┼──────────┐
       RedState  YellowState  GreenState
           │
       handle(context) → context.set_state(next_state)

Participants
------------
- **State (ABC)** — declares the interface for state-specific behaviour.
- **ConcreteState** — implements the behaviour for a particular state and
  triggers transitions via ``context.set_state()``.
- **Context** — holds the current state; delegates requests to it.

Python-specific Notes
---------------------
- Python classes are first-class objects: store state instances directly
  (no need for static/singleton patterns that C++ sometimes requires).
- ``__repr__`` on state classes produces readable debug output when logging
  transitions.
- ``@dataclass`` on the context with ``state: State = field(init=False)``
  cleanly separates constructor arguments from internal state.
- For simple state machines consider ``enum.Enum`` + a dispatch table; the
  class-based approach here is better when states have complex behaviour.

When to Use
-----------
- An object's behaviour depends on its state and must change at runtime.
- Operations have large, multi-part conditional statements that depend on
  the object's state.

Pitfalls
--------
- Can increase the number of classes significantly.
- States may need to know about each other for transition logic.

Related Patterns
----------------
- **Strategy** — similar structure; Strategy swaps algorithms, State swaps
  behaviour based on internal condition.
- **Singleton** — state objects are often singletons (safe if stateless).
- **Flyweight** — share state objects if they carry no instance data.
