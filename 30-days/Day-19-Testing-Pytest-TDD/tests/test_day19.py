"""
Tests for Day 19 — Testing, Pytest & TDD
Run with: pytest tests/test_day19.py -v
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import math
import warnings
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest


# ---------------------------------------------------------------------------
# Code under test (inlined to keep the test file self-contained)
# ---------------------------------------------------------------------------

class StackError(Exception):
    pass


class Stack:
    def __init__(self, capacity: int | None = None) -> None:
        self._data: list[Any] = []
        self.capacity = capacity

    def push(self, item: Any) -> None:
        if self.capacity is not None and len(self._data) >= self.capacity:
            raise StackError(f"Stack full (capacity={self.capacity})")
        self._data.append(item)

    def pop(self) -> Any:
        if not self._data:
            raise StackError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        if not self._data:
            raise StackError("peek at empty stack")
        return self._data[-1]

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def empty_stack() -> Stack:
    """An empty Stack."""
    return Stack()


@pytest.fixture
def bounded_stack() -> Stack:
    """A Stack with capacity=3."""
    return Stack(capacity=3)


@pytest.fixture
def filled_stack() -> Stack:
    """A Stack pre-loaded with [10, 20, 30]."""
    s = Stack()
    for v in [10, 20, 30]:
        s.push(v)
    return s


# ---------------------------------------------------------------------------
# Basic stack tests
# ---------------------------------------------------------------------------

def test_new_stack_is_empty(empty_stack: Stack) -> None:
    assert empty_stack.is_empty() is True
    assert len(empty_stack) == 0


def test_push_then_len(empty_stack: Stack) -> None:
    empty_stack.push("x")
    assert len(empty_stack) == 1
    assert empty_stack.is_empty() is False


def test_pop_returns_lifo_order(filled_stack: Stack) -> None:
    assert filled_stack.pop() == 30
    assert filled_stack.pop() == 20
    assert filled_stack.pop() == 10


def test_peek_does_not_remove(filled_stack: Stack) -> None:
    top = filled_stack.peek()
    assert top == 30
    assert len(filled_stack) == 3


def test_pop_empty_raises(empty_stack: Stack) -> None:
    with pytest.raises(StackError, match="empty"):
        empty_stack.pop()


def test_peek_empty_raises(empty_stack: Stack) -> None:
    with pytest.raises(StackError):
        empty_stack.peek()


def test_bounded_stack_enforces_capacity(bounded_stack: Stack) -> None:
    bounded_stack.push(1)
    bounded_stack.push(2)
    bounded_stack.push(3)
    with pytest.raises(StackError, match="full"):
        bounded_stack.push(4)


def test_pop_after_fill_makes_room(bounded_stack: Stack) -> None:
    bounded_stack.push(1)
    bounded_stack.push(2)
    bounded_stack.push(3)
    bounded_stack.pop()          # make room
    bounded_stack.push(4)        # should not raise
    assert len(bounded_stack) == 3


# ---------------------------------------------------------------------------
# pytest.approx tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("radius,expected", [
    (1, math.pi),
    (2, 4 * math.pi),
    (0, 0.0),
])
def test_circle_area(radius: float, expected: float) -> None:
    area = math.pi * radius ** 2
    assert area == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize("a,b,hyp", [
    (3, 4, 5),
    (5, 12, 13),
])
def test_hypotenuse(a: float, b: float, hyp: float) -> None:
    assert math.sqrt(a**2 + b**2) == pytest.approx(hyp)


# ---------------------------------------------------------------------------
# pytest.raises / pytest.warns
# ---------------------------------------------------------------------------

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


def deprecated_fn() -> None:
    warnings.warn("use new_fn() instead", DeprecationWarning, stacklevel=2)


def test_divide_by_zero() -> None:
    with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
        divide(5, 0)


def test_divide_ok() -> None:
    assert divide(10, 4) == pytest.approx(2.5)


def test_deprecation_warning() -> None:
    with pytest.warns(DeprecationWarning, match="new_fn"):
        deprecated_fn()


# ---------------------------------------------------------------------------
# Mock tests
# ---------------------------------------------------------------------------

def fetch_data(url: str) -> dict[str, Any]:
    """Simulated HTTP fetch — we will mock this."""
    import urllib.request, json
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())


def test_mock_return_value() -> None:
    m = Mock()
    m.fetch.return_value = {"status": "ok"}
    result = m.fetch("http://example.com")
    assert result == {"status": "ok"}
    m.fetch.assert_called_once_with("http://example.com")


def test_mock_side_effect() -> None:
    m = Mock()
    m.fetch.side_effect = ConnectionError("timeout")
    with pytest.raises(ConnectionError, match="timeout"):
        m.fetch("http://example.com")


def test_patch_urllib(monkeypatch: pytest.MonkeyPatch) -> None:
    """Use monkeypatch to avoid real HTTP in fetch_data."""
    # We patch urllib.request.urlopen via monkeypatch
    import io, json, urllib.request

    fake_resp = MagicMock()
    fake_resp.__enter__ = lambda s: s
    fake_resp.__exit__ = MagicMock(return_value=False)
    fake_resp.read.return_value = json.dumps({"temp": 22}).encode()

    monkeypatch.setattr(urllib.request, "urlopen", lambda url: fake_resp)
    result = fetch_data("http://fake")
    assert result == {"temp": 22}


# ---------------------------------------------------------------------------
# MagicMock dunder support
# ---------------------------------------------------------------------------

def test_magic_mock_len() -> None:
    mm = MagicMock()
    mm.__len__.return_value = 7
    assert len(mm) == 7


def test_magic_mock_context_manager() -> None:
    mm = MagicMock()
    mm.__enter__.return_value = "resource"
    mm.__exit__.return_value = False
    with mm as r:
        assert r == "resource"
