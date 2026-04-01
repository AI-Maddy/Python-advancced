"""pytest tests for builder pattern."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from builder import (
    ConcreteHouseBuilder,
    Director,
    House,
    WoodenHouseBuilder,
)


class TestWoodenHouseBuilder:
    def test_minimal_house_has_walls_and_roof(self) -> None:
        director = Director(WoodenHouseBuilder())
        house = director.build_minimal_viable_house()
        assert house.walls != "none"
        assert house.roof != "none"

    def test_minimal_house_has_no_garden(self) -> None:
        director = Director(WoodenHouseBuilder())
        house = director.build_minimal_viable_house()
        assert house.garden == "none"

    def test_full_house_has_all_features(self) -> None:
        director = Director(WoodenHouseBuilder())
        house = director.build_full_featured_house()
        assert house.walls != "none"
        assert house.roof != "none"
        assert house.garden != "none"
        assert house.garage is True

    def test_sequential_builds_are_independent(self) -> None:
        director = Director(WoodenHouseBuilder())
        h1 = director.build_minimal_viable_house()
        h2 = director.build_full_featured_house()
        assert h1 is not h2

    def test_get_result_returns_house(self) -> None:
        builder = WoodenHouseBuilder()
        builder.build_walls().build_roof()
        result = builder.get_result()
        assert isinstance(result, House)


class TestConcreteHouseBuilder:
    def test_has_two_floors(self) -> None:
        director = Director(ConcreteHouseBuilder())
        house = director.build_minimal_viable_house()
        assert house.floors == 2

    def test_optional_pool(self) -> None:
        builder = ConcreteHouseBuilder()
        house = (
            builder
            .build_walls()
            .build_roof()
            .build_swimming_pool()
            .get_result()
        )
        assert house.swimming_pool is True

    def test_optional_steps_skipped_cleanly(self) -> None:
        builder = ConcreteHouseBuilder()
        house = builder.build_walls().build_roof().get_result()
        assert house.swimming_pool is False
        assert house.garage is False

    def test_reset_clears_state(self) -> None:
        builder = ConcreteHouseBuilder()
        builder.build_walls()
        builder.reset()
        house = builder.get_result()
        assert house.walls == "none"


class TestDirector:
    def test_switch_builder(self) -> None:
        director = Director(WoodenHouseBuilder())
        h1 = director.build_full_featured_house()
        director.builder = ConcreteHouseBuilder()
        h2 = director.build_full_featured_house()
        assert h1.walls != h2.walls   # different materials

    def test_product_is_dataclass(self) -> None:
        import dataclasses

        director = Director(WoodenHouseBuilder())
        house = director.build_minimal_viable_house()
        assert dataclasses.is_dataclass(house)
