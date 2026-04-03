"""
Day 07 — Exercises: ABCs, Protocols, and Duck Typing
"""
from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


# Exercise 1: Drawable Protocol (runtime_checkable)
# - draw() -> str
# - area() -> float
# SVGCircle and SVGRect satisfy it structurally (no inheritance)
# render_all(drawables) returns list of draw() strings

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...
    def area(self) -> float: ...

class SVGCircle:
    def __init__(self, r: float) -> None: self.r = r
    def draw(self) -> str:
        return f"<circle r='{self.r}'/>"
    def area(self) -> float:
        return math.pi * self.r ** 2

class SVGRect:
    def __init__(self, w: float, h: float) -> None: self.w = w; self.h = h
    def draw(self) -> str:
        return f"<rect width='{self.w}' height='{self.h}'/>"
    def area(self) -> float:
        return self.w * self.h

def render_all(drawables: list[Drawable]) -> list[str]:
    return [d.draw() for d in drawables]


# Exercise 2: Sortable ABC with sort_key()
# Temperature and Priority implement it

class Sortable(ABC):
    @abstractmethod
    def sort_key(self) -> float: ...
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
    def __init__(self, celsius: float) -> None: self.celsius = celsius
    def sort_key(self) -> float: return self.celsius

class Priority(Sortable):
    LEVELS = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    def __init__(self, name: str) -> None: self.name = name
    def sort_key(self) -> float: return float(self.LEVELS.get(self.name, 0))


# Exercise 3: Virtual subclass with __subclasshook__
class Printable(ABC):
    @abstractmethod
    def print_me(self) -> str: ...

    @classmethod
    def __subclasshook__(cls, C: type) -> bool:
        if cls is Printable:
            if any("print_me" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented  # type: ignore[return-value]

class LegacyPrinter:
    def print_me(self) -> str: return "Legacy"

if __name__ == "__main__":
    print(isinstance(SVGCircle(1.0), Drawable))
