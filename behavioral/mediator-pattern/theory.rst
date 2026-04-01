==========================================
Mediator Pattern — Python Guide
==========================================

Overview
--------
The Mediator pattern defines an object that encapsulates how a set of objects
interact, promoting loose coupling by keeping objects from referring to each
other explicitly.

Intent
------
Replace a tangle of object-to-object references with a single centralised
mediator that routes all communication.

Structure
---------
.. code-block:: text

    ColleagueA ──► Mediator (ABC) ◄── ColleagueB
    ColleagueC ──►      │          ◄── ColleagueD
                   notify(sender, event, data)
                        │
                   ChatRoom / ATCTower / DialogMediator

Participants
------------
- **Mediator (ABC)** — declares the ``notify`` interface.
- **ConcreteMediator** — implements coordination logic between colleagues.
- **Colleague** — each colleague communicates only through the mediator.

Python-specific Notes
---------------------
- Colleagues receive the mediator at construction time (dependency
  injection); no global state needed.
- ``@dataclass`` suits colleague objects well — the mediator reference
  is just another field.
- For very simple cases, a bare function or ``signal`` (e.g. from the
  ``blinker`` library) can replace a full mediator class.
- The mediator can use a dictionary keyed by event name to dispatch to
  specific handler methods, keeping ``notify`` clean.

When to Use
-----------
- A set of objects communicate in well-defined but complex ways.
- Reusing an object is difficult because it refers to and communicates
  with many other objects.
- Behaviour distributed between several classes should be customisable
  without a lot of subclassing.

Pitfalls
--------
- The mediator itself can become a "God object" if it accumulates too
  much logic.
- Keep mediator logic thin — delegate complex behaviour back to colleagues.

Related Patterns
----------------
- **Observer** — colleagues can observe the mediator.
- **Facade** — Facade simplifies an interface; Mediator adds new behaviour
  by coordinating colleagues.
- **Command** — commands can be routed through a mediator.
