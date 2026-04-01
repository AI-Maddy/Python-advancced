"""Tests for Day 09 — Generics"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)
import pytest
from solutions import Stack, Queue, Pair, find_min, binary_search, process


class TestStack:
    def test_push_pop(self) -> None:
        s: Stack[int] = Stack()
        s.push(1); s.push(2); s.push(3)
        assert s.pop() == 3

    def test_peek(self) -> None:
        s: Stack[int] = Stack()
        s.push(5)
        assert s.peek() == 5
        assert len(s) == 1  # peek doesn't remove

    def test_is_empty(self) -> None:
        s: Stack[int] = Stack()
        assert s.is_empty()
        s.push(1)
        assert not s.is_empty()

    def test_len(self) -> None:
        s: Stack[int] = Stack()
        s.push(1); s.push(2)
        assert len(s) == 2

    def test_pop_empty_raises(self) -> None:
        with pytest.raises(IndexError):
            Stack[int]().pop()

    def test_str_stack(self) -> None:
        s: Stack[str] = Stack()
        s.push("hello")
        assert s.pop() == "hello"


class TestQueue:
    def test_enqueue_dequeue(self) -> None:
        q: Queue[int] = Queue()
        q.enqueue(1); q.enqueue(2); q.enqueue(3)
        assert q.dequeue() == 1

    def test_fifo_order(self) -> None:
        q: Queue[str] = Queue()
        q.enqueue("a"); q.enqueue("b"); q.enqueue("c")
        assert q.dequeue() == "a"
        assert q.dequeue() == "b"

    def test_dequeue_empty_raises(self) -> None:
        with pytest.raises(IndexError):
            Queue[int]().dequeue()


class TestPair:
    def test_creation(self) -> None:
        p = Pair("hello", 42)
        assert p.first == "hello"
        assert p.second == 42

    def test_swap(self) -> None:
        p = Pair("hello", 42)
        swapped = p.swap()
        assert swapped.first == 42
        assert swapped.second == "hello"

    def test_equality(self) -> None:
        assert Pair(1, "a") == Pair(1, "a")
        assert Pair(1, "a") != Pair(2, "a")


class TestFindMin:
    def test_ints(self) -> None:
        assert find_min([3, 1, 4, 1, 5]) == 1

    def test_strings(self) -> None:
        assert find_min(["banana", "apple", "cherry"]) == "apple"

    def test_single(self) -> None:
        assert find_min([42]) == 42

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError):
            find_min([])


class TestBinarySearch:
    def test_found(self) -> None:
        assert binary_search([1, 2, 3, 4, 5], 3) == 2

    def test_not_found(self) -> None:
        assert binary_search([1, 2, 4, 5], 3) == -1

    def test_first(self) -> None:
        assert binary_search([1, 2, 3], 1) == 0

    def test_last(self) -> None:
        assert binary_search([1, 2, 3], 3) == 2


class TestProcess:
    def test_int_to_str(self) -> None:
        assert process(42) == "42"

    def test_str_to_int(self) -> None:
        assert process("42") == 42
