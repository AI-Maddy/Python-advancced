"""
Day 19 — Solutions: Testing, Pytest & TDD
==========================================
Run with: pytest solutions.py -v
"""
from __future__ import annotations

import math
import warnings
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest


# ---------------------------------------------------------------------------
# Solution 1 — TDD: Stack implementation
# ---------------------------------------------------------------------------

class StackError(Exception):
    """Raised on invalid stack operations."""


class Stack:
    """LIFO stack with optional capacity."""

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


# --- TDD Tests ---

def test_stack_is_empty_initially() -> None:
    s = Stack()
    assert s.is_empty() is True
    assert len(s) == 0


def test_push_increases_size() -> None:
    s = Stack()
    s.push(1)
    s.push(2)
    assert len(s) == 2


def test_pop_returns_last_pushed() -> None:
    s = Stack()
    s.push("a")
    s.push("b")
    assert s.pop() == "b"
    assert s.pop() == "a"


def test_peek_does_not_remove() -> None:
    s = Stack()
    s.push(42)
    assert s.peek() == 42
    assert len(s) == 1


def test_pop_empty_raises() -> None:
    s = Stack()
    with pytest.raises(StackError, match="empty"):
        s.pop()


def test_peek_empty_raises() -> None:
    s = Stack()
    with pytest.raises(StackError):
        s.peek()


def test_push_over_capacity_raises() -> None:
    s = Stack(capacity=2)
    s.push(1)
    s.push(2)
    with pytest.raises(StackError, match="full"):
        s.push(3)


# ---------------------------------------------------------------------------
# Solution 2 — Mock an HTTP call
# ---------------------------------------------------------------------------

def fetch_user(user_id: int) -> dict[str, Any]:
    """Fetch user from remote API."""
    import requests
    resp = requests.get(f"https://api.example.com/users/{user_id}")
    return resp.json()  # type: ignore[no-any-return]


def test_fetch_user_calls_correct_url_and_returns_data() -> None:
    mock_resp = Mock()
    mock_resp.json.return_value = {"id": 42, "name": "Alice"}

    with patch("requests.get", return_value=mock_resp) as mock_get:
        result = fetch_user(42)
        mock_get.assert_called_once_with("https://api.example.com/users/42")
        assert result == {"id": 42, "name": "Alice"}


# ---------------------------------------------------------------------------
# Solution 3 — parametrize for math functions
# ---------------------------------------------------------------------------

def circle_area(radius: float) -> float:
    return math.pi * radius ** 2


def hypotenuse(a: float, b: float) -> float:
    return math.sqrt(a ** 2 + b ** 2)


@pytest.mark.parametrize("radius,expected", [
    (1, math.pi),
    (2, 4 * math.pi),
    (0, 0.0),
    (5, 25 * math.pi),
])
def test_circle_area(radius: float, expected: float) -> None:
    assert circle_area(radius) == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize("a,b,c", [
    (3, 4, 5),
    (5, 12, 13),
    (8, 15, 17),
    (1, 1, math.sqrt(2)),
])
def test_hypotenuse(a: float, b: float, c: float) -> None:
    assert hypotenuse(a, b) == pytest.approx(c, rel=1e-9)


# ---------------------------------------------------------------------------
# Solution 4 — pytest.raises and pytest.warns
# ---------------------------------------------------------------------------

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


def legacy_function() -> None:
    warnings.warn("legacy_function is deprecated", DeprecationWarning, stacklevel=2)


def test_divide_by_zero_raises() -> None:
    with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
        divide(10, 0)


def test_divide_normal() -> None:
    assert divide(10, 4) == pytest.approx(2.5)


def test_legacy_function_warns_deprecation() -> None:
    with pytest.warns(DeprecationWarning, match="deprecated"):
        legacy_function()


# ---------------------------------------------------------------------------
# Solution 5 — fixture + conftest pattern
# ---------------------------------------------------------------------------

@pytest.fixture
def filled_stack() -> Stack:
    """Return a Stack with items [1, 2, 3] already pushed."""
    s = Stack()
    for i in [1, 2, 3]:
        s.push(i)
    return s


def test_filled_stack_has_correct_size(filled_stack: Stack) -> None:
    assert len(filled_stack) == 3


def test_filled_stack_peek(filled_stack: Stack) -> None:
    assert filled_stack.peek() == 3


def test_filled_stack_pop_order(filled_stack: Stack) -> None:
    assert filled_stack.pop() == 3
    assert filled_stack.pop() == 2
    assert filled_stack.pop() == 1
    assert filled_stack.is_empty()
