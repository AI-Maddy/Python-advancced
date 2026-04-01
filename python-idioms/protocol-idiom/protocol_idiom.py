"""
Protocol Idiom — structural subtyping (duck typing with static checks).

typing.Protocol lets us define interfaces that classes satisfy implicitly —
no inheritance required.  Equivalent to C++ concepts / type erasure.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# 1. Drawable protocol
# ---------------------------------------------------------------------------
@runtime_checkable
class Drawable(Protocol):
    """Any object that can draw itself."""

    def draw(self) -> str:
        """Return a string representation of the drawn object."""
        ...


# ---------------------------------------------------------------------------
# 2. Serializable protocol
# ---------------------------------------------------------------------------
@runtime_checkable
class Serializable(Protocol):
    """Any object that can serialise/deserialise itself."""

    def to_dict(self) -> dict:
        """Serialise to a plain dictionary."""
        ...

    @classmethod
    def from_dict(cls, data: dict) -> Serializable:
        """Deserialise from a plain dictionary."""
        ...


# ---------------------------------------------------------------------------
# 3. Comparable protocol
# ---------------------------------------------------------------------------
@runtime_checkable
class Comparable(Protocol):
    """Structural protocol for objects that support < ordering."""

    def __lt__(self, other: object) -> bool: ...
    def __eq__(self, other: object) -> bool: ...


# ---------------------------------------------------------------------------
# Conforming classes — NO inheritance from the protocols
# ---------------------------------------------------------------------------
class Circle:
    """Satisfies Drawable without inheriting from it."""

    def __init__(self, radius: float) -> None:
        self.radius = radius

    def draw(self) -> str:
        return f"○ Circle(r={self.radius})"


class Square:
    """Satisfies Drawable without inheriting from it."""

    def __init__(self, side: float) -> None:
        self.side = side

    def draw(self) -> str:
        return f"□ Square(s={self.side})"


class Temperature:
    """Satisfies both Serializable and Comparable."""

    def __init__(self, celsius: float) -> None:
        self.celsius = celsius

    def to_dict(self) -> dict:
        return {"celsius": self.celsius}

    @classmethod
    def from_dict(cls, data: dict) -> Temperature:
        return cls(data["celsius"])

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Temperature):
            return self.celsius < other.celsius
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Temperature):
            return self.celsius == other.celsius
        return NotImplemented

    def __repr__(self) -> str:
        return f"Temperature({self.celsius}°C)"


# ---------------------------------------------------------------------------
# Functions typed against protocols
# ---------------------------------------------------------------------------
def render_all(items: list[Drawable]) -> list[str]:
    """Render any sequence of drawable objects."""
    return [item.draw() for item in items]


def save_all(items: list[Serializable]) -> list[dict]:
    """Serialise any sequence of serializable objects."""
    return [item.to_dict() for item in items]


def find_min(items: list[Comparable]) -> Comparable:
    """Return the smallest item (works for any Comparable)."""
    return min(items)  # type: ignore[type-var]


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    shapes: list[Drawable] = [Circle(5), Square(3), Circle(1)]
    print("Rendered:", render_all(shapes))

    # runtime_checkable isinstance checks
    print(f"Circle is Drawable? {isinstance(Circle(1), Drawable)}")
    print(f"int is Drawable? {isinstance(42, Drawable)}")

    temps = [Temperature(100), Temperature(-10), Temperature(37)]
    print(f"Min temperature: {find_min(temps)}")  # type: ignore[arg-type]

    d = temps[0].to_dict()
    t2 = Temperature.from_dict(d)
    print(f"Round-trip: {t2}")

    # Duck typing: any object with .draw() works
    class Star:
        def draw(self) -> str:
            return "★ Star"

    all_drawables: list[Drawable] = [Circle(2), Star()]  # type: ignore[list-item]
    print("Mixed:", render_all(all_drawables))
