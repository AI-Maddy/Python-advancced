"""
Day 21 — Exercises: functools, operator & itertools
=====================================================
Complete each TODO.
"""
from __future__ import annotations

import functools
import itertools
import operator
from collections.abc import Callable, Iterable
from functools import reduce, singledispatch, total_ordering
from typing import Any, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Exercise 1 — implement compose()
# ---------------------------------------------------------------------------
# TODO: Implement compose(*funcs) using functools.reduce.
#       compose(f, g)(x) == f(g(x))  (right-to-left application)
#       compose(str.upper, str.strip)("  hello  ") → "HELLO"

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Return a right-to-left function composition pipeline."""
    return reduce(lambda f, g: lambda x: f(g(x)), funcs)


def exercise1_compose() -> str:
    """Should return 'HELLO'."""
    pipeline = compose(str.upper, str.strip)
    return pipeline("  hello  ")


# ---------------------------------------------------------------------------
# Exercise 2 — pipeline with islice + filter
# ---------------------------------------------------------------------------
# TODO: Given an infinite counter starting at 1 (itertools.count(1)),
#       take the first 20 values, filter for even numbers, then collect.
#       Result: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

def exercise2_islice_filter() -> list[int]:
    """Return even numbers from the first 20 natural numbers."""
    first_20 = itertools.islice(itertools.count(1), 20)
    return list(filter(lambda x: x % 2 == 0, first_20))


# ---------------------------------------------------------------------------
# Exercise 3 — accumulate running totals
# ---------------------------------------------------------------------------
# TODO: Given daily_sales = [120, 85, 200, 155, 90, 310, 75],
#       return a list of (day, cumulative_total) tuples.
#       E.g. [(1, 120), (2, 205), ...]

def exercise3_accumulate() -> list[tuple[int, int]]:
    """Return list of (day_number, running_total) tuples."""
    daily_sales = [120, 85, 200, 155, 90, 310, 75]
    running = itertools.accumulate(daily_sales)
    return [(day, total) for day, total in enumerate(running, start=1)]


# ---------------------------------------------------------------------------
# Exercise 4 — groupby on dicts
# ---------------------------------------------------------------------------
# TODO: Group the employees list below by 'department'.
#       Return a dict: {dept: [list of employee names]}.
#       HINT: sort by department first, then use itertools.groupby.

def exercise4_groupby() -> dict[str, list[str]]:
    """Return {'Engineering': ['Alice', 'Carol'], 'Marketing': ['Bob', 'Dave']}."""
    employees = [
        {"name": "Alice", "department": "Engineering"},
        {"name": "Bob",   "department": "Marketing"},
        {"name": "Carol", "department": "Engineering"},
        {"name": "Dave",  "department": "Marketing"},
    ]
    sorted_emps = sorted(employees, key=operator.itemgetter("department"))
    return {
        dept: [e["name"] for e in group]
        for dept, group in itertools.groupby(
            sorted_emps, key=operator.itemgetter("department")
        )
    }


# ---------------------------------------------------------------------------
# Exercise 5 — singledispatch formatter
# ---------------------------------------------------------------------------
# TODO: Implement a format_value() singledispatch function:
#   - int    → "int:N" (e.g. "int:42")
#   - float  → "float:N.NN" (2 decimal places)
#   - list   → "list[N items]"
#   - str    → "str:'value'"
#   - default → "other:repr"

@singledispatch
def format_value(value: Any) -> str:
    """Default formatter."""
    return f"other:{value!r}"


@format_value.register(int)
def _(value: int) -> str:
    return f"int:{value}"


@format_value.register(float)
def _(value: float) -> str:
    return f"float:{value:.2f}"


@format_value.register(list)
def _(value: list[Any]) -> str:
    return f"list[{len(value)} items]"


@format_value.register(str)
def _(value: str) -> str:
    return f"str:{value!r}"


def exercise5_dispatch() -> list[str]:
    """Return formatted strings for [42, 3.14, ['a','b'], 'hi', None]."""
    return [format_value(v) for v in (42, 3.14, ["a", "b"], "hi", None)]


# ---------------------------------------------------------------------------
# Exercise 6 — total_ordering for a Card class
# ---------------------------------------------------------------------------
# TODO: Implement a Card class using @total_ordering.
#       Card has suit (str) and rank (int, 2–14 where 14 = Ace).
#       Compare by rank only.  Only implement __eq__ and __lt__.
#       Then verify Card(14, "♠") > Card(2, "♥").

@total_ordering
class Card:
    """Playing card comparable by rank."""

    def __init__(self, rank: int, suit: str) -> None:
        self.rank = rank
        self.suit = suit

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank < other.rank

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))

    def __repr__(self) -> str:
        return f"Card({self.rank}, {self.suit!r})"


def exercise6_total_ordering() -> tuple[bool, bool, bool]:
    """Return (ace_gt_two, two_lt_king, ace_gte_ace)."""
    ace  = Card(14, "♠")
    two  = Card(2, "♥")
    king = Card(13, "♣")
    ace2 = Card(14, "♦")
    return (ace > two, two < king, ace >= ace2)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_compose())
    print("Exercise 2:", exercise2_islice_filter())
    print("Exercise 3:", exercise3_accumulate())
    print("Exercise 4:", exercise4_groupby())
    print("Exercise 5:", exercise5_dispatch())
    print("Exercise 6:", exercise6_total_ordering())
