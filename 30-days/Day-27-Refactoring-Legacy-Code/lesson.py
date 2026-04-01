"""
Day 27 — Refactoring Legacy Code
==================================
Demonstrates step-by-step refactoring:
  1. Deliberately messy legacy function (~200 lines)
  2. Refactored version using Extract Method, Extract Class,
     Replace Conditional with Polymorphism
  3. Adding type hints, converting to dataclasses, DI
"""
from __future__ import annotations

# ===========================================================================
# BEFORE: Legacy God-Function (deliberately messy)
# ===========================================================================
# This is what you inherit from a junior dev 3 years ago.
# Everything in one function, magic numbers, no types, no docs.

def process_order_LEGACY(order: dict) -> dict:  # noqa: N802
    """BEFORE: 200-line God function — DO NOT WRITE CODE LIKE THIS."""

    # ----- Validate order -----
    if not order:
        return {"error": "empty order"}
    if "customer" not in order:
        return {"error": "missing customer"}
    if "items" not in order or not order["items"]:
        return {"error": "no items"}
    for item in order["items"]:
        if item.get("qty", 0) <= 0:
            return {"error": f"bad qty for {item.get('name', '?')}"}
        if item.get("price", 0) <= 0:
            return {"error": f"bad price for {item.get('name', '?')}"}
        if item.get("stock", 0) < item.get("qty", 0):
            return {"error": f"insufficient stock: {item.get('name', '?')}"}

    # ----- Calculate subtotal -----
    subtotal = 0.0
    for item in order["items"]:
        subtotal += item["price"] * item["qty"]

    # ----- Apply discount -----
    discount = 0.0
    customer = order["customer"]
    if customer.get("type") == "vip":
        discount = subtotal * 0.10   # 10% for VIP
    elif customer.get("type") == "member":
        discount = subtotal * 0.05  # 5% for members
    # coupon overrides
    if order.get("coupon") == "SAVE20":
        discount = max(discount, subtotal * 0.20)  # SAVE20 = 20%
    elif order.get("coupon") == "FLAT10":
        discount = max(discount, 10.0)

    # ----- Calculate tax -----
    after_discount = subtotal - discount
    tax_rate = 0.08
    if customer.get("country") == "US" and customer.get("state") == "OR":
        tax_rate = 0.0   # Oregon has no sales tax
    elif customer.get("country") == "UK":
        tax_rate = 0.20  # UK VAT
    tax = after_discount * tax_rate

    # ----- Shipping -----
    shipping = 5.99
    if subtotal > 100:
        shipping = 0.0  # free shipping over $100
    elif customer.get("type") == "vip":
        shipping = 0.0  # VIP always free shipping

    # ----- Final total -----
    total = after_discount + tax + shipping

    # ----- Deduct inventory -----
    for item in order["items"]:
        item["stock"] -= item["qty"]   # mutates caller's data — BAD

    # ----- Send confirmation email (I/O in business logic — BAD) -----
    print(f"[EMAIL] Dear {customer.get('name', 'Customer')}, your order total is ${total:.2f}")

    # ----- Build response -----
    return {
        "status": "confirmed",
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "tax": round(tax, 2),
        "shipping": round(shipping, 2),
        "total": round(total, 2),
        "customer": customer.get("name"),
    }


# ===========================================================================
# REFACTORING STEP 1 — Extract Value Objects (dataclasses)
# ===========================================================================

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class OrderItem:
    """One line item in an order."""
    name: str
    price: float
    qty: int
    stock: int


@dataclass
class Customer:
    """Customer information."""
    name: str
    customer_type: str   # "regular", "member", "vip"
    country: str = "US"
    state: str = ""


@dataclass
class Order:
    """A customer order."""
    customer: Customer
    items: list[OrderItem]
    coupon: str = ""


@dataclass
class OrderResult:
    """Computed result of processing an order."""
    subtotal: float
    discount: float
    tax: float
    shipping: float
    total: float
    customer_name: str
    status: str = "confirmed"


# ===========================================================================
# REFACTORING STEP 2 — Extract Classes (single responsibility)
# ===========================================================================

class OrderValidator:
    """Responsible only for validating order correctness."""

    class ValidationError(ValueError):
        pass

    def validate(self, order: Order) -> None:
        """Raise ValidationError if the order is invalid."""
        if not order.items:
            raise self.ValidationError("Order has no items")
        for item in order.items:
            if item.qty <= 0:
                raise self.ValidationError(f"Invalid qty for {item.name!r}")
            if item.price <= 0:
                raise self.ValidationError(f"Invalid price for {item.name!r}")
            if item.stock < item.qty:
                raise self.ValidationError(f"Insufficient stock for {item.name!r}")


# ===========================================================================
# REFACTORING STEP 3 — Replace Conditional with Polymorphism (OCP)
# ===========================================================================

class DiscountStrategy(Protocol):
    def compute(self, subtotal: float, coupon: str) -> float: ...


class NoDiscount:
    def compute(self, subtotal: float, coupon: str) -> float:
        return _coupon_discount(coupon, subtotal)


class MemberDiscount:
    def compute(self, subtotal: float, coupon: str) -> float:
        base = subtotal * 0.05
        return max(base, _coupon_discount(coupon, subtotal))


class VipDiscount:
    def compute(self, subtotal: float, coupon: str) -> float:
        base = subtotal * 0.10
        return max(base, _coupon_discount(coupon, subtotal))


