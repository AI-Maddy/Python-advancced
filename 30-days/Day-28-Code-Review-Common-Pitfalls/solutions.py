"""
Day 28 — Solutions: Common Python Pitfalls
===========================================
"""
from __future__ import annotations

import functools
from typing import Any


# ---------------------------------------------------------------------------
# Solution 1 — Mutable default argument
# ---------------------------------------------------------------------------

def collect_FIXED(item: str, bucket: list[str] | None = None) -> list[str]:
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


# ---------------------------------------------------------------------------
# Solution 2 — Late binding closure
# ---------------------------------------------------------------------------

def make_multipliers_FIXED(n: int) -> list:
    return [lambda x, i=i: x * i for i in range(n)]


# ---------------------------------------------------------------------------
# Solution 3 — is vs ==
# ---------------------------------------------------------------------------

def is_greeting_FIXED(s: str) -> bool:
    return s == "hello"


# ---------------------------------------------------------------------------
# Solution 4 — Bare except
# ---------------------------------------------------------------------------

def safe_divide_FIXED(a: float, b: float) -> float | str:
    try:
        return a / b
    except ZeroDivisionError:
        return "error"


# ---------------------------------------------------------------------------
# Solution 5 — Modify list during iteration
# ---------------------------------------------------------------------------

def remove_negatives_FIXED(numbers: list[int]) -> list[int]:
    return [n for n in numbers if n >= 0]


# ---------------------------------------------------------------------------
# Solution 6 — Missing super().__init__()
# ---------------------------------------------------------------------------

class Animal:
    def __init__(self, name: str, **kwargs: Any) -> None:
        self.name = name
        super().__init__(**kwargs)


class Domestic:
    def __init__(self, owner: str, **kwargs: Any) -> None:
        self.owner = owner
        super().__init__(**kwargs)


class Dog_FIXED(Animal, Domestic):
    def __init__(self, name: str, owner: str) -> None:
        super().__init__(name=name, owner=owner)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Collect fixed:", collect_FIXED("a"), collect_FIXED("b"))

    mults = make_multipliers_FIXED(5)
    print("Multipliers:", [f(10) for f in mults])

    print("Is greeting:", is_greeting_FIXED("hello"), is_greeting_FIXED("world"))
    print("Divide:", safe_divide_FIXED(10, 2), safe_divide_FIXED(10, 0))

    nums = [1, -2, 3, -4, 5, -6]
    print("No negatives:", remove_negatives_FIXED(nums))

    dog = Dog_FIXED("Rex", "Alice")
    print(f"Dog: {dog.name}, owner: {dog.owner}")
