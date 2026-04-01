"""
Day 21 — Solutions: functools, operator & itertools
=====================================================
"""
from __future__ import annotations

import functools
import itertools
import operator
from collections.abc import Callable
from functools import reduce, singledispatch, total_ordering
from typing import Any, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Solution 1 — compose
# ---------------------------------------------------------------------------

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Right-to-left function composition."""
    return reduce(lambda f, g: lambda x: f(g(x)), funcs)


def exercise1_compose() -> str:
    pipeline = compose(str.upper, str.strip)
    return pipeline("  hello  ")


# ---------------------------------------------------------------------------
# Solution 2 — islice + filter
# ---------------------------------------------------------------------------

def exercise2_islice_filter() -> list[int]:
    first_20 = itertools.islice(itertools.count(1), 20)
    return list(filter(lambda x: x % 2 == 0, first_20))


# ---------------------------------------------------------------------------
# Solution 3 — accumulate running totals
# ---------------------------------------------------------------------------

def exercise3_accumulate() -> list[tuple[int, int]]:
    daily_sales = [120, 85, 200, 155, 90, 310, 75]
    running = itertools.accumulate(daily_sales)
    return [(day, total) for day, total in enumerate(running, start=1)]


# ---------------------------------------------------------------------------
# Solution 4 — groupby on dicts
# ---------------------------------------------------------------------------

def exercise4_groupby() -> dict[str, list[str]]:
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
# Solution 5 — singledispatch formatter
# ---------------------------------------------------------------------------

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
    return [format_value(v) for v in (42, 3.14, ["a", "b"], "hi", None)]


# ---------------------------------------------------------------------------
# Solution 6 — total_ordering Card
# ---------------------------------------------------------------------------

@total_ordering
class Card:
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
    ace  = Card(14, "♠")
    two  = Card(2, "♥")
    king = Card(13, "♣")
    ace2 = Card(14, "♦")
    return (ace > two, two < king, ace >= ace2)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Solution 1:", exercise1_compose())
    print("Solution 2:", exercise2_islice_filter())
    print("Solution 3:", exercise3_accumulate())
    print("Solution 4:", exercise4_groupby())
    print("Solution 5:", exercise5_dispatch())
    print("Solution 6:", exercise6_total_ordering())
