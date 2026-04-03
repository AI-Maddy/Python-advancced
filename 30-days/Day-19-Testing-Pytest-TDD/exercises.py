"""
Day 19 — Exercises: Testing, Pytest & TDD
==========================================
Write the tests (and the code they test) for each exercise.
Run with: pytest exercises.py -v
"""
from __future__ import annotations

from typing import Any
from unittest.mock import Mock, patch

import pytest


# ---------------------------------------------------------------------------
# Exercise 1 — TDD: Stack implementation
# ---------------------------------------------------------------------------
# TODO: Implement the Stack class below AFTER writing the tests.
# Write at least 5 tests that cover:
#   push, pop, peek, is_empty, capacity enforcement, pop from empty.

class StackError(Exception):
    """Raised on invalid stack operations."""


class Stack:
    """LIFO stack with optional capacity."""

    def __init__(self, capacity: int | None = None) -> None:
        self._data: list[Any] = []
        self.capacity = capacity

    def push(self, item: Any) -> None:
        """Push item onto the stack."""
        if self.capacity is not None and len(self._data) >= self.capacity:
            raise StackError(f"Stack full (capacity={self.capacity})")
        self._data.append(item)

    def pop(self) -> Any:
        """Remove and return top item (raise StackError if empty)."""
        if not self._data:
            raise StackError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        """Return top item without removing it (raise StackError if empty)."""
        if not self._data:
            raise StackError("peek at empty stack")
        return self._data[-1]

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        """Return True if stack has no items."""
        return len(self._data) == 0


# --- Write your TDD tests below ---

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


def test_push_over_capacity_raises() -> None:
    s = Stack(capacity=2)
    s.push(1)
    s.push(2)
    with pytest.raises(StackError, match="full"):
        s.push(3)


# ---------------------------------------------------------------------------
# Exercise 2 — Mock an HTTP call
# ---------------------------------------------------------------------------
# TODO: Write a function fetch_user(user_id: int) -> dict that calls
#       requests.get("https://api.example.com/users/{user_id}").json().
#       Then write a test that mocks requests.get so no real HTTP is made.

def fetch_user(user_id: int) -> dict[str, Any]:
    """
    Fetch user from remote API.
    TODO: implement using requests.get(...).json()
    """
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
# Exercise 3 — parametrize for math functions
# ---------------------------------------------------------------------------
# TODO: Write parametrized tests for the functions below.

import math as _math


def circle_area(radius: float) -> float:
    """Return area of circle with given radius."""
    return _math.pi * radius ** 2


def hypotenuse(a: float, b: float) -> float:
    """Return hypotenuse of right triangle."""
    return _math.sqrt(a ** 2 + b ** 2)


@pytest.mark.parametrize("radius,expected", [
    (1, _math.pi),
    (2, 4 * _math.pi),
    (0, 0.0),
    (5, 25 * _math.pi),
])
def test_circle_area(radius: float, expected: float) -> None:
    assert circle_area(radius) == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize("a,b,c", [
    (3, 4, 5),
    (5, 12, 13),
    (8, 15, 17),
    (1, 1, _math.sqrt(2)),
])
def test_hypotenuse(a: float, b: float, c: float) -> None:
    assert hypotenuse(a, b) == pytest.approx(c, rel=1e-9)


# ---------------------------------------------------------------------------
# Exercise 4 — pytest.raises and pytest.warns
# ---------------------------------------------------------------------------

import warnings as _warnings


def divide(a: float, b: float) -> float:
    """Divide a by b; raises ZeroDivisionError when b == 0."""
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


def legacy_function() -> None:
    """Issues a DeprecationWarning — use new_function() instead."""
    _warnings.warn("legacy_function is deprecated", DeprecationWarning, stacklevel=2)


def test_divide_by_zero_raises() -> None:
    with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
        divide(10, 0)


def test_legacy_function_warns_deprecation() -> None:
    with pytest.warns(DeprecationWarning, match="deprecated"):
        legacy_function()


# ---------------------------------------------------------------------------
# Exercise 5 — fixture + conftest pattern (inline)
# ---------------------------------------------------------------------------
# TODO: Use a @pytest.fixture to create a pre-populated Stack,
#       then write 3 tests that share that fixture.

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
