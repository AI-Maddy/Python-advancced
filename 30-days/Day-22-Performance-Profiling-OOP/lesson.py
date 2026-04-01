"""
Day 22 — Performance & Profiling in OOP
=========================================
Topics:
  - timeit.timeit for micro-benchmarks
  - cProfile + pstats usage
  - __slots__ memory comparison with sys.getsizeof and tracemalloc
  - functools.lru_cache performance benefit demonstration
  - Common pitfalls: attribute lookup, dynamic dispatch, list vs tuple
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


# ===========================================================================
# 1. timeit — micro-benchmarks
# ===========================================================================

def demo_timeit() -> None:
    """Compare list concatenation vs list.append."""

    def concat() -> list[int]:
        result: list[int] = []
        for i in range(1000):
            result = result + [i]   # O(n^2) — bad!
        return result

    def append() -> list[int]:
        result: list[int] = []
        for i in range(1000):
            result.append(i)        # O(n) — good
        return result

    # timeit returns seconds for `number` repetitions
    t_concat = timeit.timeit(concat, number=100)
    t_append = timeit.timeit(append, number=100)

    print(f"concat: {t_concat:.4f}s ({100} reps)")
    print(f"append: {t_append:.4f}s ({100} reps)")
    print(f"append is {t_concat / t_append:.1f}x faster")


# ===========================================================================
# 2. cProfile + pstats
# ===========================================================================

def _slow_computation(n: int) -> int:
    """Example: naive Fibonacci to profile."""
    if n < 2:
        return n
    return _slow_computation(n - 1) + _slow_computation(n - 2)


def profile_function() -> None:
    """Run cProfile on _slow_computation and print top 5 lines."""
    pr = cProfile.Profile()
    pr.enable()
    _slow_computation(25)
    pr.disable()

    # Capture stats to string
    buf = io.StringIO()
    ps = pstats.Stats(pr, stream=buf)
    ps.sort_stats("cumulative")
    ps.print_stats(5)          # top 5 functions by cumulative time
    print(buf.getvalue())


# ===========================================================================
# 3. __slots__ — memory comparison
# ===========================================================================

class RegularPoint:
    """Point without __slots__ — uses a __dict__ per instance."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class SlottedPoint:
    """Point with __slots__ — no __dict__, smaller footprint."""
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


def compare_memory() -> None:
    """Compare per-instance memory of slotted vs regular class."""
    n = 100_000

    # tracemalloc approach
    tracemalloc.start()

    regular_pts = [RegularPoint(float(i), float(i)) for i in range(n)]
    snapshot1 = tracemalloc.take_snapshot()

    slotted_pts = [SlottedPoint(float(i), float(i)) for i in range(n)]
    snapshot2 = tracemalloc.take_snapshot()

    tracemalloc.stop()

    # getsizeof for a single instance
    r = RegularPoint(1.0, 2.0)
    s = SlottedPoint(1.0, 2.0)
    print(f"sys.getsizeof(RegularPoint): {sys.getsizeof(r)} bytes")
    print(f"sys.getsizeof(SlottedPoint): {sys.getsizeof(s)} bytes")
    print(f"RegularPoint has __dict__: {hasattr(r, '__dict__')}")
    print(f"SlottedPoint has __dict__: {hasattr(s, '__dict__')}")

    # tracemalloc diff
    top_stats = snapshot2.compare_to(snapshot1, "lineno")
    print(f"\ntracemalloc: top allocations after creating {n} SlottedPoints:")
    for stat in top_stats[:3]:
        print(f"  {stat}")


# ===========================================================================
# 4. lru_cache performance benefit
# ===========================================================================

def fib_naive(n: int) -> int:
    """Naive recursive Fibonacci — exponential time."""
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@functools.lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    """Memoised Fibonacci — linear time after warm-up."""
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


def demo_lru_speedup() -> None:
    """Show drastic speedup from caching."""
    N = 32

    fib_cached.cache_clear()

    t_naive  = timeit.timeit(lambda: fib_naive(N),  number=3)
    t_cached = timeit.timeit(lambda: fib_cached(N), number=3)

    print(f"fib_naive({N}):  {t_naive:.4f}s  (3 reps)")
    print(f"fib_cached({N}): {t_cached:.6f}s (3 reps)")
    print(f"Speedup: {t_naive / max(t_cached, 1e-9):.0f}x")


# ===========================================================================
# 5. Common pitfalls
# ===========================================================================

def pitfall_attribute_lookup() -> None:
    """
    Repeatedly looking up the same attribute in a tight loop is slower than
    caching it in a local variable.
    """
    class Counter:
        def __init__(self) -> None:
            self.value = 0

        def slow_increment(self, n: int) -> None:
            for _ in range(n):
                self.value += 1          # attribute lookup on each iteration

        def fast_increment(self, n: int) -> None:
            val = self.value             # cache locally
            for _ in range(n):
                val += 1
            self.value = val             # single write-back

    c = Counter()
    N = 500_000
    t_slow = timeit.timeit(lambda: c.slow_increment(N), number=3)
    t_fast = timeit.timeit(lambda: c.fast_increment(N), number=3)
    print(f"slow_increment: {t_slow:.4f}s")
    print(f"fast_increment: {t_fast:.4f}s")


def pitfall_list_vs_tuple() -> None:
    """
    Tuples are slightly faster to create and iterate than lists,
    especially for read-only data.
    """
    t_list  = timeit.timeit("[1, 2, 3, 4, 5]", number=1_000_000)
    t_tuple = timeit.timeit("(1, 2, 3, 4, 5)", number=1_000_000)
    print(f"list  literal: {t_list:.4f}s")
    print(f"tuple literal: {t_tuple:.4f}s")


def pitfall_dynamic_dispatch() -> None:
    """
    Calling methods through a Protocol/ABC adds a small overhead vs direct call.
    Usually negligible, but matters in very tight loops.
    """
    class Adder:
        def add(self, a: int, b: int) -> int:
            return a + b

    adder = Adder()
    bound = adder.add   # cache the bound method

    t_attr   = timeit.timeit(lambda: adder.add(1, 2), number=1_000_000)
    t_cached = timeit.timeit(lambda: bound(1, 2),     number=1_000_000)
    print(f"adder.add (lookup each time): {t_attr:.4f}s")
    print(f"bound method (cached):        {t_cached:.4f}s")


# ===========================================================================
# Main demo
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 22 — Performance & Profiling in OOP")
    print("=" * 60)

    print("\n--- timeit: list concat vs append ---")
    demo_timeit()

    print("\n--- cProfile of naive Fibonacci ---")
    profile_function()

    print("\n--- __slots__ memory comparison ---")
    compare_memory()

    print("\n--- lru_cache speedup ---")
    demo_lru_speedup()

    print("\n--- Pitfall: attribute lookup ---")
    pitfall_attribute_lookup()

    print("\n--- Pitfall: list vs tuple ---")
    pitfall_list_vs_tuple()

    print("\n--- Pitfall: dynamic dispatch ---")
    pitfall_dynamic_dispatch()
