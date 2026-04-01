"""
Example 1 — Slots for a high-frequency data record.
"""
from __future__ import annotations

import sys


class TradeEvent:
    """Without slots."""
    def __init__(self, symbol: str, price: float, qty: int, side: str) -> None:
        self.symbol = symbol
        self.price = price
        self.qty = qty
        self.side = side


class TradeEventSlotted:
    """With slots — lower per-instance overhead."""
    __slots__ = ("symbol", "price", "qty", "side")

    def __init__(self, symbol: str, price: float, qty: int, side: str) -> None:
        self.symbol = symbol
        self.price = price
        self.qty = qty
        self.side = side


def main() -> None:
    normal = TradeEvent("AAPL", 175.50, 100, "BUY")
    slotted = TradeEventSlotted("AAPL", 175.50, 100, "BUY")

    print(f"TradeEvent size      : {sys.getsizeof(normal)} bytes")
    print(f"TradeEventSlotted sz : {sys.getsizeof(slotted)} bytes")
    print(f"Has __dict__  normal : {hasattr(normal, '__dict__')}")
    print(f"Has __dict__ slotted : {hasattr(slotted, '__dict__')}")

    # Attribute access is the same
    assert normal.price == slotted.price
    print(f"Attribute access works: {slotted.price}")


if __name__ == "__main__":
    main()
