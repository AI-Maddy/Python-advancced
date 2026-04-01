"""
Tests for Day 03 — Classes and Encapsulation
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import pytest

from solutions import BankAccount, Counter, Fraction, Rectangle


class TestBankAccount:
    def test_initial_balance(self) -> None:
        acc = BankAccount("Alice", 100.0)
        assert acc.balance == 100.0

    def test_deposit(self) -> None:
        acc = BankAccount("Alice", 100.0)
        acc.deposit(50.0)
        assert acc.balance == 150.0

    def test_deposit_invalid(self) -> None:
        acc = BankAccount("Alice", 100.0)
        with pytest.raises(ValueError):
            acc.deposit(-10.0)
        with pytest.raises(ValueError):
            acc.deposit(0.0)

    def test_withdraw_success(self) -> None:
        acc = BankAccount("Alice", 100.0)
        result = acc.withdraw(40.0)
        assert result is True
        assert acc.balance == 60.0

    def test_withdraw_insufficient(self) -> None:
        acc = BankAccount("Alice", 50.0)
        result = acc.withdraw(100.0)
        assert result is False
        assert acc.balance == 50.0  # unchanged

    def test_transfer(self) -> None:
        a = BankAccount("Alice", 100.0)
        b = BankAccount("Bob", 50.0)
        a.transfer(b, 40.0)
        assert a.balance == 60.0
        assert b.balance == 90.0

    def test_negative_initial_raises(self) -> None:
        with pytest.raises(ValueError):
            BankAccount("Alice", -10.0)

    def test_owner_readonly(self) -> None:
        acc = BankAccount("Alice", 0.0)
        assert acc.owner == "Alice"
        with pytest.raises(AttributeError):
            acc.owner = "Bob"  # type: ignore[misc]

    def test_repr(self) -> None:
        acc = BankAccount("Alice", 100.0)
        r = repr(acc)
        assert "Alice" in r
        assert "100" in r


class TestRectangle:
    def test_area(self) -> None:
        r = Rectangle(4.0, 5.0)
        assert r.area == 20.0

    def test_perimeter(self) -> None:
        r = Rectangle(4.0, 5.0)
        assert r.perimeter == 18.0

    def test_invalid_width(self) -> None:
        with pytest.raises(ValueError):
            Rectangle(0.0, 5.0)
        with pytest.raises(ValueError):
            Rectangle(-1.0, 5.0)

    def test_invalid_height(self) -> None:
        with pytest.raises(ValueError):
            Rectangle(5.0, 0.0)

    def test_square_classmethod(self) -> None:
        sq = Rectangle.square(7.0)
        assert sq.width == sq.height == 7.0
        assert sq.area == 49.0

    def test_repr(self) -> None:
        r = Rectangle(3.0, 4.0)
        assert "3.0" in repr(r)
        assert "4.0" in repr(r)


class TestFraction:
    def test_creation(self) -> None:
        f = Fraction(3, 4)
        assert f.numerator == 3
        assert f.denominator == 4

    def test_reduction(self) -> None:
        f = Fraction(6, 4)
        assert f.numerator == 3
        assert f.denominator == 2

    def test_equality(self) -> None:
        assert Fraction(1, 2) == Fraction(2, 4)
        assert Fraction(3, 6) == Fraction(1, 2)

    def test_addition(self) -> None:
        result = Fraction(1, 2) + Fraction(1, 3)
        assert result == Fraction(5, 6)

    def test_multiplication(self) -> None:
        result = Fraction(2, 3) * Fraction(3, 4)
        assert result == Fraction(1, 2)

    def test_str(self) -> None:
        assert str(Fraction(3, 4)) == "3/4"

    def test_repr(self) -> None:
        assert repr(Fraction(3, 4)) == "Fraction(3, 4)"

    def test_zero_denominator(self) -> None:
        with pytest.raises(ZeroDivisionError):
            Fraction(1, 0)

    def test_hashable(self) -> None:
        s = {Fraction(1, 2), Fraction(2, 4), Fraction(1, 3)}
        assert len(s) == 2  # 1/2 and 2/4 are the same


class TestCounter:
    def test_starts_at_zero(self) -> None:
        c = Counter("test")
        assert c.count == 0

    def test_increment(self) -> None:
        c = Counter("test")
        c.increment()
        assert c.count == 1

    def test_increment_by(self) -> None:
        c = Counter("test")
        c.increment(5)
        assert c.count == 5

    def test_instance_count(self) -> None:
        initial = Counter.instance_count()
        Counter("x")
        Counter("y")
        assert Counter.instance_count() == initial + 2

    def test_independent_counters(self) -> None:
        c1 = Counter("a")
        c2 = Counter("b")
        c1.increment()
        c1.increment()
        assert c1.count == 2
        assert c2.count == 0
