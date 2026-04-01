"""Tests for the Strategy Pattern implementation."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from strategy_pattern import (
    BubbleSortStrategy,
    MergeSortStrategy,
    QuickSortStrategy,
    SortStrategy,
    Sorter,
)


DATASETS: list[list[int]] = [
    [],
    [1],
    [3, 1, 2],
    [5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5],
    [64, 34, 25, 12, 22, 11, 90],
    [1, 1, 1, 1],
]


@pytest.mark.parametrize("StratClass", [BubbleSortStrategy, QuickSortStrategy, MergeSortStrategy])
@pytest.mark.parametrize("data", DATASETS)
def test_strategy_sorts_correctly(StratClass: type[SortStrategy], data: list[int]) -> None:
    strat = StratClass()
    assert strat.sort(data) == sorted(data)


@pytest.mark.parametrize("StratClass", [BubbleSortStrategy, QuickSortStrategy, MergeSortStrategy])
def test_strategy_does_not_mutate_input(StratClass: type[SortStrategy]) -> None:
    original = [3, 1, 4, 1, 5]
    copy = list(original)
    StratClass().sort(original)
    assert original == copy


class TestSorterContext:
    def test_delegates_to_strategy(self) -> None:
        sorter = Sorter(strategy=BubbleSortStrategy())
        assert sorter.sort([3, 2, 1]) == [1, 2, 3]

    def test_strategy_swap_at_runtime(self) -> None:
        sorter = Sorter(strategy=BubbleSortStrategy())
        data = [5, 2, 8, 1]
        r1 = sorter.sort(data)
        sorter.set_strategy(MergeSortStrategy())
        r2 = sorter.sort(data)
        assert r1 == r2 == sorted(data)

    def test_abc_not_instantiable(self) -> None:
        with pytest.raises(TypeError):
            SortStrategy()  # type: ignore[abstract]

    def test_interface_contract(self) -> None:
        for StratClass in (BubbleSortStrategy, QuickSortStrategy, MergeSortStrategy):
            strat = StratClass()
            assert isinstance(strat, SortStrategy)
            result = strat.sort([3, 1, 2])
            assert isinstance(result, list)
