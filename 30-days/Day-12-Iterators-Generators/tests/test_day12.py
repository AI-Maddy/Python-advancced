"""Tests for Day 12 — Iterators and Generators"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)
import itertools
import pytest
from solutions import BinaryTree, fibonacci, lazy_csv_reader, NumberRange


class TestBinaryTree:
    def test_inorder(self) -> None:
        t = BinaryTree()
        for v in [5, 3, 7, 1, 4]:
            t.insert(v)
        assert list(t) == [1, 3, 4, 5, 7]

    def test_single_node(self) -> None:
        t = BinaryTree()
        t.insert(42)
        assert list(t) == [42]

    def test_empty(self) -> None:
        t = BinaryTree()
        assert list(t) == []


class TestFibonacci:
    def test_first_10(self) -> None:
        fibs = list(itertools.islice(fibonacci(), 10))
        assert fibs == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_first_element(self) -> None:
        assert next(fibonacci()) == 0

    def test_infinite(self) -> None:
        # Should not raise after many iterations
        gen = fibonacci()
        for _ in range(100):
            next(gen)


class TestLazyCSVReader:
    def test_basic(self) -> None:
        lines = ["name,age", "Alice,30", "Bob,25"]
        rows = list(lazy_csv_reader(lines))
        assert rows[0] == {"name": "Alice", "age": "30"}
        assert rows[1] == {"name": "Bob", "age": "25"}

    def test_empty(self) -> None:
        assert list(lazy_csv_reader([])) == []

    def test_headers_only(self) -> None:
        assert list(lazy_csv_reader(["a,b"])) == []

    def test_lazy(self) -> None:
        # Should yield one at a time
        lines = ["x,y", "1,2", "3,4", "5,6"]
        gen = lazy_csv_reader(lines)
        first = next(gen)
        assert first == {"x": "1", "y": "2"}


class TestNumberRange:
    def test_basic(self) -> None:
        assert list(NumberRange(1, 5)) == [1, 2, 3, 4]

    def test_step(self) -> None:
        assert list(NumberRange(0, 10, 2)) == [0, 2, 4, 6, 8]

    def test_empty(self) -> None:
        assert list(NumberRange(5, 5)) == []

    def test_iterable_twice(self) -> None:
        r = NumberRange(1, 4)
        assert list(r) == [1, 2, 3]
        assert list(r) == [1, 2, 3]  # can iterate again
