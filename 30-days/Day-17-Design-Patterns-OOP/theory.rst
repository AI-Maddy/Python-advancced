Day 17 — Design Patterns (OOP)
================================

GoF Pattern Categories
-----------------------

**Creational** — how objects are made

* Singleton, Factory Method, Abstract Factory, Builder, Prototype

**Structural** — how objects are composed

* Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy

**Behavioural** — how objects communicate

* Chain of Responsibility, Command, Interpreter, Iterator, Mediator,
  Memento, Observer, State, Strategy, Template Method, Visitor

Strategy Pattern (Pythonic)
----------------------------

In classical OOP you define a Strategy ABC.  In Python, a strategy is just
a callable (function, lambda, or ``__call__`` object).

.. code-block:: python

    SortStrategy = Callable[[list[int]], list[int]]

    class Sorter:
        def __init__(self, strategy: SortStrategy = sorted) -> None:
            self.strategy = strategy

        def sort(self, data: list[int]) -> list[int]:
            return self.strategy(data)

Observer Pattern (Pythonic)
----------------------------

Keep a list of callables.  Emit by iterating and calling each one.

.. code-block:: python

    class EventEmitter:
        def __init__(self) -> None:
            self._listeners: dict[str, list[Callable]] = {}

        def on(self, event: str, fn: Callable) -> None:
            self._listeners.setdefault(event, []).append(fn)

        def emit(self, event: str, payload=None) -> None:
            for fn in self._listeners.get(event, []):
                fn(event, payload)

Null Object Pattern
--------------------

Return an object with the same interface that does nothing, instead of
``None``.  Eliminates ``if obj is not None:`` guards throughout the code.

.. code-block:: python

    class NullLogger:
        def log(self, msg: str) -> None:
            pass   # intentionally empty

Borg Singleton
--------------

All instances share the same ``__dict__``.  Unlike a true Singleton,
multiple instance objects exist, but they behave identically because their
state is shared.

.. code-block:: python

    class Borg:
        _shared: ClassVar[dict] = {}
        def __init__(self) -> None:
            self.__dict__ = self.__class__._shared

Registry Pattern
----------------

Use ``__init_subclass__`` to auto-register subclasses by a key.

.. code-block:: python

    class Handler:
        _registry: ClassVar[dict[str, type]] = {}

        def __init_subclass__(cls, name: str = "", **kw) -> None:
            super().__init_subclass__(**kw)
            if name:
                Handler._registry[name] = cls

    class JsonHandler(Handler, name="json"): ...

Choosing Patterns
-----------------

* Strategy — swap algorithms at runtime (sorting, compression, pricing).
* Observer — decouple event producers from consumers (UI events, domain events).
* Null Object — simplify code that handles optional dependencies/loggers.
* Borg — shared configuration without enforcing single-instance.
* Registry — plugin systems, serializer registries, ORM model discovery.
