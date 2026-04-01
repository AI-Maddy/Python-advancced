"""
Day 18 — Solutions: SOLID Principles
======================================
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


# ---------------------------------------------------------------------------
# Solution 1 — SRP refactoring
# ---------------------------------------------------------------------------

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
    """Persists user data in memory."""

    def __init__(self) -> None:
        self._store: dict[str, UserData] = {}

    def save(self, user: UserData) -> None:
        """Save user keyed by email."""
        self._store[user.email] = user

    def find(self, email: str) -> UserData | None:
        """Look up user by email."""
        return self._store.get(email)


class UserNotifier:
    """Sends notifications to users."""

    def send_welcome(self, user: UserData) -> str:
        """Return welcome message (simulate send)."""
        return f"Welcome {user.name}! An email was sent to {user.email}."


def exercise1_srp() -> tuple[bool, bool, str]:
    """Create a valid user, validate, save, and send welcome."""
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
# Solution 2 — OCP: add MarkdownRenderer without touching existing classes
# ---------------------------------------------------------------------------

class Renderer(Protocol):
    def render(self, title: str, rows: list[str]) -> str: ...


class TextRenderer:
    def render(self, title: str, rows: list[str]) -> str:
        lines = [title, "-" * len(title)] + rows
        return "\n".join(lines)


class ReportGenerator:
    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer

    def generate(self, title: str, rows: list[str]) -> str:
        return self.renderer.render(title, rows)


class MarkdownRenderer:
    """New renderer — ReportGenerator untouched."""

    def render(self, title: str, rows: list[str]) -> str:
        bullets = "\n".join(f"- {r}" for r in rows)
        return f"## {title}\n{bullets}"


def exercise2_ocp() -> tuple[str, str]:
    title = "Sales"
    rows = ["Alice: $100", "Bob: $200"]
    text = ReportGenerator(TextRenderer()).generate(title, rows)
    md = ReportGenerator(MarkdownRenderer()).generate(title, rows)
    return (text, md)


# ---------------------------------------------------------------------------
# Solution 3 — Fix LSP violation
# ---------------------------------------------------------------------------

class Bird:
    """Base bird."""

    def swim(self) -> str:
        """All birds can paddle."""
        return f"{type(self).__name__} swimming"


class FlyingBird(Bird):
    """Birds that can fly."""

    def fly(self) -> str:
        """Fly!"""
        return f"{type(self).__name__} flying"


class Eagle(FlyingBird):
    """Eagle — can fly and swim."""


class Penguin(Bird):
    """Penguin — can swim, no fly() method."""


def exercise3_lsp() -> tuple[str, str, str]:
    eagle = Eagle()
    penguin = Penguin()
    return (eagle.fly(), penguin.swim(), eagle.swim())


# ---------------------------------------------------------------------------
# Solution 4 — Dependency Inversion
# ---------------------------------------------------------------------------

class PaymentGateway(Protocol):
    """Abstraction for payment gateways."""

    def charge(self, amount: float, token: str) -> str: ...


class StripeGateway:
    def charge(self, amount: float, token: str) -> str:
        return f"Stripe charged ${amount:.2f} with token {token}"


class PayPalGateway:
    def charge(self, amount: float, token: str) -> str:
        return f"PayPal charged ${amount:.2f} with token {token}"


class PaymentService:
    """Depends on PaymentGateway abstraction — not on Stripe or PayPal."""

    def __init__(self, gateway: PaymentGateway) -> None:
        self._gateway = gateway

    def pay(self, amount: float, token: str) -> str:
        return self._gateway.charge(amount, token)


def exercise4_dip() -> tuple[str, str]:
    stripe_result = PaymentService(StripeGateway()).pay(50.0, "tok_123")
    paypal_result = PaymentService(PayPalGateway()).pay(50.0, "tok_123")
    return (stripe_result, paypal_result)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Solution 1:", exercise1_srp())
    print("Solution 2:", exercise2_ocp())
    print("Solution 3:", exercise3_lsp())
    print("Solution 4:", exercise4_dip())
