"""
Day 04 — Dataclasses, Slots, and Constructors
===============================================

Topics:
  - @dataclass auto-generates __init__, __repr__, __eq__
  - field() with default_factory, metadata
  - @dataclass(frozen=True) — immutable, usable as dict key
  - @dataclass(slots=True) — memory optimization (Python 3.10+)
  - __post_init__ for validation
  - NamedTuple as alternative
  - @classmethod factories (named constructors)
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, fields, asdict, astuple
from typing import ClassVar, NamedTuple


# ---------------------------------------------------------------------------
# 1. Basic @dataclass
# ---------------------------------------------------------------------------
# @dataclass automatically generates __init__, __repr__, __eq__
# from the annotated class-level attributes.
# C++ equivalent: a struct with constructor, operator==, and to_string().

@dataclass
class Point2D:
    """2D point — simple dataclass."""
    x: float
    y: float

    def distance_to(self, other: "Point2D") -> float:
        """Euclidean distance."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


def demo_basic_dataclass() -> None:
    p1 = Point2D(1.0, 2.0)
    p2 = Point2D(4.0, 6.0)
    print(p1)               # Point2D(x=1.0, y=2.0)
    print(p1 == p2)         # False
    print(p1 == Point2D(1.0, 2.0))  # True
    print(p1.distance_to(p2))       # 5.0


# ---------------------------------------------------------------------------
# 2. field() — Custom Field Definitions
# ---------------------------------------------------------------------------

@dataclass
class Student:
    """Student with varied field configurations."""
    name: str
    grade: float = 0.0                              # field with default
    courses: list[str] = field(default_factory=list)  # mutable default!
    _internal_id: int = field(default=0, repr=False, compare=False)

    # Class variable — NOT a dataclass field
    school: ClassVar[str] = "Python Academy"

    def enroll(self, course: str) -> None:
        self.courses.append(course)

    def __post_init__(self) -> None:
        """Validation runs after __init__. Use for invariant checking."""
        if not self.name:
            raise ValueError("name cannot be empty")
        if not (0.0 <= self.grade <= 100.0):
            raise ValueError(f"grade must be 0-100, got {self.grade}")


def demo_field() -> None:
    s1 = Student("Alice", grade=85.0)
    s2 = Student("Bob")
    s1.enroll("Python")
    s1.enroll("Algorithms")
    print(s1)
    print(s2)                  # courses is [] — not shared!
    print(Student.school)      # Python Academy

    # asdict/astuple conversion
    d = asdict(s1)
    print(d)


# ---------------------------------------------------------------------------
# 3. @dataclass(frozen=True) — Immutable Dataclass
# ---------------------------------------------------------------------------
# frozen=True: generates __hash__, prevents attribute assignment.
# Can be used as a dict key or set element.
# C++ equivalent: a class with all const members.

@dataclass(frozen=True)
class Vector3D:
    """Immutable 3D vector."""
    x: float
    y: float
    z: float

    def __add__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar: float) -> "Vector3D":
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)


def demo_frozen() -> None:
    v1 = Vector3D(1.0, 2.0, 3.0)
    v2 = Vector3D(4.0, 5.0, 6.0)
    print(v1 + v2)            # Vector3D(x=5.0, y=7.0, z=9.0)
    print(v1 * 2)             # Vector3D(x=2.0, y=4.0, z=6.0)

    # Usable as dict key (frozen → has __hash__)
    cache: dict[Vector3D, float] = {v1: v1.magnitude}
    print(cache[Vector3D(1.0, 2.0, 3.0)])   # 3.741...

    # Mutation attempt raises FrozenInstanceError
    try:
        v1.x = 99.0  # type: ignore[misc]
    except Exception as e:
        print(f"Caught: {e}")


# ---------------------------------------------------------------------------
# 4. @dataclass(slots=True) — Memory Optimization (Python 3.10+)
# ---------------------------------------------------------------------------
# slots=True adds __slots__ automatically.
# Benefits: ~30% less memory per instance, faster attribute access,
#           prevents accidental new attributes.

@dataclass(slots=True)
class Particle:
    """Particle optimised with __slots__."""
    x: float
    y: float
    z: float
    mass: float
    charge: float = 0.0


def demo_slots() -> None:
    import sys
    p = Particle(1.0, 2.0, 3.0, 9.11e-31)
    print(p)
    print(f"Size: {sys.getsizeof(p)} bytes")

    # Cannot add new attributes to slotted class
    try:
        p.velocity = 1000.0  # type: ignore[attr-defined]
    except AttributeError as e:
        print(f"Caught: {e}")


# ---------------------------------------------------------------------------
# 5. __post_init__ — Validation and Derived Fields
# ---------------------------------------------------------------------------

@dataclass
class DateRange:
    """A date range with validation in __post_init__."""
    start: str   # ISO format: "YYYY-MM-DD"
    end: str

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError(
                f"start ({self.start}) must be <= end ({self.end})"
            )

    @classmethod
    def single_day(cls, date: str) -> "DateRange":
        """Named constructor: a range of one day."""
        return cls(date, date)

    @classmethod
    def year(cls, year: int) -> "DateRange":
        """Named constructor: an entire year."""
        return cls(f"{year}-01-01", f"{year}-12-31")

    @property
    def days(self) -> int:
        """Approximate days in range (simplified)."""
        from datetime import date
        d1 = date.fromisoformat(self.start)
        d2 = date.fromisoformat(self.end)
        return (d2 - d1).days + 1


# ---------------------------------------------------------------------------
# 6. NamedTuple — Tuple-based alternative to dataclass
# ---------------------------------------------------------------------------
# NamedTuple: immutable, tuple-like, readable field names.
# Smaller memory than dataclass. Use for simple value objects.

class RGB(NamedTuple):
    """Colour as a named tuple."""
    red: int
    green: int
    blue: int

    def to_hex(self) -> str:
        return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"

    @classmethod
    def white(cls) -> "RGB":
        return cls(255, 255, 255)


def demo_named_tuple() -> None:
    red = RGB(255, 0, 0)
    print(red)             # RGB(red=255, green=0, blue=0)
    print(red.to_hex())    # #FF0000
    print(red[0])          # 255 — still indexable like a tuple!
    print(tuple(red))      # (255, 0, 0)

    # Immutable
    try:
        red.red = 128  # type: ignore[misc]
    except AttributeError as e:
        print(f"Caught: {e}")


# ---------------------------------------------------------------------------
# 7. Dataclass Introspection
# ---------------------------------------------------------------------------

def demo_introspection() -> None:
    """Show how to inspect dataclass fields at runtime."""
    p = Point2D(1.0, 2.0)
    for f in fields(p):
        print(f"  {f.name}: {f.type} = {getattr(p, f.name)}")

    # Convert to dict/tuple
    print(asdict(p))      # {'x': 1.0, 'y': 2.0}
    print(astuple(p))     # (1.0, 2.0)


if __name__ == "__main__":
    print("=== Basic Dataclass ===")
    demo_basic_dataclass()
    print("\n=== field() ===")
    demo_field()
    print("\n=== frozen=True ===")
    demo_frozen()
    print("\n=== slots=True ===")
    demo_slots()

    print("\n=== DateRange ===")
    dr = DateRange("2024-01-15", "2024-03-20")
    print(dr, dr.days)
    single = DateRange.single_day("2024-06-15")
    print(single)
    year = DateRange.year(2024)
    print(year, year.days)

    print("\n=== NamedTuple ===")
    demo_named_tuple()

    print("\n=== Introspection ===")
    demo_introspection()
