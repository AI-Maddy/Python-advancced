"""
Prototype Pattern.

Objects implement ``clone()`` to return a deep copy of themselves.
A ``ShapeRegistry`` maps names to prototype instances so clients can
clone named shapes without knowing concrete types.
"""
from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from typing import Self


# ---------------------------------------------------------------------------
# Prototype ABC
# ---------------------------------------------------------------------------
class Prototype(ABC):
    """Any object that can clone itself."""

    @abstractmethod
    def clone(self) -> Self:
        """Return a deep copy of this object."""


# ---------------------------------------------------------------------------
# Concrete prototypes
# ---------------------------------------------------------------------------
class Circle(Prototype):
    """A circle with mutable fill color and radius.

    Args:
        radius: Circle radius in pixels.
        color: Fill colour (e.g. ``'red'``).
    """

    def __init__(self, radius: float, color: str = "black") -> None:
        self.radius = radius
        self.color = color
        self.tags: list[str] = []

    def clone(self) -> Circle:
        return copy.deepcopy(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius and self.color == other.color

    def __repr__(self) -> str:
        return f"Circle(r={self.radius}, color={self.color!r}, tags={self.tags})"


class Rectangle(Prototype):
    """A rectangle prototype.

    Args:
        width: Width in pixels.
        height: Height in pixels.
        color: Fill colour.
    """

    def __init__(self, width: float, height: float, color: str = "black") -> None:
        self.width = width
        self.height = height
        self.color = color
        self.children: list[Prototype] = []

    def clone(self) -> Rectangle:
        return copy.deepcopy(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rectangle):
            return NotImplemented
        return (
            self.width == other.width
            and self.height == other.height
            and self.color == other.color
        )

    def __repr__(self) -> str:
        return (
            f"Rectangle(w={self.width}, h={self.height}, "
            f"color={self.color!r}, children={len(self.children)})"
        )


# ---------------------------------------------------------------------------
# Shape registry
# ---------------------------------------------------------------------------
class ShapeRegistry:
    """Maps symbolic names to prototype instances.

    Usage::

        registry = ShapeRegistry()
        registry.register("big-red-circle", Circle(100, "red"))
        my_circle = registry.clone("big-red-circle")
    """

    def __init__(self) -> None:
        self._prototypes: dict[str, Prototype] = {}

    def register(self, name: str, prototype: Prototype) -> None:
        """Register a prototype under ``name``."""
        self._prototypes[name] = prototype

    def clone(self, name: str) -> Prototype:
        """Clone the prototype registered under ``name``.

        Raises:
            KeyError: If name is not registered.
        """
        return self._prototypes[name].clone()

    def keys(self) -> list[str]:
        return list(self._prototypes.keys())


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    registry = ShapeRegistry()
    registry.register("small-blue-circle", Circle(10, "blue"))
    registry.register("large-red-rect", Rectangle(200, 100, "red"))

    c1 = registry.clone("small-blue-circle")
    c2 = registry.clone("small-blue-circle")
    print(f"c1 == c2: {c1 == c2}")   # True (equal)
    print(f"c1 is c2: {c1 is c2}")   # False (different objects)

    # Mutating clone does not affect prototype
    assert isinstance(c1, Circle)
    c1.color = "green"
    c1.tags.append("modified")
    c3 = registry.clone("small-blue-circle")
    assert isinstance(c3, Circle)
    print(f"prototype color still blue: {c3.color == 'blue'}")  # True
    print(f"prototype tags empty: {c3.tags}")  # []

    # Nested deep copy
    rect = registry.clone("large-red-rect")
    assert isinstance(rect, Rectangle)
    rect.children.append(Circle(5))
    rect2 = rect.clone()
    assert isinstance(rect2, Rectangle)
    rect2.children.clear()
    print(f"original children count: {len(rect.children)}")  # 1
