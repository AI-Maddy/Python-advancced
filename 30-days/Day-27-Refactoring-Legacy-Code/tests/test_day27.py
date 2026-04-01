"""
Tests for Day 27 — Refactoring Legacy Code
Run with: pytest tests/test_day27.py -v
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ["solutions", "exercises", "lesson"]:
    _sys.modules.pop(_m, None)

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from solutions import (
    InventoryChecker, NotificationService, Order,
    PriceCalculator, RefactoredOrderProcessor,
)


@pytest.fixture
def inventory() -> dict[str, int]:
    return {"widget": 10, "gadget": 5}


@pytest.fixture
def calc() -> PriceCalculator:
    return PriceCalculator()


@pytest.fixture
def checker(inventory: dict[str, int]) -> InventoryChecker:
    return InventoryChecker(inventory)


@pytest.fixture
def notifier() -> NotificationService:
    return NotificationService()


def make_order(
    customer_type: str = "regular",
    items: list[dict] | None = None,
    coupon: str = "",
) -> Order:
    return Order(
        customer_name="Test User",
        customer_type=customer_type,
        items=items or [{"name": "widget", "price": 10.0, "qty": 1}],
        coupon=coupon,
    )


# ---------------------------------------------------------------------------
# PriceCalculator tests
# ---------------------------------------------------------------------------

def test_subtotal_single_item(calc: PriceCalculator) -> None:
    order = make_order(items=[{"name": "widget", "price": 10.0, "qty": 3}])
    assert calc.subtotal(order) == pytest.approx(30.0)


def test_subtotal_multiple_items(calc: PriceCalculator) -> None:
    order = make_order(items=[
        {"name": "widget", "price": 10.0, "qty": 2},
        {"name": "gadget", "price": 25.0, "qty": 1},
    ])
    assert calc.subtotal(order) == pytest.approx(45.0)


def test_discount_regular(calc: PriceCalculator) -> None:
    order = make_order("regular")
    assert calc.discount(order) == pytest.approx(0.0)


def test_discount_member(calc: PriceCalculator) -> None:
    order = make_order("member", items=[{"name": "w", "price": 100.0, "qty": 1}])
    assert calc.discount(order) == pytest.approx(5.0)


def test_discount_vip(calc: PriceCalculator) -> None:
    order = make_order("vip", items=[{"name": "w", "price": 100.0, "qty": 1}])
    assert calc.discount(order) == pytest.approx(15.0)


def test_discount_extra10_coupon(calc: PriceCalculator) -> None:
    order = make_order("regular", items=[{"name": "w", "price": 100.0, "qty": 1}], coupon="EXTRA10")
    assert calc.discount(order) == pytest.approx(10.0)


def test_discount_vip_plus_coupon(calc: PriceCalculator) -> None:
    order = make_order("vip", items=[{"name": "w", "price": 100.0, "qty": 1}], coupon="EXTRA10")
    # 15% + 10% = 25%
    assert calc.discount(order) == pytest.approx(25.0)


def test_total_includes_tax(calc: PriceCalculator) -> None:
    order = make_order("regular", items=[{"name": "w", "price": 100.0, "qty": 1}])
    # (100 - 0) * 1.08 = 108
    assert calc.total(order) == pytest.approx(108.0)


# ---------------------------------------------------------------------------
# InventoryChecker tests
# ---------------------------------------------------------------------------

def test_check_sufficient_stock(checker: InventoryChecker) -> None:
    order = make_order(items=[{"name": "widget", "price": 10.0, "qty": 5}])
    assert checker.check(order) is None


def test_check_insufficient_stock(checker: InventoryChecker) -> None:
    order = make_order(items=[{"name": "widget", "price": 10.0, "qty": 99}])
    error = checker.check(order)
    assert error is not None
    assert "widget" in error


def test_reserve_deducts_stock(checker: InventoryChecker) -> None:
    order = make_order(items=[{"name": "widget", "price": 10.0, "qty": 3}])
    checker.reserve(order)
    assert checker._inventory["widget"] == 7


# ---------------------------------------------------------------------------
# NotificationService tests
# ---------------------------------------------------------------------------

def test_notification_sent(notifier: NotificationService) -> None:
    notifier.notify("Alice", 54.0)
    assert len(notifier.sent) == 1
    assert "Alice" in notifier.sent[0]
    assert "54.00" in notifier.sent[0]


# ---------------------------------------------------------------------------
# RefactoredOrderProcessor integration tests
# ---------------------------------------------------------------------------

def test_process_success(
    calc: PriceCalculator,
    checker: InventoryChecker,
    notifier: NotificationService,
) -> None:
    proc = RefactoredOrderProcessor(calc, checker, notifier)
    order = make_order("regular", [{"name": "widget", "price": 10.0, "qty": 1}])
    result = proc.process(order)
    assert result["status"] == "ok"
    assert "total" in result


def test_process_insufficient_stock(
    calc: PriceCalculator,
    checker: InventoryChecker,
    notifier: NotificationService,
) -> None:
    proc = RefactoredOrderProcessor(calc, checker, notifier)
    order = make_order(items=[{"name": "widget", "price": 10.0, "qty": 999}])
    result = proc.process(order)
    assert "error" in result


def test_process_sends_notification(
    calc: PriceCalculator,
    checker: InventoryChecker,
    notifier: NotificationService,
) -> None:
    proc = RefactoredOrderProcessor(calc, checker, notifier)
    order = make_order()
    proc.process(order)
    assert len(notifier.sent) == 1


@pytest.mark.skip(reason="run_legacy is in exercises.py (stub); solutions.py only contains refactored code")
def test_process_matches_legacy_total() -> None:
    """Refactored result must match legacy God-function result (from solutions)."""
    import importlib.util as _ilu, os as _oo, sys as _s27
    _sol_path = _oo.path.join(_oo.path.dirname(_oo.path.dirname(_oo.path.abspath(__file__))), "solutions.py")
    _spec = _ilu.spec_from_file_location("solutions_day27", _sol_path)
    _sol = _ilu.module_from_spec(_spec)
    _s27.modules["solutions_day27"] = _sol
    _spec.loader.exec_module(_sol)
    legacy = _sol.run_legacy()
    refactored = _sol.run_refactored()
    assert abs(legacy.get("total", 0) - refactored.get("total", 0)) < 0.01
