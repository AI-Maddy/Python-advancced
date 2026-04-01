"""
Day 01 — Solutions
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")


def safe_divide(a: int | float, b: int | float) -> float | None:
    """Divide a by b; return None if b is zero."""
    if b == 0:
        return None
    return float(a) / float(b)


def format_table(data: list[tuple[str, int]]) -> str:
    """Return a formatted score table string."""
    lines: list[str] = []
    lines.append(f"{'Name':<15}{'Score':>6}")
    lines.append("-" * 21)
    for name, score in data:
        lines.append(f"{name:<15}{score:>6}")
    return "\n".join(lines)


def classify(value: object) -> str:
    """Return a string category for value's type.

    Order matters: bool must be checked before int (bool IS-A int).
    """
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


def find_first(lst: list[T], predicate: Callable[[T], bool]) -> T | None:
    """Return first element where predicate is True, or None."""
    for item in lst:
        if predicate(item):
            return item
    return None


def describe_result(result: object) -> str:
    """Return 'found: <value>' or 'not found'."""
    if result is None:
        return "not found"
    return f"found: {result}"


def factorial(n: int) -> int:
    """Return n! iteratively."""
    if n < 0:
        raise ValueError(f"factorial not defined for negative numbers: {n}")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    print(safe_divide(10, 4))          # 2.5
    print(safe_divide(7, 0))           # None

    data = [("Alice", 95), ("Bob", 87), ("Charlie", 73)]
    print(format_table(data))

    for val in [True, 42, 3.14, 1 + 2j, "hi", b"bytes", None, [1, 2]]:
        print(f"{val!r:20} → {classify(val)}")

    nums = [1, 5, 3, 8, 2]
    r1 = find_first(nums, lambda x: x > 4)
    r2 = find_first(nums, lambda x: x > 100)
    print(describe_result(r1))          # found: 5
    print(describe_result(r2))          # not found

    f100 = factorial(100)
    print(f"factorial(100) has {len(str(f100))} digits")  # 158
