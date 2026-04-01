"""Iterator Pattern — Example 3: Filtered Iterator.

Wraps any iterator and yields only elements that satisfy a predicate — a
lazy filter built from the iterator protocol.
"""
from __future__ import annotations

from typing import Callable, Generic, Iterator, TypeVar

T = TypeVar("T")


class FilteredIterator(Generic[T]):
    """Wraps an iterable and lazily yields items matching *predicate*.

    Args:
        source:    Any iterable to filter.
        predicate: Function that returns ``True`` for items to include.
    """

    def __init__(self, source: Iterator[T], predicate: Callable[[T], bool]) -> None:
        self._source = source
        self._predicate = predicate

    def __iter__(self) -> FilteredIterator[T]:
        return self

    def __next__(self) -> T:
        while True:
            item = next(self._source)  # raises StopIteration when exhausted
            if self._predicate(item):
                return item


class TransformIterator(Generic[T]):
    """Wraps an iterable and applies a transform function lazily.

    Args:
        source:    Any iterable.
        transform: Function applied to each element.
    """

    def __init__(self, source: Iterator[T], transform: Callable[[T], T]) -> None:
        self._source = source
        self._transform = transform

    def __iter__(self) -> TransformIterator[T]:
        return self

    def __next__(self) -> T:
        return self._transform(next(self._source))


def main() -> None:
    # Filter even numbers from a range
    even_iter = FilteredIterator(iter(range(20)), lambda x: x % 2 == 0)
    print("Even numbers in 0-19:", list(even_iter))

    # Filter words longer than 4 chars
    words = ["hi", "hello", "world", "ok", "Python", "iterator"]
    long_words = FilteredIterator(iter(words), lambda w: len(w) > 4)
    print("Words > 4 chars:", list(long_words))

    # Transform: square each number
    squares = TransformIterator(iter(range(1, 6)), lambda x: x * x)  # type: ignore[type-var]
    print("Squares 1-5:", list(squares))

    # Chain filter + transform: squares of odd numbers
    odd_filter = FilteredIterator(iter(range(10)), lambda x: x % 2 != 0)
    sq_odd = TransformIterator(odd_filter, lambda x: x * x)  # type: ignore[type-var]
    print("Squares of odd 0-9:", list(sq_odd))


if __name__ == "__main__":
    main()
