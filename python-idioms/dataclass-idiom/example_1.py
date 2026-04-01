"""
Example 1 — Frozen dataclass as a value object in a domain model.
"""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int   # integer cents
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError(f"amount cannot be negative: {self.amount}")
        if len(self.currency) != 3:
            raise ValueError(f"currency must be 3-letter ISO code: {self.currency!r}")

    def __add__(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return dataclasses.replace(self, amount=self.amount + other.amount)

    def __str__(self) -> str:
        return f"{self.currency} {self.amount / 100:.2f}"


def main() -> None:
    price = Money(1999, "USD")
    tax = Money(160, "USD")
    total = price + tax
    print(f"Price: {price}")
    print(f"Tax:   {tax}")
    print(f"Total: {total}")

    # Frozen: mutations raise FrozenInstanceError
    import pytest
    try:
        price.amount = 0  # type: ignore[misc]
    except dataclasses.FrozenInstanceError as e:
        print(f"Immutable: {type(e).__name__}")

    # Hashable (frozen dataclasses are hashable)
    basket: set[Money] = {price, tax, price}
    print(f"Unique items in basket: {len(basket)}")  # 2

    # Negative amount raises
    try:
        Money(-1)
    except ValueError as e:
        print(f"Validation: {e}")


if __name__ == "__main__":
    main()
