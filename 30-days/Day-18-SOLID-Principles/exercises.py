"""
Day 18 — Exercises: SOLID Principles
======================================
Complete each TODO.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol


# ---------------------------------------------------------------------------
# Exercise 1 — Refactor a God Class (SRP)
# ---------------------------------------------------------------------------
# The class below violates SRP by doing too many things.
# TODO: Refactor into separate classes:
#   - UserData (stores user fields)
#   - UserValidator (validates email/password)
#   - UserRepository (save/load from dict store)
#   - UserNotifier (sends welcome email)

class GodClassUser:
    """VIOLATION: does everything."""

    def __init__(self, name: str, email: str, password: str) -> None:
        self.name = name
        self.email = email
        self.password = password
        self._store: dict[str, Any] = {}

    def validate_email(self) -> bool:
        return "@" in self.email

    def validate_password(self) -> bool:
        return len(self.password) >= 8

    def save(self) -> None:
        self._store[self.email] = {"name": self.name, "email": self.email}

    def send_welcome_email(self) -> str:
        return f"Welcome {self.name}! An email was sent to {self.email}."


# TODO: Define UserData, UserValidator, UserRepository, UserNotifier here.

@dataclass
class UserData:
    """Holds user fields only."""
    name: str
    email: str
    password: str


class UserValidator:
    """Validates user data."""

    def validate_email(self, email: str) -> bool:
        """Return True if email contains '@'."""
        return "@" in email

    def validate_password(self, password: str) -> bool:
        """Return True if password is at least 8 characters."""
        return len(password) >= 8


class UserRepository:
    """Persists user data."""

    def __init__(self) -> None:
        self._store: dict[str, UserData] = {}

    def save(self, user: UserData) -> None:
        """Save user keyed by email."""
        self._store[user.email] = user

    def find(self, email: str) -> UserData | None:
        """Look up user by email."""
        return self._store.get(email)


class UserNotifier:
    """Sends notifications."""
    def send_welcome(self, user: UserData) -> str:
        """Return welcome message (simulate send)."""
        return f"Welcome {user.name}! An email was sent to {user.email}."


def exercise1_srp() -> tuple[bool, bool, str]:
    """
    Create a valid user, validate, save, and send welcome.
    Return (email_valid, password_valid, welcome_message).
    """
    user = UserData("Alice", "alice@example.com", "s3cr3tPwd")
    validator = UserValidator()
    repo = UserRepository()
    notifier = UserNotifier()

    email_ok = validator.validate_email(user.email)
    pass_ok = validator.validate_password(user.password)
    repo.save(user)
    msg = notifier.send_welcome(user)
    return (email_ok, pass_ok, msg)


# ---------------------------------------------------------------------------
# Exercise 2 — Add Feature without Modifying Existing Code (OCP)
# ---------------------------------------------------------------------------
# A ReportGenerator accepts a Renderer protocol.
# TODO: Add a MarkdownRenderer without modifying ReportGenerator or TextRenderer.

class Renderer(Protocol):
    def render(self, title: str, rows: list[str]) -> str: ...


class TextRenderer:
    """Renders as plain text."""

    def render(self, title: str, rows: list[str]) -> str:
        lines = [title, "-" * len(title)] + rows
        return "\n".join(lines)


class ReportGenerator:
    """Generates a report using an injected renderer — closed for modification."""

    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer

    def generate(self, title: str, rows: list[str]) -> str:
        """Generate and return report string."""
        return self.renderer.render(title, rows)


class MarkdownRenderer:
    """Render as Markdown (## title, then bullet list)."""

    def render(self, title: str, rows: list[str]) -> str:
        bullets = "\n".join(f"- {r}" for r in rows)
        return f"## {title}\n{bullets}"


def exercise2_ocp() -> tuple[str, str]:
    """Return (text_report, markdown_report) for same data."""
    title = "Sales"
    rows = ["Alice: $100", "Bob: $200"]
    text = ReportGenerator(TextRenderer()).generate(title, rows)
    md = ReportGenerator(MarkdownRenderer()).generate(title, rows)
    return (text, md)


# ---------------------------------------------------------------------------
# Exercise 3 — Fix LSP Violation
# ---------------------------------------------------------------------------
# The Bird/Penguin hierarchy below violates LSP because Penguin.fly() raises.
# TODO: Redesign so substitution works.

class BadBird:
    def fly(self) -> str:
        return "flying"


class BadPenguin(BadBird):
    def fly(self) -> str:
        raise NotImplementedError("Penguins can't fly!")  # LSP violation


# TODO: Create a correct hierarchy:
#   Bird (base, no fly method), FlyingBird(Bird) with fly(), Penguin(Bird).
#   Both should be usable as Bird without surprises.

class Bird:
    """Base bird — all birds can swim."""
    def swim(self) -> str:
        return f"{type(self).__name__} swimming"


class FlyingBird(Bird):
    """Birds that can fly."""
    def fly(self) -> str:
        return f"{type(self).__name__} flying"


class Eagle(FlyingBird):
    """Eagle — can fly and swim."""


class Penguin(Bird):
    """Penguin: can swim, cannot fly — no fly() method at all."""
    ...


def exercise3_lsp() -> tuple[str, str, str]:
    """
    Return (eagle.fly(), penguin.swim(), eagle.swim()).
    No LSP violation — Penguin does not have .fly().
    """
    eagle = Eagle()
    penguin = Penguin()
    return (eagle.fly(), penguin.swim(), eagle.swim())


# ---------------------------------------------------------------------------
# Exercise 4 — Apply Dependency Inversion
# ---------------------------------------------------------------------------
# TODO: Refactor the PaymentService below so it depends on a PaymentGateway
#       Protocol instead of a concrete StripeGateway.
#       Add a PayPalGateway that satisfies the same Protocol.

class StripeGateway:
    """Low-level Stripe implementation."""

    def charge(self, amount: float, token: str) -> str:
        return f"Stripe charged ${amount:.2f} with token {token}"


class BadPaymentService:
    """VIOLATION: hard-coded dependency on StripeGateway."""

    def __init__(self) -> None:
        self.gateway = StripeGateway()  # cannot swap without modification

    def pay(self, amount: float, token: str) -> str:
        return self.gateway.charge(amount, token)


class PaymentGateway(Protocol):
    """Abstraction for payment gateways."""
    def charge(self, amount: float, token: str) -> str: ...


class PayPalGateway:
    """PayPal gateway satisfying PaymentGateway protocol."""
    def charge(self, amount: float, token: str) -> str:
        return f"PayPal charged ${amount:.2f} with token {token}"


class PaymentService:
    """High-level service depending on PaymentGateway abstraction."""

    def __init__(self, gateway: PaymentGateway) -> None:
        self._gateway = gateway

    def pay(self, amount: float, token: str) -> str:
        return self._gateway.charge(amount, token)


def exercise4_dip() -> tuple[str, str]:
    """
    Return (stripe_result, paypal_result) for $50 charge with token "tok_123".
    """
    stripe_result = PaymentService(StripeGateway()).pay(50.0, "tok_123")
    paypal_result = PaymentService(PayPalGateway()).pay(50.0, "tok_123")
    return (stripe_result, paypal_result)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_srp())
    print("Exercise 2:", exercise2_ocp())
    print("Exercise 3:", exercise3_lsp())
    print("Exercise 4:", exercise4_dip())
