"""
Tests for Day 21 — functools, operator & itertools
Run with: pytest tests/test_day21.py -v
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import itertools
import math
import operator
from collections.abc import Callable
from functools import lru_cache, partial, reduce, singledispatch, total_ordering
from typing import Any

import pytest


# ---------------------------------------------------------------------------
# compose
# ---------------------------------------------------------------------------

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return reduce(lambda f, g: lambda x: f(g(x)), funcs)


def test_compose_single() -> None:
    assert compose(str.upper)("hello") == "HELLO"


def test_compose_two() -> None:
    assert compose(str.upper, str.strip)("  hello  ") == "HELLO"


def test_compose_three() -> None:
    p = compose(str.upper, str.strip, lambda s: s.replace(",", ""))
    assert p("  hi, there  ") == "HI THERE"


def test_compose_order() -> None:
    # compose(f, g)(x) == f(g(x)), i.e. g applied first
    double = lambda x: x * 2
    add1 = lambda x: x + 1
    # compose(double, add1)(5) == double(add1(5)) == double(6) == 12
    assert compose(double, add1)(5) == 12


# ---------------------------------------------------------------------------
# reduce
# ---------------------------------------------------------------------------

def test_reduce_sum() -> None:
    assert reduce(operator.add, [1, 2, 3, 4, 5]) == 15


def test_reduce_product() -> None:
    assert reduce(operator.mul, [1, 2, 3, 4], 1) == 24


def test_reduce_initial_empty() -> None:
    assert reduce(operator.add, [], 0) == 0


# ---------------------------------------------------------------------------
# partial
# ---------------------------------------------------------------------------

def power(base: float, exp: float) -> float:
    return base ** exp


def test_partial_square() -> None:
    sq = partial(power, exp=2)
    assert sq(5) == 25


def test_partial_add() -> None:
    add10 = partial(operator.add, 10)
    assert add10(5) == 15


# ---------------------------------------------------------------------------
# lru_cache
# ---------------------------------------------------------------------------

@lru_cache(maxsize=64)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def test_lru_cache_fib_correct() -> None:
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(10) == 55
    assert fib(20) == 6765


def test_lru_cache_caches_calls() -> None:
    fib.cache_clear()
    fib(10)
    info = fib.cache_info()
    assert info.currsize > 0


# ---------------------------------------------------------------------------
# total_ordering
# ---------------------------------------------------------------------------

@total_ordering
class Weight:
    def __init__(self, kg: float) -> None:
        self.kg = kg

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Weight):
            return NotImplemented
        return self.kg == other.kg

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Weight):
            return NotImplemented
        return self.kg < other.kg

    def __hash__(self) -> int:
        return hash(self.kg)


def test_total_ordering_lt() -> None:
    assert Weight(5) < Weight(10)


def test_total_ordering_gt() -> None:
    assert Weight(10) > Weight(5)


def test_total_ordering_le() -> None:
    assert Weight(5) <= Weight(5)
    assert Weight(5) <= Weight(10)


def test_total_ordering_ge() -> None:
    assert Weight(10) >= Weight(10)


# ---------------------------------------------------------------------------
# singledispatch
# ---------------------------------------------------------------------------

@singledispatch
def describe(val: Any) -> str:
    return f"other:{type(val).__name__}"


@describe.register(int)
def _(val: int) -> str:
    return f"int:{val}"


@describe.register(str)
def _(val: str) -> str:
    return f"str:{val!r}"


def test_singledispatch_int() -> None:
    assert describe(42) == "int:42"


def test_singledispatch_str() -> None:
    assert describe("hi") == "str:'hi'"


def test_singledispatch_default() -> None:
    assert describe(3.14).startswith("other:")


# ---------------------------------------------------------------------------
# operator
# ---------------------------------------------------------------------------

def test_attrgetter() -> None:
    from dataclasses import dataclass

    @dataclass
    class P:
        x: int
        y: int

    points = [P(3, 1), P(1, 4), P(2, 2)]
    by_x = sorted(points, key=operator.attrgetter("x"))
    assert [p.x for p in by_x] == [1, 2, 3]


def test_itemgetter() -> None:
    data = [("b", 2), ("a", 1), ("c", 3)]
    by_first = sorted(data, key=operator.itemgetter(0))
    assert [t[0] for t in by_first] == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# itertools
# ---------------------------------------------------------------------------

def test_chain() -> None:
    assert list(itertools.chain([1, 2], [3], [4, 5])) == [1, 2, 3, 4, 5]


def test_islice() -> None:
    assert list(itertools.islice(itertools.count(0), 5)) == [0, 1, 2, 3, 4]


def test_accumulate() -> None:
    assert list(itertools.accumulate([1, 2, 3, 4])) == [1, 3, 6, 10]


def test_groupby() -> None:
    data = sorted(["apple", "avocado", "banana", "blueberry"], key=lambda s: s[0])
    groups = {k: list(v) for k, v in itertools.groupby(data, key=lambda s: s[0])}
    assert groups["a"] == ["apple", "avocado"]
    assert groups["b"] == ["banana", "blueberry"]


def test_takewhile() -> None:
    assert list(itertools.takewhile(lambda x: x < 5, [1, 2, 3, 7, 4])) == [1, 2, 3]


def test_dropwhile() -> None:
    assert list(itertools.dropwhile(lambda x: x < 5, [1, 2, 3, 7, 4])) == [7, 4]


def test_combinations() -> None:
    combos = list(itertools.combinations([1, 2, 3], 2))
    assert len(combos) == 3
    assert (1, 2) in combos


def test_product() -> None:
    p = list(itertools.product([1, 2], ["a", "b"]))
    assert len(p) == 4
    assert (1, "a") in p
