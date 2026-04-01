==========================================
Chain of Responsibility Pattern — Python Guide
==========================================

Overview
--------
The Chain of Responsibility pattern passes a request along a chain of
handlers.  Upon receiving a request, each handler decides either to process
it or to pass it to the next handler in the chain.

Intent
------
Avoid coupling the sender of a request to its receiver by giving more than
one object a chance to handle the request.

Structure
---------
.. code-block:: text

    Client ──► Handler1 ──► Handler2 ──► Handler3 ──► (None)
                  │               │             │
              handle()        handle()      handle()
              (or forward)    (or forward)  (or forward)

Participants
------------
- **Handler (ABC)** — declares the ``handle()`` interface and holds a
  reference to the next handler (``_next``).
- **ConcreteHandler** — processes requests it is responsible for; otherwise
  forwards to ``_next``.
- **Client** — initiates the request to the first handler in the chain.

Python-specific Notes
---------------------
- ``set_next`` returning ``self`` (or the next handler) enables fluent
  chaining: ``h1.set_next(h2).set_next(h3)``.
- Returning ``None`` for unhandled requests is clean and Pythonic (no
  sentinel objects needed).
- Middleware frameworks (Django, Flask, Starlette) use this pattern
  extensively.  The ``__call__`` protocol can replace ``handle`` for WSGI
  compatibility.
- ``functools.reduce`` can build chains programmatically from a list of
  handlers.

When to Use
-----------
- More than one object may handle a request, and the handler isn't known
  a priori.
- You want to issue a request without specifying the receiver explicitly.
- The set of handlers should be specifiable dynamically.

Pitfalls
--------
- A request can go unhandled if the chain is not properly configured.
- Debugging long chains can be difficult — add logging at each step.
- Performance-sensitive paths should keep chains short.

Related Patterns
----------------
- **Composite** — chain can be implemented as a composite.
- **Command** — commands can be chained.
- **Decorator** — adds behaviour at every step (CoR stops at first match).
