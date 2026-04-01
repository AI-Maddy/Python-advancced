"""
Day 17 — Design Patterns (OOP)
================================
Topics:
  - All 23 GoF patterns briefly categorized
  - Strategy: just a callable, no ABC needed
  - Observer: list of callables
  - Null Object pattern
  - Borg singleton (Pythonic alternative)
  - Registry pattern via class variable dict
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, ClassVar, TypeVar

T = TypeVar("T")

# ===========================================================================
# 1. GoF Patterns — brief catalogue
# ===========================================================================
# CREATIONAL (how objects are created)
#   Singleton, Factory Method, Abstract Factory, Builder, Prototype
#
# STRUCTURAL (how objects are composed)
#   Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
#
# BEHAVIOURAL (how objects communicate)
#   Chain of Responsibility, Command, Interpreter, Iterator, Mediator,
#   Memento, Observer, State, Strategy, Template Method, Visitor


# ===========================================================================
# 2. Strategy — just a callable
# ===========================================================================
# Traditional OOP: define an ABC, create concrete subclasses.
# Python: a strategy IS a function / callable object — no ABC needed.

SortStrategy = Callable[[list[int]], list[int]]


def bubble_sort(data: list[int]) -> list[int]:
    """O(n^2) sort — useful for nearly-sorted small lists."""
    lst = data[:]
    n = len(lst)
    for i in range(n):
        for j in range(n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


def python_sort(data: list[int]) -> list[int]:
    """Timsort — Python's built-in, O(n log n)."""
    return sorted(data)


class Sorter:
    """Context that delegates sorting to a strategy callable."""

    def __init__(self, strategy: SortStrategy = python_sort) -> None:
        self.strategy = strategy

    def sort(self, data: list[int]) -> list[int]:
        """Apply the strategy."""
        return self.strategy(data)

    def set_strategy(self, strategy: SortStrategy) -> None:
        """Swap strategy at runtime."""
        self.strategy = strategy


def demo_strategy() -> None:
    """Demonstrate Strategy pattern with callables."""
    sorter = Sorter(bubble_sort)
    data = [5, 2, 8, 1, 9]
    print("Bubble sort:", sorter.sort(data))

    sorter.set_strategy(python_sort)
    print("Python sort:", sorter.sort(data))

    # Lambda as one-off strategy
    sorter.set_strategy(lambda d: sorted(d, reverse=True))
    print("Reverse sort:", sorter.sort(data))


# ===========================================================================
# 3. Observer — list of callables
# ===========================================================================
# Traditional OOP: Observer ABC + Subject that keeps a list.
# Python: subject keeps a list of plain callables.

Listener = Callable[[str, Any], None]


class EventEmitter:
    """
    Simple publish-subscribe event bus.

    Observers are plain callables: ``listener(event_name, payload)``.
    """

    def __init__(self) -> None:
        self._listeners: dict[str, list[Listener]] = {}

    def on(self, event: str, listener: Listener) -> None:
        """Register a listener for an event."""
        self._listeners.setdefault(event, []).append(listener)

    def off(self, event: str, listener: Listener) -> None:
        """Unregister a listener."""
        self._listeners.get(event, []).remove(listener)

    def emit(self, event: str, payload: Any = None) -> None:
        """Notify all registered listeners."""
        for listener in self._listeners.get(event, []):
            listener(event, payload)


def demo_observer() -> None:
    """Demonstrate Observer with callable listeners."""
    bus = EventEmitter()

    log: list[str] = []

    def on_login(event: str, user: Any) -> None:
        log.append(f"LOG: {event} → {user}")

    def on_login_alert(event: str, user: Any) -> None:
        log.append(f"ALERT: Welcome {user}!")

    bus.on("login", on_login)
    bus.on("login", on_login_alert)
    bus.emit("login", "alice")

    bus.off("login", on_login_alert)
    bus.emit("login", "bob")   # only on_login fires

    for entry in log:
        print(entry)


# ===========================================================================
# 4. Null Object pattern
# ===========================================================================
# Instead of returning None (and forcing callers to check), return an object
# that implements the interface but does nothing.

class Logger:
    """Simple logger interface."""

    def log(self, message: str) -> None:
        """Log a message (real implementation)."""
        print(f"[LOG] {message}")


class NullLogger:
    """
    Null Object — same interface as Logger but does nothing.
    Callers never need to check 'if logger is not None'.
    """

    def log(self, message: str) -> None:
        """Silently discard message."""


