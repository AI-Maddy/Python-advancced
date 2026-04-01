"""
Day 27 — Solutions: Refactoring Legacy Code
=============================================
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Order:
    customer_name: str
    customer_type: str
    items: list[dict]
    coupon: str = ""


class PriceCalculator:
    def subtotal(self, order: Order) -> float:
        return sum(i["price"] * i["qty"] for i in order.items)

    def discount(self, order: Order) -> float:
        sub = self.subtotal(order)
        if order.customer_type == "vip":
            d = sub * 0.15
        elif order.customer_type == "member":
            d = sub * 0.05
        else:
            d = 0.0
        if order.coupon == "EXTRA10":
            d += sub * 0.10
        return d

    def total(self, order: Order) -> float:
        return (self.subtotal(order) - self.discount(order)) * 1.08


class InventoryChecker:
    def __init__(self, inventory: dict[str, int]) -> None:
        self._inventory = dict(inventory)

    def check(self, order: Order) -> str | None:
        for item in order.items:
            available = self._inventory.get(item["name"], 0)
            if available < item["qty"]:
                return f"insufficient stock: {item['name']}"
        return None

    def reserve(self, order: Order) -> None:
        for item in order.items:
            self._inventory[item["name"]] = (
                self._inventory.get(item["name"], 0) - item["qty"]
            )


class NotificationService:
    def __init__(self) -> None:
        self.sent: list[str] = []

    def notify(self, customer_name: str, total: float) -> None:
        msg = f"Confirmed for {customer_name}: ${total:.2f}"
        self.sent.append(msg)


class RefactoredOrderProcessor:
    def __init__(
        self,
        calculator: PriceCalculator,
        checker: InventoryChecker,
        notifier: NotificationService,
    ) -> None:
        self._calc    = calculator
        self._checker = checker
        self._notifier = notifier

    def process(self, order: Order) -> dict:
        error = self._checker.check(order)
        if error:
            return {"error": error}
        total = self._calc.total(order)
        self._checker.reserve(order)
        self._notifier.notify(order.customer_name, total)
        return {"status": "ok", "total": round(total, 2)}


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
    result = run_refactored()
    print("Result:", result)
    # Legacy comparison
    from exercises import run_legacy
    legacy = run_legacy()
    print(f"Legacy total: {legacy.get('total'):.2f}")
    print(f"Refactored total: {result.get('total'):.2f}")
    print(f"Match: {abs(legacy.get('total', 0) - result.get('total', 0)) < 0.01}")
