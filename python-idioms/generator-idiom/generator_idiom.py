"""
Generator Idiom.

Demonstrates:
* Generator functions (yield)
* Generator expressions
* send(), throw(), close() protocol
* yield from delegation
* Infinite sequence generators
* Pipeline composition with generators
"""
from __future__ import annotations

from typing import Generator, Iterator


# ---------------------------------------------------------------------------
# 1. Basic generator function
# ---------------------------------------------------------------------------
def fibonacci() -> Generator[int, None, None]:
    """Infinite Fibonacci sequence generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def take(n: int, it: Iterator[int]) -> list[int]:
    """Take the first n items from an iterator."""
    return [next(it) for _ in range(n)]


# ---------------------------------------------------------------------------
# 2. Finite generators with return value
# ---------------------------------------------------------------------------
def countdown(start: int) -> Generator[int, None, str]:
    """Count down from start to 1; return 'done' on completion."""
    for i in range(start, 0, -1):
        yield i
    return "done"


# ---------------------------------------------------------------------------
# 3. send() — coroutine-style generator
# ---------------------------------------------------------------------------
def accumulator() -> Generator[float, float, None]:
    """Running total coroutine.

    Each ``send(value)`` adds value to the total and yields the new total.
    """
    total: float = 0.0
    while True:
        value = yield total
        if value is None:
            break
        total += value


def running_average() -> Generator[float, float, None]:
    """Yield the running average of sent values."""
    total: float = 0.0
    count: int = 0
    while True:
        value = yield (total / count if count else 0.0)
        if value is None:
            break
        total += value
        count += 1


# ---------------------------------------------------------------------------
# 4. throw() and close()
# ---------------------------------------------------------------------------
def resilient_generator() -> Generator[int, None, None]:
    """Generator that handles ValueError via throw() and cleans up on close()."""
    i = 0
    try:
        while True:
            try:
                yield i
                i += 1
            except ValueError as e:
                print(f"  [generator] caught ValueError: {e}; resetting")
                i = 0
    except GeneratorExit:
        print("  [generator] cleaning up on close()")


# ---------------------------------------------------------------------------
# 5. yield from — delegation
# ---------------------------------------------------------------------------
def flatten(nested: list) -> Generator[object, None, None]:
    """Recursively flatten an arbitrarily nested list using yield from."""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def chain(*iterables: Iterator) -> Generator[object, None, None]:
    """Equivalent to itertools.chain using yield from."""
    for it in iterables:
        yield from it


# ---------------------------------------------------------------------------
# 6. Pipeline composition
# ---------------------------------------------------------------------------
def integers_from(start: int = 0) -> Generator[int, None, None]:
    """Infinite integer generator starting at start."""
    n = start
    while True:
        yield n
        n += 1


def filter_gen(pred, it: Iterator) -> Generator[object, None, None]:
    """Generator filter."""
    for item in it:
        if pred(item):
            yield item


def map_gen(func, it: Iterator) -> Generator[object, None, None]:
    """Generator map."""
    for item in it:
        yield func(item)


def take_gen(n: int, it: Iterator) -> Generator[object, None, None]:
    """Take first n items."""
    for _, item in zip(range(n), it):
        yield item


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Fibonacci
    fib = fibonacci()
    print("Fibonacci:", take(10, fib))

    # Countdown with StopIteration return value
    gen = countdown(5)
    nums = []
    try:
        while True:
            nums.append(next(gen))
    except StopIteration as e:
        print(f"Countdown: {nums}, return={e.value!r}")

    # send() accumulator
    acc = accumulator()
    next(acc)   # prime the coroutine
    for v in (10.0, 20.0, 5.0):
        total = acc.send(v)
        print(f"  acc.send({v}) → total={total}")

    # throw()
    rg = resilient_generator()
    print(next(rg))
    rg.throw(ValueError, "bad value")
    print(next(rg))
    rg.close()

    # yield from
    nested = [1, [2, [3, 4], 5], [6, 7]]
    print("Flattened:", list(flatten(nested)))

    # Pipeline: first 5 even squares starting from 0
    pipeline = take_gen(
        5,
        map_gen(
            lambda x: x ** 2,
            filter_gen(lambda x: x % 2 == 0, integers_from(0))
        )
    )
    print("Even squares:", list(pipeline))