class Service:
    """A service that optionally logs actions."""

    def __init__(self, logger: Logger | NullLogger | None = None) -> None:
        # Default to NullLogger so callers don't have to check
        self._logger: Logger | NullLogger = logger if logger is not None else NullLogger()

    def do_work(self, task: str) -> str:
        """Perform work and log it."""
        self._logger.log(f"Starting {task}")
        result = f"{task} done"
        self._logger.log(f"Finished {task}")
        return result


def demo_null_object() -> None:
    """Demonstrate Null Object pattern."""
    verbose_svc = Service(Logger())
    silent_svc = Service()           # NullLogger used — no output

    print("Verbose service:")
    result = verbose_svc.do_work("report generation")
    print(f"Result: {result}")

    print("\nSilent service (no log output):")
    result = silent_svc.do_work("background sync")
    print(f"Result: {result}")


# ===========================================================================
# 5. Borg Singleton — shared state, multiple instances
# ===========================================================================
# Classic Singleton: only one instance ever created (__new__ trick or metaclass).
# Borg: multiple instances, but they all share the SAME __dict__.
# More Pythonic because subclassing works naturally.

class Borg:
    """Base Borg class — all instances share state."""
    _shared: ClassVar[dict[str, Any]] = {}

    def __init__(self) -> None:
        self.__dict__ = self.__class__._shared


class AppConfig(Borg):
    """
    Application configuration — every instance reflects the same state.

    >>> c1 = AppConfig()
    >>> c1.debug = True
    >>> c2 = AppConfig()
    >>> c2.debug
    True
    """

    def __init__(self) -> None:
        super().__init__()
        if not self._shared:
            self.debug: bool = False
            self.version: str = "1.0"


def demo_borg() -> None:
    """Demonstrate Borg pattern."""
    c1 = AppConfig()
    c2 = AppConfig()

    print(f"Before: c1.debug={c1.debug}, c2.debug={c2.debug}")
    c1.debug = True
    print(f"After setting c1.debug=True:")
    print(f"  c1.debug={c1.debug}, c2.debug={c2.debug}")
    print(f"  c1 is c2: {c1 is c2}")   # False — different instances
    print(f"  same __dict__: {c1.__dict__ is c2.__dict__}")  # True


# ===========================================================================
# 6. Registry pattern — class variable dict
# ===========================================================================
# Maintain a central registry of all subclasses/plugins, keyed by name.
# Used extensively in frameworks (Django models, SQLAlchemy, click).

class HandlerRegistry:
    """
    Base class that automatically registers all concrete subclasses.
    Override ``name`` class attribute in each subclass.
    """
    _registry: ClassVar[dict[str, type[HandlerRegistry]]] = {}
    name: ClassVar[str] = ""

    def __init_subclass__(cls, name: str = "", **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if name:
            cls.name = name
            HandlerRegistry._registry[name] = cls

    @classmethod
    def get(cls, name: str) -> type[HandlerRegistry]:
        """Look up a handler class by name."""
        try:
            return cls._registry[name]
        except KeyError:
            raise KeyError(f"No handler registered for {name!r}") from None

    @classmethod
    def all_names(cls) -> list[str]:
        """Return all registered names."""
        return list(cls._registry.keys())

    def handle(self, data: Any) -> str:
        """Process data — override in subclasses."""
        raise NotImplementedError


class JsonHandler(HandlerRegistry, name="json"):
    """Handles JSON data."""

    def handle(self, data: Any) -> str:
        """Return data as JSON string."""
        import json
        return json.dumps(data)


class CsvHandler(HandlerRegistry, name="csv"):
    """Handles CSV-like data (list of lists)."""

    def handle(self, data: Any) -> str:
        """Return rows as CSV lines."""
        import csv, io
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerows(data)
        return buf.getvalue().strip()


def demo_registry() -> None:
    """Demonstrate Registry pattern."""
    print("Registered handlers:", HandlerRegistry.all_names())

    handler_cls = HandlerRegistry.get("json")
    handler = handler_cls()
    print("JSON:", handler.handle({"x": 1, "y": 2}))

    csv_handler = HandlerRegistry.get("csv")()
    print("CSV:", csv_handler.handle([["a", "b"], [1, 2]]))


# ===========================================================================
# Main demo
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 17 — Design Patterns (OOP)")
    print("=" * 60)

    print("\n--- Strategy Pattern ---")
    demo_strategy()

    print("\n--- Observer Pattern ---")
    demo_observer()

    print("\n--- Null Object Pattern ---")
    demo_null_object()

    print("\n--- Borg Singleton ---")
    demo_borg()

    print("\n--- Registry Pattern ---")
    demo_registry()
