"""
Example 1 — Validated model fields (like a mini ORM).
"""
from __future__ import annotations

from descriptor import Clamped, TypeChecked, Validated


class Product:
    name: str = TypeChecked(str)  # type: ignore[assignment]
    price: float = Validated(  # type: ignore[assignment]
        lambda v: isinstance(v, (int, float)) and v > 0,
        "price must be positive",
    )
    stock: int = Clamped(0, 10_000)  # type: ignore[assignment]

    def __init__(self, name: str, price: float, stock: int) -> None:
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self) -> str:
        return f"Product({self.name!r}, ${self.price:.2f}, stock={self.stock})"


def main() -> None:
    import traceback

    p = Product("Widget", 9.99, 50)
    print(p)

    # Type check
    try:
        p.name = 123  # type: ignore[assignment]
    except TypeError as e:
        print(f"TypeError: {e}")

    # Validation
    try:
        p.price = -5.0
    except ValueError as e:
        print(f"ValueError: {e}")

    # Clamping (no error, just clamps)
    p.stock = 99_999
    print(f"Stock after over-assignment: {p.stock}")  # 10000

    p.stock = -100
    print(f"Stock after under-assignment: {p.stock}")  # 0


if __name__ == "__main__":
    main()
