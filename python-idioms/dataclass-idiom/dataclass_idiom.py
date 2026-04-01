"""
Dataclass Idiom — Python's "rule of zero".

Demonstrates:
* @dataclass — auto __init__, __repr__, __eq__
* @dataclass(frozen=True) — immutable value objects
* @dataclass(slots=True) — memory-efficient (Python 3.10+)
* field(default_factory=...) and __post_init__
* InitVar for init-only parameters
* dataclasses.asdict, dataclasses.replace
* NamedTuple comparison
"""
from __future__ import annotations

import dataclasses
from dataclasses import InitVar, dataclass, field
from typing import NamedTuple


# ---------------------------------------------------------------------------
# Basic dataclass
# ---------------------------------------------------------------------------
@dataclass
class Point:
    """Mutable 2-D point."""

    x: float
    y: float

    def distance_to(self, other: Point) -> float:
        import math
        return math.hypot(self.x - other.x, self.y - other.y)


# ---------------------------------------------------------------------------
# Frozen (immutable) dataclass
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class RGB:
    """Immutable colour value object.

    Raises:
        ValueError: if any channel is outside [0, 255].
    """

    r: int
    g: int
    b: int

    def __post_init__(self) -> None:
        for ch, val in (("r", self.r), ("g", self.g), ("b", self.b)):
            if not 0 <= val <= 255:
                raise ValueError(f"Channel {ch!r} must be 0–255, got {val}")

    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"


# ---------------------------------------------------------------------------
# Dataclass with slots=True (Python 3.10+)
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class Vector3:
    """Memory-efficient 3-D vector (no __dict__)."""

    x: float
    y: float
    z: float

    def magnitude(self) -> float:
        import math
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


# ---------------------------------------------------------------------------
# Dataclass with default_factory and __post_init__ + InitVar
# ---------------------------------------------------------------------------
@dataclass
class Team:
    """A named team with optional member list.

    Args:
        name: Team name.
        members: Initial members (default empty list).
        max_size: Maximum allowed members (InitVar — used only during init).
    """

    name: str
    members: list[str] = field(default_factory=list)
    _max_size: int = field(init=False, repr=False, default=100)
    max_size: InitVar[int] = 100

    def __post_init__(self, max_size: int) -> None:
        self._max_size = max_size
        if len(self.members) > max_size:
            raise ValueError(f"Too many members: {len(self.members)} > {max_size}")

    def add_member(self, name: str) -> None:
        if len(self.members) >= self._max_size:
            raise ValueError("Team is full")
        self.members.append(name)


# ---------------------------------------------------------------------------
# NamedTuple (comparison)
# ---------------------------------------------------------------------------
class Coordinate(NamedTuple):
    """Immutable coordinate using NamedTuple (lightweight alternative)."""

    latitude: float
    longitude: float

    def label(self) -> str:
        ns = "N" if self.latitude >= 0 else "S"
        ew = "E" if self.longitude >= 0 else "W"
        return f"{abs(self.latitude):.4f}°{ns}, {abs(self.longitude):.4f}°{ew}"


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Basic
    p1 = Point(0.0, 0.0)
    p2 = Point(3.0, 4.0)
    print(f"Distance: {p1.distance_to(p2)}")  # 5.0

    # Frozen
    red = RGB(255, 0, 0)
    print(f"Red: {red.to_hex()}")
    print(f"Frozen equal: {RGB(255, 0, 0) == red}")
    try:
        RGB(256, 0, 0)  # raises
    except ValueError as e:
        print(f"Validation: {e}")

    # asdict / replace
    red_dict = dataclasses.asdict(red)
    print(f"asdict: {red_dict}")
    pink = dataclasses.replace(red, b=128)
    print(f"replace: {pink.to_hex()}")

    # Slots
    v = Vector3(1.0, 2.0, 3.0)
    print(f"Vector magnitude: {v.magnitude():.4f}")
    print(f"Has __dict__: {hasattr(v, '__dict__')}")  # False

    # Team with InitVar
    team = Team("Avengers", ["Iron Man", "Thor"], max_size=5)
    team.add_member("Hulk")
    print(f"Team: {team}")

    # NamedTuple
    loc = Coordinate(51.5074, -0.1278)
    print(f"Location: {loc.label()}")
