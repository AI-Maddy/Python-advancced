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
        # TODO: implement
        ...

    def push(self, item: Any) -> None:
        """Push item onto the stack."""
        # TODO: implement (raise StackError if over capacity)
        ...

    def pop(self) -> Any:
        """Remove and return top item (raise StackError if empty)."""
        # TODO: implement
        ...

    def peek(self) -> Any:
        """Return top item without removing it (raise StackError if empty)."""
        # TODO: implement
        ...

    def __len__(self) -> int:
        # TODO: implement
        ...
        return 0

    def is_empty(self) -> bool:
        """Return True if stack has no items."""
        # TODO: implement
        ...
        return True


# --- Write your TDD tests below ---

# TODO: test_stack_is_empty_initially
# TODO: test_push_increases_size
# TODO: test_pop_returns_last_pushed
# TODO: test_peek_does_not_remove
# TODO: test_pop_empty_raises
# TODO: test_push_over_capacity_raises


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
    # TODO
    ...
    return {}


# TODO: test_fetch_user_calls_correct_url_and_returns_data


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


# TODO: @pytest.mark.parametrize test for circle_area with approx checks
# TODO: @pytest.mark.parametrize test for hypotenuse (3,4,5) (5,12,13) etc.


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


# TODO: test_divide_by_zero_raises
# TODO: test_legacy_function_warns_deprecation


# ---------------------------------------------------------------------------
# Exercise 5 — fixture + conftest pattern (inline)
# ---------------------------------------------------------------------------
# TODO: Use a @pytest.fixture to create a pre-populated Stack,
#       then write 3 tests that share that fixture.

@pytest.fixture
def filled_stack() -> Stack:
    """TODO: return a Stack with items [1, 2, 3] already pushed."""
    # TODO
    ...
    return Stack()


# TODO: test_filled_stack_has_correct_size(filled_stack)
# TODO: test_filled_stack_peek(filled_stack)
# TODO: test_filled_stack_pop_order(filled_stack)
