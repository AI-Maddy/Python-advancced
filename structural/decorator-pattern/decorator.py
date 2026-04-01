"""
Structural Decorator Pattern (GoF).

Uses composition to extend objects at runtime without modifying their class.
Coffee example: MilkDecorator, SugarDecorator, VanillaDecorator all wrap a
Beverage and add to its cost and description.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Component interface
# ---------------------------------------------------------------------------
class Beverage(ABC):
    """Abstract component — any coffee drink."""

    @abstractmethod
    def description(self) -> str:
        """Return a human-readable description of the drink."""

    @abstractmethod
    def cost(self) -> float:
        """Return the price in USD."""


# ---------------------------------------------------------------------------
# Concrete component
# ---------------------------------------------------------------------------
class Espresso(Beverage):
    """Base espresso: no extras."""

    def description(self) -> str:
        return "Espresso"

    def cost(self) -> float:
        return 1.99


class HouseBlend(Beverage):
    """Standard drip coffee."""

    def description(self) -> str:
        return "House Blend"

    def cost(self) -> float:
        return 0.89


# ---------------------------------------------------------------------------
# Abstract decorator
# ---------------------------------------------------------------------------
class CondimentDecorator(Beverage, ABC):
    """Abstract decorator — wraps a Beverage and delegates to it."""

    def __init__(self, beverage: Beverage) -> None:
        self._beverage = beverage

    @property
    def beverage(self) -> Beverage:
        return self._beverage


# ---------------------------------------------------------------------------
# Concrete decorators
# ---------------------------------------------------------------------------
class MilkDecorator(CondimentDecorator):
    """Adds steamed milk (+$0.25)."""

    def description(self) -> str:
        return self._beverage.description() + ", Milk"

    def cost(self) -> float:
        return self._beverage.cost() + 0.25


class SugarDecorator(CondimentDecorator):
    """Adds sugar (+$0.10)."""

    def description(self) -> str:
        return self._beverage.description() + ", Sugar"

    def cost(self) -> float:
        return self._beverage.cost() + 0.10


class VanillaDecorator(CondimentDecorator):
    """Adds vanilla syrup (+$0.50)."""

    def description(self) -> str:
        return self._beverage.description() + ", Vanilla"

    def cost(self) -> float:
        return self._beverage.cost() + 0.50


class DoubleShotDecorator(CondimentDecorator):
    """Doubles the shot count (+$0.80)."""

    def description(self) -> str:
        return self._beverage.description() + ", Double Shot"

    def cost(self) -> float:
        return self._beverage.cost() + 0.80


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Espresso with milk + double shot
    drink: Beverage = Espresso()
    drink = MilkDecorator(drink)
    drink = DoubleShotDecorator(drink)
    print(f"{drink.description()} = ${drink.cost():.2f}")

    # House blend with sugar, milk, vanilla
    drink2: Beverage = HouseBlend()
    drink2 = SugarDecorator(drink2)
    drink2 = MilkDecorator(drink2)
    drink2 = VanillaDecorator(drink2)
    print(f"{drink2.description()} = ${drink2.cost():.2f}")
