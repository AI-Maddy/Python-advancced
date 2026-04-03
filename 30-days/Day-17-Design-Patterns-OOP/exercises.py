"""
Day 17 — Exercises: Design Patterns (OOP)
==========================================
Complete each TODO.
"""
from __future__ import annotations

import json as _json
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
        self._strategies = strategies

    def process(self, text: str) -> str:
        """Apply all strategies in sequence."""
        result = text
        for strategy in self._strategies:
            result = strategy(result)
        return result


def exercise1_strategy() -> str:
    """Should return 'HELLO_WORLD'."""
    processor = TextProcessor([
        str.strip,
        str.upper,
        lambda s: s.replace(" ", "_"),
    ])
    return processor.process("  hello world  ")


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
        self.symbol = symbol
        self._price = initial_price
        self._observers: list[Callable[[float, float], None]] = []

    def add_observer(self, observer: Callable[[float, float], None]) -> None:
        """Register a price-change observer."""
        self._observers.append(observer)

    @property
    def price(self) -> float:
        """Current price."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """Set new price and notify observers."""
        old = self._price
        self._price = new_price
        for obs in self._observers:
            obs(old, new_price)


def exercise2_observer() -> list[str]:
    """Return list of notification messages after two price changes."""
    messages: list[str] = []

    def alert(old: float, new: float) -> None:
        direction = "up" if new > old else "down"
        messages.append(f"Price went {direction}: {old} → {new}")

    def logger(old: float, new: float) -> None:
        messages.append(f"LOG: {old:.2f} → {new:.2f}")

    stock = Stock("AAPL", 150.0)
    stock.add_observer(alert)
    stock.add_observer(logger)
    stock.price = 155.0
    stock.price = 148.0
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
        self.__dict__ = self.__class__._shared
        if "max_connections" not in self._shared:
            self.max_connections: int = 10


def exercise3_borg() -> tuple[int, int]:
    """
    Return (pool1.max_connections, pool2.max_connections) after setting
    pool1.max_connections = 20.  Both should be 20.
    """
    pool1 = DatabasePool()
    pool2 = DatabasePool()
    pool1.max_connections = 20
    return (pool1.max_connections, pool2.max_connections)


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
        super().__init_subclass__(**kwargs)
        if format:
            Serializer._registry[format] = cls

    @classmethod
    def get(cls, format: str) -> type[Serializer]:
        """Retrieve serializer class by format name."""
        try:
            return cls._registry[format]
        except KeyError:
            raise KeyError(f"No serializer for format {format!r}") from None

    def serialize(self, data: dict[str, Any]) -> str:
        """Override in subclasses."""
        raise NotImplementedError


class JsonSerializer(Serializer, format="json"):
    """JSON serializer."""

    def serialize(self, data: dict[str, Any]) -> str:
        """Return JSON string."""
        return _json.dumps(data, separators=(",", ":"))


class XmlSerializer(Serializer, format="xml"):
    """Minimal XML serializer."""

    def serialize(self, data: dict[str, Any]) -> str:
        """Return simple XML string."""
        inner = "".join(f"<{k}>{v}</{k}>" for k, v in data.items())
        return f"<root>{inner}</root>"


def exercise4_registry() -> tuple[str, str]:
    """Return (json_output, xml_output) for {"greeting": "hello"}."""
    data = {"greeting": "hello"}
    json_out = Serializer.get("json")().serialize(data)
    xml_out = Serializer.get("xml")().serialize(data)
    return (json_out, xml_out)


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


def exercise5_null_observer() -> bool:
    """Return True if Stock + NullObserver raises no exceptions."""
    try:
        stock = Stock("MSFT", 300.0)
        stock.add_observer(NullObserver())
        stock.price = 310.0
        stock.price = 295.0
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