def _coupon_discount(coupon: str, subtotal: float) -> float:
    if coupon == "SAVE20":
        return subtotal * 0.20
    if coupon == "FLAT10":
        return 10.0
    return 0.0


_DISCOUNT_STRATEGIES: dict[str, DiscountStrategy] = {
    "regular": NoDiscount(),
    "member":  MemberDiscount(),
    "vip":     VipDiscount(),
}


class TaxCalculator:
    """Responsible only for tax computation."""

    _RATES: dict[tuple[str, str], float] = {
        ("US", "OR"): 0.0,
        ("UK", ""):   0.20,
    }
    _DEFAULT_RATE = 0.08

    def compute(self, amount: float, customer: Customer) -> float:
        rate = self._RATES.get((customer.country, customer.state), self._DEFAULT_RATE)
        return amount * rate


class ShippingCalculator:
    """Responsible only for shipping cost."""

    def compute(self, subtotal: float, customer: Customer) -> float:
        if subtotal > 100 or customer.customer_type == "vip":
            return 0.0
        return 5.99


# ===========================================================================
# REFACTORING STEP 4 — Notification via Dependency Injection (DIP)
# ===========================================================================

class Notifier(Protocol):
    def notify(self, customer_name: str, total: float) -> None: ...


class PrintNotifier:
    """Console notifier (for dev/test)."""
    def notify(self, customer_name: str, total: float) -> None:
        print(f"[EMAIL] Dear {customer_name}, your order total is ${total:.2f}")


class SilentNotifier:
    """No-op notifier (for tests)."""
    def notify(self, customer_name: str, total: float) -> None:
        pass   # do nothing


# ===========================================================================
# REFACTORING STEP 5 — Clean OrderProcessor (composing all pieces)
# ===========================================================================

class OrderProcessor:
    """
    AFTER: High-level coordinator — clean, focused, testable.

    Dependencies are injected; all concerns are separated.
    """

    def __init__(
        self,
        validator: OrderValidator | None = None,
        tax_calc: TaxCalculator | None = None,
        shipping_calc: ShippingCalculator | None = None,
        notifier: Notifier | None = None,
    ) -> None:
        self._validator   = validator      or OrderValidator()
        self._tax         = tax_calc       or TaxCalculator()
        self._shipping    = shipping_calc  or ShippingCalculator()
        self._notifier    = notifier       or SilentNotifier()

    def process(self, order: Order) -> OrderResult:
        """
        Validate, price, and confirm an order.

        Args:
            order: The order to process.

        Returns:
            OrderResult with all computed values.

        Raises:
            OrderValidator.ValidationError: if order data is invalid.
        """
        # 1. Validate
        self._validator.validate(order)

        # 2. Subtotal
        subtotal = sum(i.price * i.qty for i in order.items)

        # 3. Discount
        strategy = _DISCOUNT_STRATEGIES.get(
            order.customer.customer_type, NoDiscount()
        )
        discount = strategy.compute(subtotal, order.coupon)
        after_discount = subtotal - discount

        # 4. Tax
        tax = self._tax.compute(after_discount, order.customer)

        # 5. Shipping
        shipping = self._shipping.compute(subtotal, order.customer)

        # 6. Total
        total = after_discount + tax + shipping

        # 7. Notify (I/O via injected dependency — not inside business logic)
        self._notifier.notify(order.customer.name, total)

        return OrderResult(
            subtotal=round(subtotal, 2),
            discount=round(discount, 2),
            tax=round(tax, 2),
            shipping=round(shipping, 2),
            total=round(total, 2),
            customer_name=order.customer.name,
        )


# ===========================================================================
# Comparison summary
# ===========================================================================
# BEFORE (process_order_LEGACY):
#   - No types, no docstrings
#   - I/O (email) mixed with business logic
#   - Mutates caller's data (stock deduction)
#   - Monolithic — hard to test, extend, or reason about
#   - ~60 lines doing 7 different jobs
#
# AFTER (OrderProcessor):
#   - Full type hints and docstrings
#   - I/O injected via Notifier protocol
#   - Immutable data flow (Order → OrderResult)
#   - Each class has one job (SRP)
#   - Open for extension: add coupon strategy without touching OrderProcessor
#   - Easily testable with SilentNotifier and mock calculators


# ===========================================================================
# Main demo
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 27 — Refactoring Legacy Code")
    print("=" * 60)

    print("\n--- Legacy version ---")
    legacy_order = {
        "customer": {"name": "Alice", "type": "vip", "country": "US", "state": "CA"},
        "items": [
            {"name": "Widget", "price": 20.0, "qty": 3, "stock": 10},
            {"name": "Gadget", "price": 50.0, "qty": 1, "stock": 5},
        ],
        "coupon": "SAVE20",
    }
    result = process_order_LEGACY(legacy_order)
    print(f"Legacy result: {result}")

    print("\n--- Refactored version ---")
    customer = Customer("Alice", "vip", country="US", state="CA")
    items = [
        OrderItem("Widget", 20.0, 3, 10),
        OrderItem("Gadget", 50.0, 1, 5),
    ]
    order = Order(customer=customer, items=items, coupon="SAVE20")
    processor = OrderProcessor(notifier=PrintNotifier())
    result2 = processor.process(order)
    print(f"Refactored result: {result2}")
