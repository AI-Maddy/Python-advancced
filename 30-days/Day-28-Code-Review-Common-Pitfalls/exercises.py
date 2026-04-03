"""
Day 28 — Exercises: Fix the Buggy Code
========================================
Each TODO marks a piece of code that contains one of the pitfalls from lesson.py.
Fix the bug without changing the function signature.
"""
from __future__ import annotations

from typing import Any


# ---------------------------------------------------------------------------
# Exercise 1 — Fix mutable default argument
# ---------------------------------------------------------------------------

def collect_BAD(item: str, bucket: list[str] = []) -> list[str]:  # noqa: B006
    """BUGGY: mutable default. Fix it."""
    bucket.append(item)
    return bucket


# TODO: Fix collect_BAD → collect_FIXED

def collect_FIXED(item: str, bucket: list[str] | None = None) -> list[str]:
    """TODO: fix the mutable default."""
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


# ---------------------------------------------------------------------------
# Exercise 2 — Fix late binding closure
# ---------------------------------------------------------------------------

def make_multipliers_BAD(n: int) -> list:
    """BUGGY: all multipliers multiply by n-1 (last loop value)."""
    return [lambda x: x * i for i in range(n)]


# TODO: Fix make_multipliers so multipliers[0](5) == 0, multipliers[2](5) == 10, etc.

def make_multipliers_FIXED(n: int) -> list:
    """TODO: fix late binding."""
    return [lambda x, i=i: x * i for i in range(n)]


# ---------------------------------------------------------------------------
# Exercise 3 — Fix `is` vs `==`
# ---------------------------------------------------------------------------

def is_greeting_BAD(s: str) -> bool:
    """BUGGY: uses `is` instead of `==`."""
    return s is "hello"  # type: ignore[comparison-overlap]  # noqa: F632


def is_greeting_FIXED(s: str) -> bool:
    """TODO: fix identity comparison."""
    return s == "hello"


# ---------------------------------------------------------------------------
# Exercise 4 — Fix bare except
# ---------------------------------------------------------------------------

def safe_divide_BAD(a: float, b: float) -> float | str:
    """BUGGY: catches everything including KeyboardInterrupt."""
    try:
        return a / b
    except:
        return "error"


def safe_divide_FIXED(a: float, b: float) -> float | str:
    """TODO: catch only ZeroDivisionError."""
    try:
        return a / b
    except ZeroDivisionError:
        return "error"


# ---------------------------------------------------------------------------
# Exercise 5 — Fix list modification during iteration
# ---------------------------------------------------------------------------

def remove_negatives_BAD(numbers: list[int]) -> list[int]:
    """BUGGY: modifies list during iteration — skips elements."""
    for n in numbers:
        if n < 0:
            numbers.remove(n)
    return numbers


def remove_negatives_FIXED(numbers: list[int]) -> list[int]:
    """TODO: correctly remove all negative numbers."""
    return [n for n in numbers if n >= 0]


# ---------------------------------------------------------------------------
# Exercise 6 — Fix missing super().__init__()
# ---------------------------------------------------------------------------

class Animal:
    def __init__(self, name: str) -> None:
        self.name = name


class Domestic:
    def __init__(self, owner: str) -> None:
        self.owner = owner


class Dog_BAD(Animal, Domestic):
    def __init__(self, name: str, owner: str) -> None:
        Animal.__init__(self, name)   # skips Domestic — MRO not respected
        # Domestic.__init__ never called → self.owner missing


class Dog_FIXED(Animal, Domestic):
    def __init__(self, name: str, owner: str) -> None:
        # TODO: use super() and MRO properly
        # Hint: you need to call both Animal.__init__ and Domestic.__init__
        # with super() this requires cooperative multiple inheritance
        # For simplicity here, call each directly or use super() chain.
        Animal.__init__(self, name)
        Domestic.__init__(self, owner)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Exercise 1
    print("Collect fixed:", collect_FIXED("a"), collect_FIXED("b"))

    # Exercise 2
    mults = make_multipliers_FIXED(5)
    print("Multipliers:", [f(10) for f in mults])  # should be [0, 10, 20, 30, 40]

    # Exercise 3
    print("Is greeting:", is_greeting_FIXED("hello"), is_greeting_FIXED("world"))

    # Exercise 4
    print("Divide:", safe_divide_FIXED(10, 2), safe_divide_FIXED(10, 0))

    # Exercise 5
    nums = [1, -2, 3, -4, 5, -6]
    print("No negatives:", remove_negatives_FIXED(nums))

    # Exercise 6
    dog = Dog_FIXED("Rex", "Alice")
    print("Dog:", dog.name, dog.owner)
