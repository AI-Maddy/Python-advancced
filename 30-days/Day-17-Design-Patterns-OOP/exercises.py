"""
Day 17 — Exercises: Design Patterns (OOP)
==========================================
Complete each TODO.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any, ClassVar


# ---------------------------------------------------------------------------
# Exercise 1 — Function-based Strategy
# ---------------------------------------------------------------------------
# TODO: Implement a TextProcessor class that accepts a list of
#       transformation strategies (callables: str -> str).
#       process(text) applies all strategies in order.
#       Demonstrate with: strip, upper, and a custom replace(' ', '_') step.

class TextProcessor:
    """Applies a pipeline of string transformation strategies."""

    def __init__(self, strategies: list[Callable[[str], str]]) -> None:
        # TODO
        ...

    def process(self, text: str) -> str:
        """Apply all strategies in sequence."""
        # TODO
        ...
        return text


def exercise1_strategy() -> str:
    """Should return 'HELLO_WORLD'."""
    # TODO: build processor with strip, upper, replace-space strategies
    ...
    return ""


# ---------------------------------------------------------------------------
# Exercise 2 — Callable Observer List
# ---------------------------------------------------------------------------
# TODO: Implement a Stock class with a price attribute.
#       When price changes, notify all registered observers (callables).
#       Observer signature: (old_price: float, new_price: float) -> None
#       Demonstrate with two observers that print messages.

class Stock:
    """Represents a stock with an observable price."""

    def __init__(self, symbol: str, initial_price: float) -> None:
        # TODO
        ...

    def add_observer(self, observer: Callable[[float, float], None]) -> None:
        """Register a price-change observer."""
        # TODO
        ...

    @property
    def price(self) -> float:
        """Current price."""
        # TODO
        ...
        return 0.0

    @price.setter
    def price(self, new_price: float) -> None:
        """Set new price and notify observers."""
        # TODO
        ...


def exercise2_observer() -> list[str]:
    """Return list of notification messages after two price changes."""
    messages: list[str] = []
    # TODO: create Stock, add observers that append to messages, change price twice
    ...
    return messages


# ---------------------------------------------------------------------------
# Exercise 3 — Borg Singleton
# ---------------------------------------------------------------------------
# TODO: Implement a DatabasePool class using Borg pattern.
#       It should have a max_connections attribute (default 10).
#       Show that two instances share state when max_connections is changed.

class DatabasePool:
    """Borg-based database connection pool config."""

    _shared: ClassVar[dict[str, Any]] = {}

    def __init__(self) -> None:
        # TODO: hook __dict__ to _shared, set defaults on first init
        ...


def exercise3_borg() -> tuple[int, int]:
    """
    Return (pool1.max_connections, pool2.max_connections) after setting
    pool1.max_connections = 20.  Both should be 20.
    """
    # TODO
    ...
    return (0, 0)


# ---------------------------------------------------------------------------
# Exercise 4 — Registry via __init_subclass__
# ---------------------------------------------------------------------------
# TODO: Create a Serializer base class with a registry.
#       Subclasses pass format="json", format="yaml", etc.
#       Each subclass implements serialize(data: dict) -> str.
#       Implement JsonSerializer and XmlSerializer (XML can be fake/simple).
#       Demonstrate Serializer.get("json")().serialize({"k": "v"}).

class Serializer:
    """Auto-registering serializer base class."""

    _registry: ClassVar[dict[str, type[Serializer]]] = {}

    def __init_subclass__(cls, format: str = "", **kwargs: Any) -> None:
        # TODO: register cls under format key
        ...

    @classmethod
    def get(cls, format: str) -> type[Serializer]:
        """Retrieve serializer class by format name."""
        # TODO
        ...
        raise KeyError(format)

    def serialize(self, data: dict[str, Any]) -> str:
        """Override in subclasses."""
        raise NotImplementedError


class JsonSerializer(Serializer, format="json"):
    """JSON serializer."""

    def serialize(self, data: dict[str, Any]) -> str:
        """Return JSON string."""
        # TODO
        ...
        return ""


class XmlSerializer(Serializer, format="xml"):
    """Minimal XML serializer."""

    def serialize(self, data: dict[str, Any]) -> str:
        """Return simple XML string."""
        # TODO — e.g. "<root><key>value</key></root>"
        ...
        return ""


def exercise4_registry() -> tuple[str, str]:
    """Return (json_output, xml_output) for {"greeting": "hello"}."""
    # TODO
    ...
    return ("", "")


# ---------------------------------------------------------------------------
# Exercise 5 — Null Object + Observer combo
# ---------------------------------------------------------------------------
# TODO: Create a NullObserver that satisfies the same interface as a real
#       observer but does nothing.  Verify the Stock class works when given
#       a NullObserver (no errors, no output).

class NullObserver:
    """Null observer — silently discards notifications."""

    def __call__(self, old_price: float, new_price: float) -> None:
        """Do nothing."""
        # TODO
        ...


def exercise5_null_observer() -> bool:
    """Return True if Stock + NullObserver raises no exceptions."""
    try:
        # TODO: create Stock, add NullObserver, change price
        ...
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_strategy())
    print("Exercise 2:", exercise2_observer())
    print("Exercise 3:", exercise3_borg())
    print("Exercise 4:", exercise4_registry())
    print("Exercise 5:", exercise5_null_observer())
