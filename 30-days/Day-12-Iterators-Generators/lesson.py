"""
Day 12 — Iterators and Generators
===================================

Topics:
  - __iter__ / __next__ protocol
  - Generator functions (yield)
  - Generator expressions
  - yield from for delegation
  - itertools module
  - Infinite sequences, lazy pipelines
  - send() and coroutine-style generators
"""
from __future__ import annotations

import itertools
from typing import Iterator, Generator


# ---------------------------------------------------------------------------
# 1. Iterator Protocol
# ---------------------------------------------------------------------------

class Countdown:
    """Class-based iterator: __iter__ + __next__."""

    def __init__(self, start: int) -> None:
        self._current = start

    def __iter__(self) -> "Countdown":
        return self   # the object itself is the iterator

    def __next__(self) -> int:
        if self._current < 0:
            raise StopIteration
        val = self._current
        self._current -= 1
        return val


# ---------------------------------------------------------------------------
# 2. Generator Functions (yield)
# ---------------------------------------------------------------------------

def count_up(start: int, stop: int) -> Generator[int, None, None]:
    """Generator: lazily yields values from start to stop."""
    current = start
    while current <= stop:
        yield current
        current += 1


def infinite_counter(start: int = 0) -> Generator[int, None, None]:
    """Infinite generator — use with islice or break."""
    n = start
    while True:
        yield n
        n += 1


# ---------------------------------------------------------------------------
# 3. yield from — Delegation
# ---------------------------------------------------------------------------

def flatten(nested: list[object]) -> Generator[object, None, None]:
    """Recursively flatten a nested list using yield from."""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


# ---------------------------------------------------------------------------
# 4. itertools
# ---------------------------------------------------------------------------

def demo_itertools() -> None:
    # chain: concatenate iterables
    combined = list(itertools.chain([1, 2], [3, 4], [5]))
    print(f"chain: {combined}")

    # islice: lazy slice of iterator
    first_5 = list(itertools.islice(infinite_counter(), 5))
    print(f"islice: {first_5}")

    # count: infinite counter
    naturals = itertools.islice(itertools.count(1), 5)
    print(f"count: {list(naturals)}")

    # cycle: repeat sequence indefinitely
    cycled = list(itertools.islice(itertools.cycle("ABC"), 7))
    print(f"cycle: {cycled}")

    # groupby: group consecutive elements
    data = [("a", 1), ("a", 2), ("b", 3), ("b", 4), ("a", 5)]
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        print(f"  group {key}: {list(group)}")

    # product: cartesian product
    combos = list(itertools.product("AB", [1, 2]))
    print(f"product: {combos}")

    # accumulate
    import operator
    running_sum = list(itertools.accumulate([1, 2, 3, 4, 5]))
    running_prod = list(itertools.accumulate([1, 2, 3, 4, 5], operator.mul))
    print(f"accumulate sum: {running_sum}")
    print(f"accumulate prod: {running_prod}")


# ---------------------------------------------------------------------------
# 5. Lazy Pipeline
# ---------------------------------------------------------------------------

def lazy_pipeline_demo() -> None:
    """Show lazy evaluation — no intermediate lists."""
    # Process a million items without loading all into memory
    def is_even(n: int) -> bool:
        return n % 2 == 0

    # ALL of these are lazy — nothing computed yet:
    nums = itertools.count(0)              # infinite counter
    evens = filter(is_even, nums)          # filter is lazy
    squares = map(lambda x: x*x, evens)   # map is lazy
    first10 = itertools.islice(squares, 10)

    # Only computed here:
    print(list(first10))
    # [0, 4, 16, 36, 64, 100, 144, 196, 256, 324]


# ---------------------------------------------------------------------------
# 6. send() — Coroutine-style Generators
# ---------------------------------------------------------------------------

def accumulator() -> Generator[float, float, str]:
    """Generator that accepts values via send() and yields running total."""
    total: float = 0.0
    while True:
        value = yield total   # yield sends total OUT, receives value IN
        if value is None:
            break
        total += value
    return f"Final total: {total}"


def demo_send() -> None:
    gen = accumulator()
    next(gen)          # advance to first yield
    gen.send(10.0)     # total = 10.0
    gen.send(20.0)     # total = 30.0
    total = gen.send(5.0)   # total = 35.0
    print(f"Running total: {total}")


if __name__ == "__main__":
    print("=== Countdown Iterator ===")
    for n in Countdown(5):
        print(n, end=" ")
    print()

    print("\n=== Generator Function ===")
    for n in count_up(1, 5):
        print(n, end=" ")
    print()

    print("\n=== yield from ===")
    nested = [1, [2, 3], [4, [5, 6]]]
    print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6]

    print("\n=== itertools ===")
    demo_itertools()

    print("\n=== Lazy Pipeline ===")
    lazy_pipeline_demo()

    print("\n=== send() ===")
    demo_send()
