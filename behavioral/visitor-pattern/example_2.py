"""Visitor Pattern — Example 2: Tax Calculator.

Different product types (FoodItem, ElectronicsItem, LuxuryItem) have
different tax rates.  A TaxVisitor computes tax without modifying the items.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class TaxVisitor(ABC):
    @abstractmethod
    def visit_food(self, item: FoodItem) -> float: ...
    @abstractmethod
    def visit_electronics(self, item: ElectronicsItem) -> float: ...
    @abstractmethod
    def visit_luxury(self, item: LuxuryItem) -> float: ...


class ProductItem(ABC):
    @abstractmethod
    def accept(self, visitor: TaxVisitor) -> float: ...


@dataclass
class FoodItem(ProductItem):
    name: str
    price: float

    def accept(self, visitor: TaxVisitor) -> float:
        return visitor.visit_food(self)


@dataclass
class ElectronicsItem(ProductItem):
    name: str
    price: float

    def accept(self, visitor: TaxVisitor) -> float:
        return visitor.visit_electronics(self)


@dataclass
class LuxuryItem(ProductItem):
    name: str
    price: float

    def accept(self, visitor: TaxVisitor) -> float:
        return visitor.visit_luxury(self)


class StandardTaxVisitor(TaxVisitor):
    """Standard tax rates: food 5%, electronics 15%, luxury 25%."""

    def visit_food(self, item: FoodItem) -> float:
        tax = item.price * 0.05
        print(f"  {item.name}: ${item.price:.2f} + ${tax:.2f} food tax")
        return tax

    def visit_electronics(self, item: ElectronicsItem) -> float:
        tax = item.price * 0.15
        print(f"  {item.name}: ${item.price:.2f} + ${tax:.2f} electronics tax")
        return tax

    def visit_luxury(self, item: LuxuryItem) -> float:
        tax = item.price * 0.25
        print(f"  {item.name}: ${item.price:.2f} + ${tax:.2f} luxury tax")
        return tax


def main() -> None:
    cart: list[ProductItem] = [
        FoodItem("Organic Apples", 4.99),
        ElectronicsItem("USB Hub", 29.99),
        LuxuryItem("Gold Watch", 1299.00),
        FoodItem("Artisan Bread", 6.50),
    ]

    tax_calc = StandardTaxVisitor()
    total_tax = sum(item.accept(tax_calc) for item in cart)
    subtotal = sum(i.price for i in cart)  # type: ignore[union-attr]
    print(f"\nSubtotal: ${subtotal:.2f}")
    print(f"Tax:      ${total_tax:.2f}")
    print(f"Total:    ${subtotal + total_tax:.2f}")


if __name__ == "__main__":
    main()
