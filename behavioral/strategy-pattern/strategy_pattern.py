"""Strategy Pattern — swaps algorithms at runtime behind a common interface.

The Strategy pattern defines a family of algorithms, encapsulates each one,
and makes them interchangeable.  The strategy lets the algorithm vary
independently from the clients that use it.

Python-specific notes:
- ABCs provide the interface contract.
- Because Python functions are first-class, a strategy can also be a plain
  callable; the class-based approach shown here is preferred when strategies
  need configuration state.
- ``dataclass`` is used for strategies that hold parameters.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Abstract strategy
# ---------------------------------------------------------------------------

class SortStrategy(ABC):
    """Abstract base class for all sort strategies."""

    @abstractmethod
    def sort(self, data: list[Any]) -> list[Any]:
        """Return a new sorted list from *data*.

        Args:
            data: The input sequence to sort.

        Returns:
            A new list containing the same elements in sorted order.
        """


# ---------------------------------------------------------------------------
# Concrete strategies
# ---------------------------------------------------------------------------

class BubbleSortStrategy(SortStrategy):
    """O(n²) bubble sort — useful for tiny nearly-sorted lists."""

    def sort(self, data: list[Any]) -> list[Any]:
        """Sort *data* using the bubble-sort algorithm."""
        arr = list(data)
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class QuickSortStrategy(SortStrategy):
    """O(n log n) average quicksort — good general-purpose strategy."""

    def sort(self, data: list[Any]) -> list[Any]:
        """Sort *data* using the quicksort algorithm."""
        arr = list(data)
        self._quick(arr, 0, len(arr) - 1)
        return arr

    def _quick(self, arr: list[Any], lo: int, hi: int) -> None:
        if lo < hi:
            p = self._partition(arr, lo, hi)
            self._quick(arr, lo, p - 1)
            self._quick(arr, p + 1, hi)

    @staticmethod
    def _partition(arr: list[Any], lo: int, hi: int) -> int:
        pivot = arr[hi]
        i = lo - 1
        for j in range(lo, hi):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        return i + 1


class MergeSortStrategy(SortStrategy):
    """O(n log n) merge sort — stable and suitable for linked structures."""

    def sort(self, data: list[Any]) -> list[Any]:
        """Sort *data* using the merge-sort algorithm."""
        arr = list(data)
        return self._merge_sort(arr)

    def _merge_sort(self, arr: list[Any]) -> list[Any]:
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])
        return self._merge(left, right)

    @staticmethod
    def _merge(left: list[Any], right: list[Any]) -> list[Any]:
        result: list[Any] = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------

@dataclass
class Sorter:
    """Context that delegates sorting to an interchangeable ``SortStrategy``.

    Attributes:
        strategy: The current sorting strategy.
    """
    strategy: SortStrategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        """Replace the current strategy at runtime.

        Args:
            strategy: New strategy to use on the next call to ``sort``.
        """
        self.strategy = strategy

    def sort(self, data: list[Any]) -> list[Any]:
        """Sort *data* using the configured strategy.

        Args:
            data: Input list to sort.

        Returns:
            Sorted list.
        """
        return self.strategy.sort(data)


# ---------------------------------------------------------------------------
# Client demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """Compare three sort strategies on the same dataset."""
    data = [64, 34, 25, 12, 22, 11, 90]

    sorter = Sorter(strategy=BubbleSortStrategy())
    print("Bubble:", sorter.sort(data))

    sorter.set_strategy(QuickSortStrategy())
    print("Quick: ", sorter.sort(data))

    sorter.set_strategy(MergeSortStrategy())
    print("Merge: ", sorter.sort(data))

    # All strategies should produce the same result
    assert (
        sorter.sort(data)
        == BubbleSortStrategy().sort(data)
        == QuickSortStrategy().sort(data)
    )
    print("All strategies agree ✓")


if __name__ == "__main__":
    main()
