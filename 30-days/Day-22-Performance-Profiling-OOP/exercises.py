"""
Day 22 — Exercises: Performance & Profiling
============================================
Complete each TODO.
"""
from __future__ import annotations

import cProfile
import functools
import io
import pstats
import sys
import timeit
import tracemalloc
from typing import Any


# ---------------------------------------------------------------------------
# Exercise 1 — Benchmark __slots__ vs __dict__
# ---------------------------------------------------------------------------
# TODO: Create RegularPoint and SlottedPoint classes.
#       Use sys.getsizeof to compare a single instance of each.
#       Return (size_regular, size_slotted, slotted_is_smaller: bool).

class RegularPoint:
    """TODO: point with no __slots__."""
    def __init__(self, x: float, y: float) -> None:
        ...


class SlottedPoint:
    """TODO: point with __slots__ = ('x', 'y')."""
    __slots__ = ("x", "y")
    def __init__(self, x: float, y: float) -> None:
        ...


def exercise1_slots_benchmark() -> tuple[int, int, bool]:
    """Return (regular_size, slotted_size, slotted_is_smaller)."""
    # TODO
    ...
    return (0, 0, False)


# ---------------------------------------------------------------------------
# Exercise 2 — Add lru_cache to Fibonacci and measure speedup
# ---------------------------------------------------------------------------
# TODO: Implement fib_naive(n) and fib_cached(n) (with @functools.lru_cache).
#       For N=30, time 5 repetitions of each.
#       Return (naive_time_seconds, cached_time_seconds, speedup_factor).

def fib_naive(n: int) -> int:
    """TODO: naive recursive fibonacci."""
    ...
    return 0


@functools.lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    """TODO: memoised recursive fibonacci."""
    ...
    return 0


def exercise2_lru_speedup() -> tuple[float, float, float]:
    """Return (naive_time, cached_time, speedup).  speedup > 1."""
    # TODO
    ...
    return (0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# Exercise 3 — Profile a class hierarchy with cProfile
# ---------------------------------------------------------------------------
# TODO: Create a Shape hierarchy:
#   Shape (base, area() raises NotImplementedError)
#   Circle(Shape, radius): area = pi * r^2
#   Rectangle(Shape, w, h): area = w * h
#
# Profile a function that creates 10_000 Circles and 10_000 Rectangles
# and sums all areas.  Return the total area (float) and the top profile
# entry name (str) from pstats.

import math as _math

class Shape:
    """TODO: base shape."""
    def area(self) -> float:
        raise NotImplementedError


class Circle(Shape):
    """TODO: circle."""
    def __init__(self, radius: float) -> None:
        ...
    def area(self) -> float:
        ...
        return 0.0


class Rectangle(Shape):
    """TODO: rectangle."""
    def __init__(self, width: float, height: float) -> None:
        ...
    def area(self) -> float:
        ...
        return 0.0


def exercise3_profile() -> tuple[float, str]:
    """Return (total_area, top_function_name_from_profile)."""
    # TODO: profile the area computation and return results
    ...
    return (0.0, "")


# ---------------------------------------------------------------------------
# Exercise 4 — tracemalloc: measure memory of a list comprehension
# ---------------------------------------------------------------------------
# TODO: Use tracemalloc to measure peak memory of building a list of
#       100_000 integers vs a generator expression that sums them on the fly.
#       Return (list_peak_bytes, generator_sum).
#       generator_sum should equal sum(range(100_000)).

def exercise4_tracemalloc() -> tuple[int, int]:
    """Return (list_peak_bytes, generator_sum)."""
    # TODO
    ...
    return (0, 0)


# ---------------------------------------------------------------------------
# Exercise 5 — timeit: dict lookup vs list search
# ---------------------------------------------------------------------------
# TODO: Build a list of 1000 integers and a dict with the same integers as
#       keys.  Time looking up the integer 999 in each structure (10_000 reps).
#       Return (list_time, dict_time, dict_is_faster: bool).

def exercise5_dict_vs_list() -> tuple[float, float, bool]:
    """Return (list_lookup_time, dict_lookup_time, dict_is_faster)."""
    # TODO
    ...
    return (0.0, 0.0, False)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_slots_benchmark())
    print("Exercise 2:", exercise2_lru_speedup())
    print("Exercise 3:", exercise3_profile())
    print("Exercise 4:", exercise4_tracemalloc())
    print("Exercise 5:", exercise5_dict_vs_list())
