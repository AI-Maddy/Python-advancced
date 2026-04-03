"""
Day 22 — Exercises: Performance & Profiling
============================================
Complete each TODO.
"""
from __future__ import annotations

import cProfile
import functools
import io
import math as _math
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
    """Point with no __slots__."""
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class SlottedPoint:
    """Point with __slots__ = ('x', 'y')."""
    __slots__ = ("x", "y")
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


def exercise1_slots_benchmark() -> tuple[int, int, bool]:
    """Return (regular_size, slotted_size, slotted_is_smaller)."""
    r = RegularPoint(1.0, 2.0)
    s = SlottedPoint(1.0, 2.0)
    r_size = sys.getsizeof(r)
    s_size = sys.getsizeof(s)
    return (r_size, s_size, s_size < r_size)


# ---------------------------------------------------------------------------
# Exercise 2 — Add lru_cache to Fibonacci and measure speedup
# ---------------------------------------------------------------------------
# TODO: Implement fib_naive(n) and fib_cached(n) (with @functools.lru_cache).
#       For N=30, time 5 repetitions of each.
#       Return (naive_time_seconds, cached_time_seconds, speedup_factor).

def fib_naive(n: int) -> int:
    """Naive recursive fibonacci."""
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@functools.lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    """Memoised recursive fibonacci."""
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


def exercise2_lru_speedup() -> tuple[float, float, float]:
    """Return (naive_time, cached_time, speedup).  speedup > 1."""
    N = 30
    reps = 5
    fib_cached.cache_clear()
    t_naive  = timeit.timeit(lambda: fib_naive(N),  number=reps)
    t_cached = timeit.timeit(lambda: fib_cached(N), number=reps)
    speedup = t_naive / max(t_cached, 1e-9)
    return (t_naive, t_cached, speedup)


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

class Shape:
    """Base shape."""
    def area(self) -> float:
        raise NotImplementedError


class Circle(Shape):
    """Circle."""
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return _math.pi * self.radius ** 2


class Rectangle(Shape):
    """Rectangle."""
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


def _sum_areas() -> float:
    shapes: list[Shape] = (
        [Circle(float(i % 10 + 1)) for i in range(10_000)]
        + [Rectangle(float(i % 5 + 1), float(i % 3 + 1)) for i in range(10_000)]
    )
    return sum(s.area() for s in shapes)


def exercise3_profile() -> tuple[float, str]:
    """Return (total_area, top_function_name_from_profile)."""
    pr = cProfile.Profile()
    pr.enable()
    total = _sum_areas()
    pr.disable()

    buf = io.StringIO()
    ps = pstats.Stats(pr, stream=buf)
    ps.sort_stats("cumulative")
    ps.print_stats(1)
    lines = [l for l in buf.getvalue().splitlines() if l.strip() and not l.startswith(" ")]
    # Extract top function name from pstats output
    top_name = ""
    for line in buf.getvalue().splitlines():
        parts = line.strip().split()
        if len(parts) >= 6 and "(" in parts[-1]:
            top_name = parts[-1]
            break

    return (total, top_name or "area")


# ---------------------------------------------------------------------------
# Exercise 4 — tracemalloc: measure memory of a list comprehension
# ---------------------------------------------------------------------------
# TODO: Use tracemalloc to measure peak memory of building a list of
#       100_000 integers vs a generator expression that sums them on the fly.
#       Return (list_peak_bytes, generator_sum).
#       generator_sum should equal sum(range(100_000)).

def exercise4_tracemalloc() -> tuple[int, int]:
    """Return (list_peak_bytes, generator_sum)."""
    tracemalloc.start()
    lst = [i for i in range(100_000)]
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    gen_sum = sum(i for i in range(100_000))
    return (peak, gen_sum)


# ---------------------------------------------------------------------------
# Exercise 5 — timeit: dict lookup vs list search
# ---------------------------------------------------------------------------
# TODO: Build a list of 1000 integers and a dict with the same integers as
#       keys.  Time looking up the integer 999 in each structure (10_000 reps).
#       Return (list_time, dict_time, dict_is_faster: bool).

def exercise5_dict_vs_list() -> tuple[float, float, bool]:
    """Return (list_lookup_time, dict_lookup_time, dict_is_faster)."""
    data_list = list(range(1000))
    data_dict = {i: True for i in range(1000)}
    target = 999
    reps = 10_000

    t_list = timeit.timeit(lambda: target in data_list, number=reps)
    t_dict = timeit.timeit(lambda: target in data_dict, number=reps)
    return (t_list, t_dict, t_dict < t_list)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_slots_benchmark())
    print("Exercise 2:", exercise2_lru_speedup())
    print("Exercise 3:", exercise3_profile())
    print("Exercise 4:", exercise4_tracemalloc())
    print("Exercise 5:", exercise5_dict_vs_list())
