"""
Example 1 — Mixin composition for a REST resource.
"""
from __future__ import annotations

import json
from mixin_idiom import LoggingMixin, SerializationMixin, ValidationMixin


class Product(LoggingMixin, ValidationMixin, SerializationMixin):
    def __init__(self, name: str, price: float, sku: str) -> None:
        self.name = name
        self.price = price
        self.sku = sku

    def _rules(self) -> list[tuple[bool, str]]:
        return [
            (bool(self.name), "name is required"),
            (self.price > 0, "price must be positive"),
            (len(self.sku) == 8, "SKU must be 8 characters"),
        ]

    def __repr__(self) -> str:
        return f"Product({self.name!r}, ${self.price:.2f})"


def main() -> None:
    import logging
    logging.basicConfig(level=logging.INFO)

    p = Product("Widget", 9.99, "WDGT0001")
    p.validate()
    p.log("info", "Product validated")
    serialised = p.to_json()
    print("Serialised:", serialised)

    restored = Product.from_json(serialised)
    print("Restored:", restored)

    # Bad product
    try:
        bad = Product("", -1.0, "BAD")
        bad.validate()
    except ValueError as e:
        print(f"Validation error: {e}")


if __name__ == "__main__":
    main()
