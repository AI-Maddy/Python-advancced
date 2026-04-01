"""
Day 22 — Solutions: Performance & Profiling
============================================
"""
from __future__ import annotations

import cProfile
import functools
import io
import math
import pstats
import sys
import timeit
import tracemalloc
from typing import Any


# ---------------------------------------------------------------------------
# Solution 1 — __slots__ benchmark
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


def exercise1_slots_benchmark() -> tuple[int, int, bool]:
    r = RegularPoint(1.0, 2.0)
    s = SlottedPoint(1.0, 2.0)
    r_size = sys.getsizeof(r)
    s_size = sys.getsizeof(s)
    return (r_size, s_size, s_size < r_size)


# ---------------------------------------------------------------------------
# Solution 2 — lru_cache speedup
# ---------------------------------------------------------------------------

def fib_naive(n: int) -> int:
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@functools.lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


def exercise2_lru_speedup() -> tuple[float, float, float]:
    N = 30
    reps = 5
    fib_cached.cache_clear()
    t_naive  = timeit.timeit(lambda: fib_naive(N),  number=reps)
    t_cached = timeit.timeit(lambda: fib_cached(N), number=reps)
    speedup = t_naive / max(t_cached, 1e-9)
    return (t_naive, t_cached, speedup)


# ---------------------------------------------------------------------------
# Solution 3 — cProfile of class hierarchy
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


def _sum_areas() -> float:
    shapes: list[Shape] = (
        [Circle(float(i % 10 + 1)) for i in range(10_000)]
        + [Rectangle(float(i % 5 + 1), float(i % 3 + 1)) for i in range(10_000)]
    )
    return sum(s.area() for s in shapes)


def exercise3_profile() -> tuple[float, str]:
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
# Solution 4 — tracemalloc
# ---------------------------------------------------------------------------

def exercise4_tracemalloc() -> tuple[int, int]:
    tracemalloc.start()
    lst = [i for i in range(100_000)]
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    gen_sum = sum(i for i in range(100_000))
    return (peak, gen_sum)


# ---------------------------------------------------------------------------
# Solution 5 — dict vs list lookup
# ---------------------------------------------------------------------------

def exercise5_dict_vs_list() -> tuple[float, float, bool]:
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
    print("Solution 1:", exercise1_slots_benchmark())
    print("Solution 2:", exercise2_lru_speedup())
    print("Solution 3:", exercise3_profile())
    print("Solution 4:", exercise4_tracemalloc())
    print("Solution 5:", exercise5_dict_vs_list())
