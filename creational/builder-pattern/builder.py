"""
Builder Pattern.

Separates the construction of a complex ``House`` object from its
representation.  A ``Director`` orchestrates builder steps; clients may
also call builder steps directly for custom builds.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Product (dataclass)
# ---------------------------------------------------------------------------
@dataclass
class House:
    """Fully constructed house product."""

    walls: str = "none"
    roof: str = "none"
    garden: str = "none"
    garage: bool = False
    swimming_pool: bool = False
    floors: int = 1
    windows: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        parts = [
            f"House({self.floors} floor(s))",
            f"  walls={self.walls}",
            f"  roof={self.roof}",
            f"  garden={self.garden}",
            f"  garage={self.garage}",
            f"  pool={self.swimming_pool}",
            f"  windows={self.windows}",
        ]
        return "\n".join(parts)


# ---------------------------------------------------------------------------
# Abstract builder
# ---------------------------------------------------------------------------
class HouseBuilder(ABC):
    """Abstract builder interface."""

    @abstractmethod
    def build_walls(self) -> HouseBuilder: ...

    @abstractmethod
    def build_roof(self) -> HouseBuilder: ...

    @abstractmethod
    def build_garden(self) -> HouseBuilder: ...

    def build_garage(self) -> HouseBuilder:  # optional step
        return self

    def build_swimming_pool(self) -> HouseBuilder:  # optional step
        return self

    @abstractmethod
    def get_result(self) -> House: ...

    def reset(self) -> None:
        """Reset builder state for reuse."""


# ---------------------------------------------------------------------------
# Concrete builders
# ---------------------------------------------------------------------------
class WoodenHouseBuilder(HouseBuilder):
    """Builds a cosy wooden cottage."""

    def __init__(self) -> None:
        self._house = House()

    def build_walls(self) -> WoodenHouseBuilder:
        self._house.walls = "pine timber frame"
        return self

    def build_roof(self) -> WoodenHouseBuilder:
        self._house.roof = "cedar shingles"
        return self

    def build_garden(self) -> WoodenHouseBuilder:
        self._house.garden = "wildflower meadow"
        return self

    def build_garage(self) -> WoodenHouseBuilder:
        self._house.garage = True
        return self

    def get_result(self) -> House:
        result = self._house
        self._house = House()  # reset for next build
        return result

    def reset(self) -> None:
        self._house = House()


class ConcreteHouseBuilder(HouseBuilder):
    """Builds a modern reinforced-concrete house."""

    def __init__(self) -> None:
        self._house = House()

    def build_walls(self) -> ConcreteHouseBuilder:
        self._house.walls = "reinforced concrete"
        self._house.floors = 2
        return self

    def build_roof(self) -> ConcreteHouseBuilder:
        self._house.roof = "flat concrete slab"
        return self

    def build_garden(self) -> ConcreteHouseBuilder:
        self._house.garden = "minimalist zen garden"
        return self

    def build_swimming_pool(self) -> ConcreteHouseBuilder:
        self._house.swimming_pool = True
        return self

    def build_garage(self) -> ConcreteHouseBuilder:
        self._house.garage = True
        return self

    def get_result(self) -> House:
        result = self._house
        self._house = House()
        return result

    def reset(self) -> None:
        self._house = House()


# ---------------------------------------------------------------------------
# Director
# ---------------------------------------------------------------------------
class Director:
    """Knows the standard construction recipes."""

    def __init__(self, builder: HouseBuilder) -> None:
        self._builder = builder

    @property
    def builder(self) -> HouseBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: HouseBuilder) -> None:
        self._builder = builder

    def build_minimal_viable_house(self) -> House:
        """Walls + roof only — no extras."""
        return (
            self._builder
            .build_walls()
            .build_roof()
            .get_result()
        )

    def build_full_featured_house(self) -> House:
        """All standard features."""
        return (
            self._builder
            .build_walls()
            .build_roof()
            .build_garden()
            .build_garage()
            .get_result()
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    director = Director(WoodenHouseBuilder())

    print("=== Minimal wooden house ===")
    print(director.build_minimal_viable_house())

    print("\n=== Full wooden house ===")
    print(director.build_full_featured_house())

    director.builder = ConcreteHouseBuilder()
    print("\n=== Full concrete house ===")
    print(director.build_full_featured_house())

    # Custom build without director
    print("\n=== Custom concrete + pool ===")
    builder = ConcreteHouseBuilder()
    house = (
        builder
        .build_walls()
        .build_roof()
        .build_swimming_pool()
        .get_result()
    )
    print(house)
