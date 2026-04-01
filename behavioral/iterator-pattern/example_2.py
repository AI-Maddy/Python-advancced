"""Iterator Pattern — Example 2: Range Iterator with Step.

A custom ``RangeIterator`` mimics Python's built-in ``range()`` but as an
explicit iterator class with ``__iter__`` / ``__next__``.
"""
from __future__ import annotations


class RangeIterator:
    """Iterates over [start, stop) with a given step.

    Args:
        start: First value.
        stop:  Upper bound (exclusive).
        step:  Increment per step (default 1; may be negative).
    """

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        if step == 0:
            raise ValueError("step must not be zero")
        self._current = start
        self._stop = stop
        self._step = step

    def __iter__(self) -> RangeIterator:
        return self

    def __next__(self) -> int:
        if self._step > 0 and self._current >= self._stop:
            raise StopIteration
        if self._step < 0 and self._current <= self._stop:
            raise StopIteration
        value = self._current
        self._current += self._step
        return value

    def __repr__(self) -> str:
        return (
            f"RangeIterator(current={self._current}, "
            f"stop={self._stop}, step={self._step})"
        )


class InfiniteCounter:
    """Infinite iterator that counts from *start* by *step* indefinitely.

    Use ``itertools.islice`` or a loop with a break to limit output.
    """

    def __init__(self, start: int = 0, step: int = 1) -> None:
        self._value = start
        self._step = step

    def __iter__(self) -> InfiniteCounter:
        return self

    def __next__(self) -> int:
        value = self._value
        self._value += self._step
        return value


def main() -> None:
    print("RangeIterator(0, 10, 2):", list(RangeIterator(0, 10, 2)))
    print("RangeIterator(10, 0, -3):", list(RangeIterator(10, 0, -3)))
    print("RangeIterator(5, 5):", list(RangeIterator(5, 5)))

    # Verify matches built-in range
    for start, stop, step in [(0, 10, 1), (0, 20, 3), (10, 0, -2)]:
        custom = list(RangeIterator(start, stop, step))
        builtin = list(range(start, stop, step))
        assert custom == builtin, f"Mismatch for range({start},{stop},{step})"
    print("All RangeIterator results match built-in range().")

    # Infinite counter — take first 5 even numbers
    counter = InfiniteCounter(0, 2)
    evens = [next(counter) for _ in range(5)]
    print(f"\nFirst 5 even numbers via InfiniteCounter: {evens}")

    # Bad step
    try:
        RangeIterator(0, 10, 0)
    except ValueError as e:
        print(f"\nCaught expected error: {e}")


if __name__ == "__main__":
    main()
