"""pytest tests for structural decorator pattern."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from decorator import (
    Beverage,
    DoubleShotDecorator,
    Espresso,
    HouseBlend,
    MilkDecorator,
    SugarDecorator,
    VanillaDecorator,
)


class TestEspresso:
    def test_base_cost(self) -> None:
        assert Espresso().cost() == pytest.approx(1.99)

    def test_base_description(self) -> None:
        assert Espresso().description() == "Espresso"


class TestMilkDecorator:
    def test_cost_accumulates(self) -> None:
        drink = MilkDecorator(Espresso())
        assert drink.cost() == pytest.approx(1.99 + 0.25)

    def test_description_appends(self) -> None:
        drink = MilkDecorator(Espresso())
        assert "Milk" in drink.description()
        assert "Espresso" in drink.description()


class TestSugarDecorator:
    def test_cost_accumulates(self) -> None:
        drink = SugarDecorator(Espresso())
        assert drink.cost() == pytest.approx(1.99 + 0.10)

    def test_description_appends(self) -> None:
        drink = SugarDecorator(HouseBlend())
        assert "Sugar" in drink.description()


class TestVanillaDecorator:
    def test_cost_accumulates(self) -> None:
        drink = VanillaDecorator(Espresso())
        assert drink.cost() == pytest.approx(1.99 + 0.50)


class TestStackedDecorators:
    def test_three_layer_cost(self) -> None:
        drink: Beverage = Espresso()
        drink = MilkDecorator(drink)
        drink = SugarDecorator(drink)
        drink = VanillaDecorator(drink)
        expected = 1.99 + 0.25 + 0.10 + 0.50
        assert drink.cost() == pytest.approx(expected)

    def test_three_layer_description(self) -> None:
        drink: Beverage = Espresso()
        drink = MilkDecorator(drink)
        drink = SugarDecorator(drink)
        drink = VanillaDecorator(drink)
        desc = drink.description()
        assert "Espresso" in desc
        assert "Milk" in desc
        assert "Sugar" in desc
        assert "Vanilla" in desc

    def test_double_milk_stacks(self) -> None:
        drink: Beverage = HouseBlend()
        drink = MilkDecorator(drink)
        drink = MilkDecorator(drink)
        assert drink.cost() == pytest.approx(0.89 + 0.25 + 0.25)

    def test_is_beverage(self) -> None:
        drink: Beverage = MilkDecorator(Espresso())
        assert isinstance(drink, Beverage)

    def test_order_of_wrapping_does_not_change_cost(self) -> None:
        base = Espresso()
        order1: Beverage = VanillaDecorator(MilkDecorator(base))
        base2 = Espresso()
        order2: Beverage = MilkDecorator(VanillaDecorator(base2))
        assert order1.cost() == pytest.approx(order2.cost())
