"""
Day 27 — Exercises: Refactoring Legacy Code
=============================================
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


# ---------------------------------------------------------------------------
# Exercise: Refactor the God Class below into clean components
# ---------------------------------------------------------------------------
# This OrderProcessor does too many things.  Break it apart into:
#   - Order (dataclass holding order data)
#   - PriceCalculator (computes subtotal, discount, tax, total)
#   - InventoryChecker (checks stock, reserves items)
#   - NotificationService (sends confirmation)
#   - RefactoredOrderProcessor (coordinates the above)

class GodOrderProcessor:
    """
    LEGACY — DO NOT MODIFY THIS CLASS.
    Refactor its behaviour into the classes below.
    """

    def __init__(self) -> None:
        self._inventory: dict[str, int] = {"widget": 10, "gadget": 5}
        self._notifications: list[str] = []

    def process(
        self,
        customer_name: str,
        customer_type: str,
        items: list[dict],  # [{"name": str, "price": float, "qty": int}]
        coupon: str = "",
    ) -> dict:
        # Validate
        for item in items:
            stock = self._inventory.get(item["name"], 0)
            if stock < item["qty"]:
                return {"error": f"insufficient stock: {item['name']}"}

        # Compute subtotal
        subtotal = sum(i["price"] * i["qty"] for i in items)

        # Discount
        if customer_type == "vip":
            discount = subtotal * 0.15
        elif customer_type == "member":
            discount = subtotal * 0.05
        else:
            discount = 0.0
        if coupon == "EXTRA10":
            discount += subtotal * 0.10

        # Tax
        total = (subtotal - discount) * 1.08

        # Reserve inventory
        for item in items:
            self._inventory[item["name"]] = self._inventory.get(item["name"], 0) - item["qty"]

        # Notify
        msg = f"Confirmed for {customer_name}: ${total:.2f}"
        self._notifications.append(msg)

        return {"status": "ok", "total": round(total, 2)}


# ---------------------------------------------------------------------------
# TODO: Implement the refactored components below
# ---------------------------------------------------------------------------

@dataclass
class Order:
    """TODO: hold order data."""
    customer_name: str
    customer_type: str    # "regular", "member", "vip"
    items: list[dict]     # [{"name": str, "price": float, "qty": int}]
    coupon: str = ""


class PriceCalculator:
    """TODO: compute subtotal, discount, total."""

    def subtotal(self, order: Order) -> float:
        # TODO
        ...
        return 0.0

    def discount(self, order: Order) -> float:
        # TODO: 15% for vip, 5% for member + 10% extra for EXTRA10 coupon
        ...
        return 0.0

    def total(self, order: Order) -> float:
        # TODO: (subtotal - discount) * 1.08 (tax)
        ...
        return 0.0


class InventoryChecker:
    """TODO: check and reserve stock."""

    def __init__(self, inventory: dict[str, int]) -> None:
        # TODO
        ...

    def check(self, order: Order) -> str | None:
        """Return error message if insufficient stock, else None."""
        # TODO
        ...
        return None

    def reserve(self, order: Order) -> None:
        """Deduct quantities from inventory."""
        # TODO
        ...


class NotificationService:
    """TODO: track sent notifications."""

    def __init__(self) -> None:
        self.sent: list[str] = []

    def notify(self, customer_name: str, total: float) -> None:
        """TODO: append message to self.sent."""
        # TODO
        ...


class RefactoredOrderProcessor:
    """TODO: coordinate Order, PriceCalculator, InventoryChecker, NotificationService."""

    def __init__(
        self,
        calculator: PriceCalculator,
        checker: InventoryChecker,
        notifier: NotificationService,
    ) -> None:
        # TODO
        ...

    def process(self, order: Order) -> dict:
        """TODO: validate → calculate → reserve → notify → return result."""
        # TODO
        ...
        return {}


# ---------------------------------------------------------------------------
# Verify refactoring produces same results as legacy
# ---------------------------------------------------------------------------

def run_legacy() -> dict:
    proc = GodOrderProcessor()
    return proc.process(
        "Alice", "vip",
        [{"name": "widget", "price": 10.0, "qty": 2}],
        coupon="EXTRA10",
    )


def run_refactored() -> dict:
    inventory = {"widget": 10, "gadget": 5}
    order = Order(
        customer_name="Alice",
        customer_type="vip",
        items=[{"name": "widget", "price": 10.0, "qty": 2}],
        coupon="EXTRA10",
    )
    calc    = PriceCalculator()
    checker = InventoryChecker(inventory)
    notif   = NotificationService()
    proc    = RefactoredOrderProcessor(calc, checker, notif)
    return proc.process(order)


if __name__ == "__main__":
    legacy = run_legacy()
    refactored = run_refactored()
    print(f"Legacy result:     {legacy}")
    print(f"Refactored result: {refactored}")
    match = legacy.get("total") == refactored.get("total")
    print(f"Results match: {match}")
