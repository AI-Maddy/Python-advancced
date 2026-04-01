"""
Tests for Day 22 — Performance & Profiling
Run with: pytest tests/test_day22.py -v
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import functools
import math
import sys
import timeit
import tracemalloc

import pytest


# ---------------------------------------------------------------------------
# __slots__ tests
# ---------------------------------------------------------------------------

class RegularPoint:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class SlottedPoint:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


def test_slotted_has_no_dict() -> None:
    s = SlottedPoint(1.0, 2.0)
    assert not hasattr(s, "__dict__")


def test_regular_has_dict() -> None:
    r = RegularPoint(1.0, 2.0)
    assert hasattr(r, "__dict__")


def test_slotted_smaller_than_regular() -> None:
    r = RegularPoint(1.0, 2.0)
    s = SlottedPoint(1.0, 2.0)
    # __slots__ eliminates __dict__; total footprint is smaller
    assert not hasattr(s, "__dict__")
    assert hasattr(r, "__dict__")
    # total bytes including __dict__
    r_total = sys.getsizeof(r) + sys.getsizeof(r.__dict__)
    s_total = sys.getsizeof(s)
    assert s_total < r_total


def test_slotted_prevents_new_attributes() -> None:
    s = SlottedPoint(1.0, 2.0)
    with pytest.raises(AttributeError):
        s.z = 3.0  # type: ignore[attr-defined]


def test_regular_allows_new_attributes() -> None:
    r = RegularPoint(1.0, 2.0)
    r.z = 3.0  # type: ignore[attr-defined]  # should not raise
    assert r.z == 3.0  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# lru_cache tests
# ---------------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def test_fib_correctness() -> None:
    fib.cache_clear()
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(10) == 55
    assert fib(30) == 832040


def test_fib_cache_populated() -> None:
    fib.cache_clear()
    fib(20)
    info = fib.cache_info()
    assert info.currsize > 0
    assert info.hits > 0


def test_lru_cache_speedup() -> None:
    """Cached fibonacci should be dramatically faster than naive."""
    def fib_naive(n: int) -> int:
        if n < 2:
            return n
        return fib_naive(n - 1) + fib_naive(n - 2)

    fib.cache_clear()
    N = 28
    t_naive  = timeit.timeit(lambda: fib_naive(N),  number=3)
    t_cached = timeit.timeit(lambda: fib(N),         number=3)
    assert t_naive > t_cached * 10  # at least 10x faster


# ---------------------------------------------------------------------------
# timeit sanity tests
# ---------------------------------------------------------------------------

def test_dict_lookup_faster_than_list() -> None:
    lst = list(range(1000))
    dct = {i: True for i in range(1000)}
    target = 999

    t_list = timeit.timeit(lambda: target in lst, number=5000)
    t_dict = timeit.timeit(lambda: target in dct, number=5000)
    assert t_dict < t_list


def test_append_faster_than_concat() -> None:
    def concat(n: int) -> list[int]:
        r: list[int] = []
        for i in range(n):
            r = r + [i]
        return r

    def append(n: int) -> list[int]:
        r: list[int] = []
        for i in range(n):
            r.append(i)
        return r

    t_concat = timeit.timeit(lambda: concat(200), number=50)
    t_append = timeit.timeit(lambda: append(200), number=50)
    assert t_append < t_concat


# ---------------------------------------------------------------------------
# tracemalloc test
# ---------------------------------------------------------------------------

def test_tracemalloc_detects_allocation() -> None:
    tracemalloc.start()
    lst = [i for i in range(10_000)]
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak > 0
    assert len(lst) == 10_000  # keep reference alive during measurement


# ---------------------------------------------------------------------------
# Shape area correctness
# ---------------------------------------------------------------------------

class Shape:
    def area(self) -> float:
        raise NotImplementedError


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


def test_circle_area() -> None:
    assert Circle(1).area() == pytest.approx(math.pi)
    assert Circle(5).area() == pytest.approx(25 * math.pi)


def test_rectangle_area() -> None:
    assert Rectangle(3, 4).area() == 12.0
    assert Rectangle(10, 10).area() == 100.0
