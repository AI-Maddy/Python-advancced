"""
Day 18 — SOLID Principles
===========================
Topics:
  S — Single Responsibility Principle (SRP)
  O — Open/Closed Principle (OCP)
  L — Liskov Substitution Principle (LSP)
  I — Interface Segregation Principle (ISP)
  D — Dependency Inversion Principle (DIP)
"""
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


# ===========================================================================
# S — Single Responsibility Principle
# ===========================================================================
# "A class should have only one reason to change."
#
# BAD: OrderProcessor does too many things — order logic, formatting, AND email.

class BadOrderProcessor:
    """VIOLATION: mixes order logic, report formatting, and email sending."""

    def __init__(self, items: list[dict[str, float]]) -> None:
        self.items = items

    def calculate_total(self) -> float:
        return sum(item["price"] * item["qty"] for item in self.items)

    def format_report(self) -> str:
        lines = [f"  {i['name']}: {i['qty']} x ${i['price']:.2f}" for i in self.items]
        total = self.calculate_total()
        return "ORDER REPORT\n" + "\n".join(lines) + f"\nTotal: ${total:.2f}"

    def send_email(self, to: str) -> None:
        report = self.format_report()
        # Imagine SMTP code here — tightly coupled!
        print(f"Sending to {to}:\n{report}")


# GOOD: each class has one job.

@dataclass
class OrderItem:
    """Value object for a line item."""
    name: str
    price: float
    qty: int


class Order:
    """Responsible ONLY for order data and total calculation."""

    def __init__(self, items: list[OrderItem]) -> None:
        self.items = items

    def total(self) -> float:
        """Return total cost."""
        return sum(i.price * i.qty for i in self.items)


class OrderReportFormatter:
    """Responsible ONLY for formatting an order as text."""

    def format(self, order: Order) -> str:
        """Return a human-readable order report."""
        lines = [f"  {i.name}: {i.qty} x ${i.price:.2f}" for i in order.items]
        return "ORDER REPORT\n" + "\n".join(lines) + f"\nTotal: ${order.total():.2f}"


class EmailSender:
    """Responsible ONLY for sending emails."""

    def send(self, to: str, body: str) -> None:
        """Simulate sending an email."""
        print(f"EMAIL → {to}\n{body}")


def demo_srp() -> None:
    """Demonstrate SRP refactoring."""
    items = [OrderItem("Widget", 9.99, 3), OrderItem("Gadget", 24.99, 1)]
    order = Order(items)
    report = OrderReportFormatter().format(order)
    EmailSender().send("customer@example.com", report)


# ===========================================================================
# O — Open/Closed Principle
# ===========================================================================
# "Open for extension, closed for modification."
# Add new behaviour by adding new classes, not by editing existing ones.

@runtime_checkable
class Discount(Protocol):
    """Protocol for discount strategies — extend by adding new classes."""

    def apply(self, total: float) -> float:
        """Return discounted total."""
        ...


class NoDiscount:
    """No discount applied."""

    def apply(self, total: float) -> float:
        """Return total unchanged."""
        return total


class PercentageDiscount:
    """Apply a percentage discount."""

    def __init__(self, percent: float) -> None:
        self.percent = percent

    def apply(self, total: float) -> float:
        """Return total reduced by percent."""
        return total * (1 - self.percent / 100)


class BuyOneGetOneFreeDiscount:
    """50% discount (simulating BOGO on equal-priced items)."""

    def apply(self, total: float) -> float:
        """Return half the total."""
        return total / 2


class Cart:
    """
    Cart is CLOSED for modification.
    To add new discount types: create a new Discount class — don't touch Cart.
    """

    def __init__(self, items: list[tuple[str, float]]) -> None:
        self._items = items

    def subtotal(self) -> float:
        """Sum of all item prices."""
        return sum(price for _, price in self._items)

    def checkout(self, discount: Discount) -> float:
        """Apply discount and return final price."""
        return discount.apply(self.subtotal())


def demo_ocp() -> None:
    """Demonstrate OCP — adding new discount without modifying Cart."""
    cart = Cart([("Book", 20.0), ("Pen", 5.0)])
    print(f"No discount:  ${cart.checkout(NoDiscount()):.2f}")
    print(f"10% off:      ${cart.checkout(PercentageDiscount(10)):.2f}")
    print(f"BOGO:         ${cart.checkout(BuyOneGetOneFreeDiscount()):.2f}")


# ===========================================================================
# L — Liskov Substitution Principle
# ===========================================================================
# "Subtypes must be substitutable for their base type without breaking correctness."

# VIOLATION: Square IS-A Rectangle mathematically, but breaks invariants.

class BadRectangle:
    """Rectangle with settable width and height."""

    def __init__(self, width: float, height: float) -> None:
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, v: float) -> None:
        self._width = v

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, v: float) -> None:
        self._height = v

    def area(self) -> float:
        return self._width * self._height


