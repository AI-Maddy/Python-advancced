"""
Day 19 — Testing, Pytest & TDD
================================
Topics:
  - pytest fixtures, conftest.py, parametrize, marks
  - pytest.raises, pytest.warns, pytest.approx
  - unittest.mock: Mock, MagicMock, patch, patch.object
  - TDD red-green-refactor cycle demonstrated
  - pytest-cov coverage intro
  - hypothesis property-based testing intro
"""
from __future__ import annotations

import math
import warnings
from collections.abc import Iterator
from typing import Any
from unittest.mock import MagicMock, Mock, patch, patch as mock_patch


# ===========================================================================
# 1. The code under test — a simple Stack
# ===========================================================================

class StackError(Exception):
    """Raised for invalid Stack operations."""


class Stack:
    """
    LIFO stack with optional max capacity.

    >>> s = Stack()
    >>> s.push(1)
    >>> s.pop()
    1
    """

    def __init__(self, capacity: int | None = None) -> None:
        self._data: list[Any] = []
        self.capacity = capacity

    def push(self, item: Any) -> None:
        """Push item onto the stack."""
        if self.capacity is not None and len(self._data) >= self.capacity:
            raise StackError(f"Stack is full (capacity={self.capacity})")
        self._data.append(item)

    def pop(self) -> Any:
        """Remove and return top item."""
        if not self._data:
            raise StackError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        """Return top item without removing it."""
        if not self._data:
            raise StackError("peek at empty stack")
        return self._data[-1]

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        """Return True if stack has no items."""
        return len(self._data) == 0


# ===========================================================================
# 2. A service that makes HTTP calls — for mocking demo
# ===========================================================================

class WeatherService:
    """
    Fetches weather data from an external API.
    In tests we mock the HTTP call, not the business logic.
    """

    BASE_URL = "https://api.weather.example.com"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def get_temperature(self, city: str) -> float:
        """
        Return temperature in Celsius for ``city``.
        Raises ``ValueError`` if city not found.
        """
        import urllib.request, json
        url = f"{self.BASE_URL}/temp?city={city}&key={self._api_key}"
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read())
        if "error" in data:
            raise ValueError(data["error"])
        return float(data["temp_c"])


# ===========================================================================
# 3. pytest concepts (described — actual tests go in tests/)
# ===========================================================================

# --- FIXTURES ---
# A fixture is a function decorated with @pytest.fixture that provides
# test inputs/resources.  pytest auto-injects them by parameter name.
#
# Example:
#   @pytest.fixture
#   def stack() -> Stack:
#       return Stack()
#
#   def test_push(stack: Stack) -> None:
#       stack.push(42)
#       assert len(stack) == 1

# --- CONFTEST.PY ---
# Fixtures defined in conftest.py are shared across the whole directory tree.
# No import needed — pytest discovers them automatically.

# --- PARAMETRIZE ---
# @pytest.mark.parametrize("a,b,expected", [(1,2,3), (0,0,0), (-1,1,0)])
# def test_add(a: int, b: int, expected: int) -> None:
#     assert add(a, b) == expected

# --- MARKS ---
# @pytest.mark.slow      — custom mark for slow tests
# @pytest.mark.skip      — always skip
# @pytest.mark.skipif(condition, reason="...")
# @pytest.mark.xfail     — expected to fail

# --- pytest.raises ---
# with pytest.raises(StackError, match="empty"):
#     stack.pop()

# --- pytest.warns ---
# with pytest.warns(DeprecationWarning):
#     deprecated_function()

# --- pytest.approx ---
# assert 0.1 + 0.2 == pytest.approx(0.3)
# assert math.sqrt(2) == pytest.approx(1.4142, rel=1e-4)


# ===========================================================================
# 4. unittest.mock — mocking external dependencies
# ===========================================================================

def demo_mock() -> None:
    """Show Mock, MagicMock, patch usage (conceptual)."""

    # --- Mock: records calls, returns Magic values ---
    m = Mock()
    m.do_something(1, key="value")
    print(m.do_something.call_count)   # 1
    m.do_something.assert_called_once_with(1, key="value")

    # --- MagicMock: also supports dunder methods ---
    mm = MagicMock()
    mm.__len__.return_value = 5
    print(len(mm))  # 5

    # --- Mock return value and side_effect ---
    fetcher = Mock()
    fetcher.fetch.return_value = {"temp_c": 22.5}
    print(fetcher.fetch("London"))

    fetcher.fetch.side_effect = ConnectionError("timeout")
    try:
        fetcher.fetch("Paris")
    except ConnectionError as e:
        print(f"Got expected error: {e}")

    # --- patch as context manager ---
    # with patch("urllib.request.urlopen") as mock_urlopen:
    #     mock_urlopen.return_value.__enter__.return_value.read.return_value = b'{"temp_c":20}'
    #     svc = WeatherService("key")
    #     temp = svc.get_temperature("London")
    #     assert temp == 20.0

    # --- patch.object ---
    # with patch.object(WeatherService, "get_temperature", return_value=25.0):
    #     svc = WeatherService("key")
    #     assert svc.get_temperature("anywhere") == 25.0


# ===========================================================================
# 5. TDD Red-Green-Refactor cycle (narrative)
# ===========================================================================
# RED:   Write a failing test for a feature that doesn't exist yet.
# GREEN: Write the minimal code to make the test pass (no more).
# REFACTOR: Clean up the code while keeping tests green.
#
# Example — designing a BoundedStack via TDD:
#
# Step 1 (RED):
#   def test_bounded_stack_raises_when_full():
#       s = Stack(capacity=2)
#       s.push(1); s.push(2)
#       with pytest.raises(StackError):
#           s.push(3)     # Stack.push doesn't check capacity yet → test FAILS
#
# Step 2 (GREEN):
#   Add capacity check to Stack.push → test passes.
#
# Step 3 (REFACTOR):
#   Extract the check into _check_capacity(), add docstring → tests still pass.


# ===========================================================================
# 6. pytest-cov (run from command line)
# ===========================================================================
# Install: pip install pytest-cov
# Run:     pytest --cov=. --cov-report=term-missing
# Output shows which lines are NOT covered by tests.


# ===========================================================================
# 7. hypothesis — property-based testing
# ===========================================================================

def demo_hypothesis_concepts() -> None:
    """
    Hypothesis generates random inputs and checks invariants.

    Example usage in a test file:

        from hypothesis import given, strategies as st

        @given(st.lists(st.integers()))
        def test_sort_length_preserved(lst: list[int]) -> None:
            assert len(sorted(lst)) == len(lst)

        @given(st.integers(min_value=1), st.integers(min_value=1))
        def test_stack_push_pop_roundtrip(a: int, b: int) -> None:
            s = Stack()
            s.push(a)
            s.push(b)
            assert s.pop() == b
            assert s.pop() == a
    """
    print("Hypothesis: property-based testing — see tests/ for examples.")


# ===========================================================================
# Main demo
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 19 — Testing, Pytest & TDD")
    print("=" * 60)

    print("\n--- Stack behaviour ---")
    s: Stack = Stack(capacity=3)
    s.push("a")
    s.push("b")
    s.push("c")
    print(f"Size: {len(s)}, peek: {s.peek()}")
    print(f"Pop: {s.pop()}, size now: {len(s)}")
    try:
        s.push("d")
        s.push("e")   # should raise
    except StackError as e:
        print(f"Caught StackError: {e}")

    print("\n--- Mock demo ---")
    demo_mock()

    print("\n--- Hypothesis ---")
    demo_hypothesis_concepts()

    print("\nSee tests/test_day19.py for full pytest examples.")
