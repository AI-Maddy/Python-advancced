"""
Tests for Day 18 — SOLID Principles
Run with: pytest tests/test_day18.py -v
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

from dataclasses import dataclass
from typing import Protocol

import pytest


# ---------------------------------------------------------------------------
# SRP tests
# ---------------------------------------------------------------------------

@dataclass
class UserData:
    name: str
    email: str
    password: str


class UserValidator:
    def validate_email(self, email: str) -> bool:
        return "@" in email

    def validate_password(self, password: str) -> bool:
        return len(password) >= 8


class UserRepository:
    def __init__(self) -> None:
        self._store: dict[str, UserData] = {}

    def save(self, user: UserData) -> None:
        self._store[user.email] = user

    def find(self, email: str) -> UserData | None:
        return self._store.get(email)


class UserNotifier:
    def send_welcome(self, user: UserData) -> str:
        return f"Welcome {user.name}! An email was sent to {user.email}."


def test_srp_validate_email() -> None:
    v = UserValidator()
    assert v.validate_email("a@b.com") is True
    assert v.validate_email("noemail") is False


def test_srp_validate_password() -> None:
    v = UserValidator()
    assert v.validate_password("longpass") is True
    assert v.validate_password("short") is False


def test_srp_repository_save_find() -> None:
    repo = UserRepository()
    u = UserData("Alice", "alice@x.com", "password1")
    repo.save(u)
    assert repo.find("alice@x.com") is u
    assert repo.find("other@x.com") is None


def test_srp_notifier() -> None:
    notifier = UserNotifier()
    u = UserData("Bob", "bob@x.com", "password1")
    msg = notifier.send_welcome(u)
    assert "Bob" in msg and "bob@x.com" in msg


# ---------------------------------------------------------------------------
# OCP tests
# ---------------------------------------------------------------------------

class Renderer(Protocol):
    def render(self, title: str, rows: list[str]) -> str: ...


class TextRenderer:
    def render(self, title: str, rows: list[str]) -> str:
        return "\n".join([title, "-" * len(title)] + rows)


class MarkdownRenderer:
    def render(self, title: str, rows: list[str]) -> str:
        return "## " + title + "\n" + "\n".join(f"- {r}" for r in rows)


class ReportGenerator:
    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer

    def generate(self, title: str, rows: list[str]) -> str:
        return self.renderer.render(title, rows)


def test_ocp_text_renderer() -> None:
    r = ReportGenerator(TextRenderer())
    out = r.generate("Sales", ["a", "b"])
    assert "Sales" in out and "-----" in out


def test_ocp_markdown_renderer() -> None:
    r = ReportGenerator(MarkdownRenderer())
    out = r.generate("Sales", ["row1"])
    assert out.startswith("## Sales")
    assert "- row1" in out


def test_ocp_report_generator_unchanged() -> None:
    """Adding MarkdownRenderer doesn't require changes to ReportGenerator."""
    class JsonRenderer:
        def render(self, title: str, rows: list[str]) -> str:
            import json
            return json.dumps({"title": title, "rows": rows})

    r = ReportGenerator(JsonRenderer())
    out = r.generate("T", ["x"])
    assert '"title": "T"' in out


# ---------------------------------------------------------------------------
# LSP tests
# ---------------------------------------------------------------------------

from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...


@dataclass
class Rectangle(Shape):
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height


@dataclass
class Square(Shape):
    side: float

    def area(self) -> float:
        return self.side ** 2


def test_lsp_rectangle_area() -> None:
    r = Rectangle(4, 5)
    assert r.area() == 20


def test_lsp_square_area() -> None:
    s = Square(4)
    assert s.area() == 16


def test_lsp_substitution() -> None:
    """Both Rectangle and Square can replace Shape without breakage."""
    shapes: list[Shape] = [Rectangle(3, 4), Square(5)]
    areas = [s.area() for s in shapes]
    assert areas == [12, 25]


# ---------------------------------------------------------------------------
# ISP tests
# ---------------------------------------------------------------------------

class Workable(Protocol):
    def work(self) -> str: ...


class Human:
    def work(self) -> str:
        return "Human working"

    def eat(self) -> str:
        return "Human eating"


class Robot:
    def work(self) -> str:
        return "Robot working"


def manage_workers(workers: list[Workable]) -> list[str]:
    return [w.work() for w in workers]


def test_isp_human_and_robot_work() -> None:
    results = manage_workers([Human(), Robot()])
    assert results == ["Human working", "Robot working"]


def test_isp_robot_has_no_eat() -> None:
    r = Robot()
    assert not hasattr(r, "eat")


# ---------------------------------------------------------------------------
# DIP tests
# ---------------------------------------------------------------------------

class PaymentGateway(Protocol):
    def charge(self, amount: float, token: str) -> str: ...


class StripeGateway:
    def charge(self, amount: float, token: str) -> str:
        return f"Stripe:{amount}:{token}"


class PayPalGateway:
    def charge(self, amount: float, token: str) -> str:
        return f"PayPal:{amount}:{token}"


class PaymentService:
    def __init__(self, gateway: PaymentGateway) -> None:
        self._gateway = gateway

    def pay(self, amount: float, token: str) -> str:
        return self._gateway.charge(amount, token)


def test_dip_stripe() -> None:
    svc = PaymentService(StripeGateway())
    result = svc.pay(100.0, "tok_abc")
    assert result == "Stripe:100.0:tok_abc"


def test_dip_paypal() -> None:
    svc = PaymentService(PayPalGateway())
    result = svc.pay(50.0, "pp_xyz")
    assert result == "PayPal:50.0:pp_xyz"


def test_dip_mock_gateway() -> None:
    """Any object with .charge() satisfies the Protocol."""
    class MockGateway:
        def charge(self, amount: float, token: str) -> str:
            return f"mock:{amount}"

    svc = PaymentService(MockGateway())
    assert svc.pay(25.0, "t") == "mock:25.0"
