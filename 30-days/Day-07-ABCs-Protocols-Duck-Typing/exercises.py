"""
Day 07 — Exercises: ABCs, Protocols, and Duck Typing
"""
from __future__ import annotations

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
    def draw(self) -> str: pass  # TODO
    def area(self) -> float: pass  # TODO

class SVGRect:
    def __init__(self, w: float, h: float) -> None: self.w = w; self.h = h
    def draw(self) -> str: pass  # TODO
    def area(self) -> float: pass  # TODO

def render_all(drawables: list[Drawable]) -> list[str]:
    pass  # TODO


# Exercise 2: Sortable ABC with sort_key()
# Temperature and Priority implement it

class Sortable(ABC):
    @abstractmethod
    def sort_key(self) -> float: ...
    # TODO: __lt__, __le__, __gt__, __eq__, __hash__

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
        # TODO: return True if C has print_me in its MRO
        return NotImplemented  # type: ignore[return-value]

class LegacyPrinter:
    def print_me(self) -> str: return "Legacy"

if __name__ == "__main__":
    print(isinstance(SVGCircle(1.0), Drawable))
