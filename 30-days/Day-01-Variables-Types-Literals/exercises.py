"""
Day 01 — Exercises: Variables, Types, and Literals
"""
from __future__ import annotations


# ---------------------------------------------------------------------------
# Exercise 1: Type Coercion and Conversion
# ---------------------------------------------------------------------------
# Python does not silently coerce types (unlike C++ which widens int → double).
# Write `safe_divide(a, b)` that returns a float, handles division by zero
# by returning None, and accepts both int and float inputs.

def safe_divide(a: int | float, b: int | float) -> float | None:
    """Divide a by b; return None if b is zero.

    Examples:
        >>> safe_divide(10, 4)
        2.5
        >>> safe_divide(7, 0) is None
        True
        >>> safe_divide(1, 3)  # doctest: +ELLIPSIS
        0.333...
    """
    if b == 0:
        return None
    return float(a) / float(b)


# ---------------------------------------------------------------------------
# Exercise 2: f-string Formatting Table
# ---------------------------------------------------------------------------
# Write `format_table(data)` that takes a list of (name: str, score: int)
# tuples and returns a formatted table string:
#
#   Name            Score
#   ---------------------
#   Alice              95
#   Bob                87
#   Charlie            73
#
# Requirements:
#   - Name column: 15 characters wide, left-aligned
#   - Score column: 6 characters wide, right-aligned
#   - Header underline: 21 dashes

def format_table(data: list[tuple[str, int]]) -> str:
    """Return a formatted score table string."""
    lines: list[str] = []
    lines.append(f"{'Name':<15}{'Score':>6}")
    lines.append("-" * 21)
    for name, score in data:
        lines.append(f"{name:<15}{score:>6}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Exercise 3: Type Checking with isinstance
# ---------------------------------------------------------------------------
# Write `classify(value)` that returns a string describing the value's category:
#   "boolean"     — if value is bool (check BEFORE int, since bool IS-A int)
#   "integer"     — if value is int (but not bool)
#   "float"       — if value is float
#   "complex"     — if value is complex
#   "text"        — if value is str
#   "bytes"       — if value is bytes
#   "none"        — if value is None
#   "other"       — everything else

def classify(value: object) -> str:
    """Return a string category for value's type."""
    if value is None:
        return "none"
    if isinstance(value, bool):      # before int!
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "float"
    if isinstance(value, complex):
        return "complex"
    if isinstance(value, str):
        return "text"
    if isinstance(value, bytes):
        return "bytes"
    return "other"


# ---------------------------------------------------------------------------
# Exercise 4: None Sentinel Pattern
# ---------------------------------------------------------------------------
# In C++, -1 or 0 are often used as "no value" sentinels (error-prone).
# Python uses None (or Optional[T]) for this purpose.
#
# Write `find_first(lst, predicate)` that returns the first element satisfying
# predicate, or None if none is found.
# Then write `describe_result(result)` that handles None correctly using `is`.

from typing import Callable, TypeVar

T = TypeVar("T")


def find_first(lst: list[T], predicate: Callable[[T], bool]) -> T | None:
    """Return first element where predicate is True, or None."""
    for item in lst:
        if predicate(item):
            return item
    return None


def describe_result(result: object) -> str:
    """Return 'found: <value>' or 'not found' using is-None check."""
    if result is None:
        return "not found"
    return f"found: {result}"


# ---------------------------------------------------------------------------
# Exercise 5: Arbitrary Precision Integers
# ---------------------------------------------------------------------------
# C++ int overflows silently; Python int has arbitrary precision.
# Write `factorial(n)` without using math.factorial.
# Verify that factorial(100) has 158 digits.

def factorial(n: int) -> int:
    """Return n! using iteration (no math.factorial).

    Raises:
        ValueError: if n is negative.
    """
    if n < 0:
        raise ValueError(f"factorial not defined for negative numbers: {n}")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    print(safe_divide(10, 4))
    print(safe_divide(7, 0))

    data = [("Alice", 95), ("Bob", 87), ("Charlie", 73)]
    print(format_table(data))

    for val in [True, 42, 3.14, 1 + 2j, "hi", b"bytes", None, [1, 2]]:
        print(f"{val!r:20} → {classify(val)}")

    nums = [1, 5, 3, 8, 2]
    print(find_first(nums, lambda x: x > 4))
    print(find_first(nums, lambda x: x > 100))

    f100 = factorial(100)
    print(f"factorial(100) has {len(str(f100))} digits")
