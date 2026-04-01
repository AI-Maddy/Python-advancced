"""
Day 07 — Solutions
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Exercise 1: Drawable Protocol
# ---------------------------------------------------------------------------

@runtime_checkable
class Drawable(Protocol):
    """Structural: anything with draw() and area()."""
    def draw(self) -> str: ...
    def area(self) -> float: ...


class SVGCircle:
    """Satisfies Drawable structurally — no inheritance."""
    def __init__(self, r: float) -> None:
        self.r = r

    def draw(self) -> str:
        return f"<circle r='{self.r}'/>"

    def area(self) -> float:
        import math
        return math.pi * self.r ** 2


class SVGRect:
    def __init__(self, w: float, h: float) -> None:
        self.w = w
        self.h = h

    def draw(self) -> str:
        return f"<rect width='{self.w}' height='{self.h}'/>"

    def area(self) -> float:
        return self.w * self.h


def render_all(drawables: list[Drawable]) -> list[str]:
    return [d.draw() for d in drawables]


# ---------------------------------------------------------------------------
# Exercise 2: Sortable ABC
# ---------------------------------------------------------------------------

class Sortable(ABC):
    """ABC: provides sort key; __lt__/__gt__ derived from it."""

    @abstractmethod
    def sort_key(self) -> float:
        ...

    def __lt__(self, other: "Sortable") -> bool:
        return self.sort_key() < other.sort_key()

    def __le__(self, other: "Sortable") -> bool:
        return self.sort_key() <= other.sort_key()

    def __gt__(self, other: "Sortable") -> bool:
        return self.sort_key() > other.sort_key()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sortable):
            return NotImplemented
        return self.sort_key() == other.sort_key()

    def __hash__(self) -> int:
        return hash(self.sort_key())


class Temperature(Sortable):
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius

    def sort_key(self) -> float:
        return self.celsius

    def __repr__(self) -> str:
        return f"Temperature({self.celsius}°C)"


class Priority(Sortable):
    LEVELS = {"low": 1, "medium": 2, "high": 3, "critical": 4}

    def __init__(self, name: str) -> None:
        self.name = name

    def sort_key(self) -> float:
        return float(self.LEVELS.get(self.name, 0))

    def __repr__(self) -> str:
        return f"Priority({self.name!r})"


# ---------------------------------------------------------------------------
# Exercise 3: Virtual subclass registration
# ---------------------------------------------------------------------------

class Printable(ABC):
    """ABC with __subclasshook__: any class with print_me() qualifies."""

    @abstractmethod
    def print_me(self) -> str:
        ...

    @classmethod
    def __subclasshook__(cls, C: type) -> bool:
        if cls is Printable:
            if any("print_me" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented  # type: ignore[return-value]


class LegacyPrinter:
    """Old class — has print_me() but doesn't inherit from Printable."""
    def print_me(self) -> str:
        return "Legacy output"


class ManuallyRegistered:
    """Explicitly registered as virtual subclass."""
    def print_me(self) -> str:
        return "Manually registered"


# Explicit virtual subclass registration
Printable.register(ManuallyRegistered)  # type: ignore[arg-type]


if __name__ == "__main__":
    shapes: list[Drawable] = [SVGCircle(5.0), SVGRect(3.0, 4.0)]
    for s in shapes:
        print(f"{s.draw()} area={s.area():.2f}")
    print(isinstance(SVGCircle(1.0), Drawable))  # True

    temps = [Temperature(100), Temperature(-10), Temperature(37)]
    print(sorted(temps))

    printer = LegacyPrinter()
    print(isinstance(printer, Printable))  # True via __subclasshook__

    manual = ManuallyRegistered()
    print(isinstance(manual, Printable))   # True via register()