class BadSquare(BadRectangle):
    """VIOLATION: setting width silently changes height too."""

    @BadRectangle.width.setter  # type: ignore[override]
    def width(self, v: float) -> None:
        self._width = v
        self._height = v  # surprise!

    @BadRectangle.height.setter  # type: ignore[override]
    def height(self, v: float) -> None:
        self._width = v  # surprise!
        self._height = v


def lsp_violation_demo() -> None:
    """Show how BadSquare breaks code that expects BadRectangle behaviour."""
    def set_width_and_check(r: BadRectangle) -> None:
        r.height = 5
        r.width = 4
        expected = 4 * 5
        actual = r.area()
        ok = "OK" if actual == expected else f"BROKEN (got {actual}, expected {expected})"
        print(f"{type(r).__name__}: area={actual} {ok}")

    set_width_and_check(BadRectangle(2, 2))
    set_width_and_check(BadSquare(2, 2))   # area=16 instead of 20!


# CORRECT FIX: don't inherit — both are Shapes.

@dataclass
class Shape(ABC):
    """Abstract shape."""

    @abstractmethod
    def area(self) -> float:
        """Return area."""


@dataclass
class Rectangle(Shape):
    """Mutable rectangle — width and height are independent."""
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height


@dataclass
class Square(Shape):
    """Square — a single side length, not a Rectangle."""
    side: float

    def area(self) -> float:
        return self.side ** 2


def demo_lsp() -> None:
    """Both Rectangle and Square satisfy the Shape contract."""
    lsp_violation_demo()
    shapes: list[Shape] = [Rectangle(4, 5), Square(4)]
    for s in shapes:
        print(f"{type(s).__name__}.area() = {s.area()}")


# ===========================================================================
# I — Interface Segregation Principle
# ===========================================================================
# "Clients should not be forced to depend on interfaces they don't use."

# BAD: fat ABC forces every implementor to implement all methods.

class FatWorkerABC(ABC):
    """VIOLATION: forces Robot to implement eat() which makes no sense."""

    @abstractmethod
    def work(self) -> str: ...

    @abstractmethod
    def eat(self) -> str: ...

    @abstractmethod
    def sleep(self) -> str: ...


# GOOD: narrow Protocols — implement only what you need.

class Workable(Protocol):
    def work(self) -> str: ...


class Eatable(Protocol):
    def eat(self) -> str: ...


class Sleepable(Protocol):
    def sleep(self) -> str: ...


class Human:
    """Humans work, eat, and sleep."""

    def work(self) -> str:
        return "Human working"

    def eat(self) -> str:
        return "Human eating"

    def sleep(self) -> str:
        return "Human sleeping"


class Robot:
    """Robots only work — no eat, no sleep needed."""

    def work(self) -> str:
        return "Robot working"


def manage_workers(workers: list[Workable]) -> list[str]:
    """Only depends on Workable — works with Human AND Robot."""
    return [w.work() for w in workers]


def demo_isp() -> None:
    """Both Human and Robot satisfy Workable without a fat ABC."""
    workers: list[Workable] = [Human(), Robot()]
    for result in manage_workers(workers):
        print(result)


# ===========================================================================
# D — Dependency Inversion Principle
# ===========================================================================
# "High-level modules should not depend on low-level modules.
#  Both should depend on abstractions (Protocols/ABCs)."

class MessageSender(Protocol):
    """Abstraction for sending messages."""

    def send(self, recipient: str, message: str) -> None:
        """Send a message to recipient."""
        ...


class SmtpEmailSender:
    """Concrete low-level: SMTP email."""

    def send(self, recipient: str, message: str) -> None:
        """Send via SMTP (simulated)."""
        print(f"SMTP → {recipient}: {message}")


class SlackSender:
    """Concrete low-level: Slack webhook."""

    def send(self, recipient: str, message: str) -> None:
        """Post to Slack channel (simulated)."""
        print(f"SLACK #{recipient}: {message}")


class NotificationService:
    """
    High-level module — depends on MessageSender Protocol, not on SMTP or Slack.
    Swap senders without changing this class.
    """

    def __init__(self, sender: MessageSender) -> None:
        self._sender = sender

    def notify(self, user: str, event: str) -> None:
        """Send a notification message."""
        self._sender.send(user, f"Event: {event}")


def demo_dip() -> None:
    """Inject different senders without modifying NotificationService."""
    for sender in (SmtpEmailSender(), SlackSender()):
        svc = NotificationService(sender)
        svc.notify("alice", "order shipped")


# ===========================================================================
# Main demo
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 18 — SOLID Principles")
    print("=" * 60)

    print("\n--- S: Single Responsibility ---")
    demo_srp()

    print("\n--- O: Open/Closed ---")
    demo_ocp()

    print("\n--- L: Liskov Substitution ---")
    demo_lsp()

    print("\n--- I: Interface Segregation ---")
    demo_isp()

    print("\n--- D: Dependency Inversion ---")
    demo_dip()
