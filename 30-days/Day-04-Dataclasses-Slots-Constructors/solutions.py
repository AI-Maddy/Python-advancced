"""
Day 04 — Solutions
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import ClassVar, NamedTuple


# ---------------------------------------------------------------------------
# Exercise 1: Point3D dataclass
# ---------------------------------------------------------------------------

@dataclass
class Point3D:
    """3D point with distance and midpoint methods."""
    x: float
    y: float
    z: float

    def distance_to(self, other: "Point3D") -> float:
        return math.sqrt(
            (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2
        )

    def midpoint(self, other: "Point3D") -> "Point3D":
        return Point3D(
            (self.x + other.x) / 2,
            (self.y + other.y) / 2,
            (self.z + other.z) / 2,
        )

    @classmethod
    def origin(cls) -> "Point3D":
        return cls(0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# Exercise 2: ImmutableConfig frozen dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ImmutableConfig:
    """Application configuration — immutable after creation."""
    host: str
    port: int
    debug: bool = False
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not (1 <= self.port <= 65535):
            raise ValueError(f"Invalid port: {self.port}")

    @classmethod
    def development(cls) -> "ImmutableConfig":
        return cls(host="localhost", port=8000, debug=True)

    @classmethod
    def production(cls, host: str, port: int = 443) -> "ImmutableConfig":
        return cls(host=host, port=port, debug=False)


# ---------------------------------------------------------------------------
# Exercise 3: DateRange with classmethods
# ---------------------------------------------------------------------------

@dataclass
class DateRange:
    """Date range with validation and classmethods."""
    start: str
    end: str

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError(f"start must be <= end, got {self.start} > {self.end}")

    @classmethod
    def single_day(cls, date: str) -> "DateRange":
        return cls(date, date)

    @classmethod
    def year(cls, year: int) -> "DateRange":
        return cls(f"{year}-01-01", f"{year}-12-31")

    @property
    def days(self) -> int:
        from datetime import date
        d1 = date.fromisoformat(self.start)
        d2 = date.fromisoformat(self.end)
        return (d2 - d1).days + 1

    def contains(self, date_str: str) -> bool:
        return self.start <= date_str <= self.end

    def overlaps(self, other: "DateRange") -> bool:
        return self.start <= other.end and other.start <= self.end


# ---------------------------------------------------------------------------
# Exercise 4: NamedTuple Card
# ---------------------------------------------------------------------------

class Card(NamedTuple):
    """Playing card as a NamedTuple."""
    rank: str   # "A", "2"-"10", "J", "Q", "K"
    suit: str   # "♠", "♥", "♦", "♣"

    RANKS: ClassVar[list[str]] = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    SUITS: ClassVar[list[str]] = ["♠","♥","♦","♣"]

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    @property
    def value(self) -> int:
        """Blackjack value."""
        if self.rank in ("J", "Q", "K"):
            return 10
        if self.rank == "A":
            return 11
        return int(self.rank)


if __name__ == "__main__":
    p1 = Point3D(0.0, 0.0, 0.0)
    p2 = Point3D(1.0, 2.0, 2.0)
    print(p1.distance_to(p2))     # 3.0
    print(p1.midpoint(p2))

    dev = ImmutableConfig.development()
    prod = ImmutableConfig.production("example.com")
    print(dev, prod)
    print({dev, prod})  # set — uses __hash__

    dr = DateRange.year(2024)
    print(dr.contains("2024-06-15"))
    print(dr.overlaps(DateRange("2024-12-01", "2025-01-31")))

    ace_spades = Card("A", "♠")
    print(ace_spades, ace_spades.value)
