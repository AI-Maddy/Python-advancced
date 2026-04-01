"""
Day 04 — Exercises: Dataclasses, Slots, and Constructors
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, NamedTuple


# Exercise 1: Point3D dataclass with distance_to, midpoint, and origin classmethod
@dataclass
class Point3D:
    x: float
    y: float
    z: float

    def distance_to(self, other: "Point3D") -> float:
        # TODO
        pass

    def midpoint(self, other: "Point3D") -> "Point3D":
        # TODO
        pass

    @classmethod
    def origin(cls) -> "Point3D":
        # TODO
        pass


# Exercise 2: ImmutableConfig — frozen dataclass
# Fields: host, port, debug=False, tags: tuple[str,...]=()
# __post_init__: validate port in 1..65535
# classmethods: development(), production(host, port=443)

@dataclass(frozen=True)
class ImmutableConfig:
    # TODO
    pass


# Exercise 3: DateRange with classmethods single_day, year
# contains(date_str) -> bool
# overlaps(other) -> bool

@dataclass
class DateRange:
    start: str
    end: str
    # TODO: __post_init__, classmethods, properties, contains, overlaps


# Exercise 4: Card NamedTuple with value property
class Card(NamedTuple):
    rank: str
    suit: str
    # TODO: value property, __str__


if __name__ == "__main__":
    p = Point3D(1.0, 2.0, 3.0)
    print(p)
