"""
Day 09 — Solutions
"""
from __future__ import annotations

from typing import Generic, TypeVar, Protocol, overload
from collections import deque

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._items: deque[T] = deque()

    def enqueue(self, item: T) -> None:
        self._items.append(item)

    def dequeue(self) -> T:
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


class Pair(Generic[A, B]):
    def __init__(self, first: A, second: B) -> None:
        self.first = first
        self.second = second

    def swap(self) -> "Pair[B, A]":
        return Pair(self.second, self.first)

    def __repr__(self) -> str:
        return f"Pair({self.first!r}, {self.second!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pair):
            return NotImplemented
        return self.first == other.first and self.second == other.second


class Comparable(Protocol):
    def __lt__(self, other: "Comparable") -> bool: ...

C = TypeVar("C", bound="Comparable")


def find_min(items: list[C]) -> C:
    if not items:
        raise ValueError("empty sequence")
    result = items[0]
    for item in items[1:]:
        if item < result:
            result = item
    return result


def binary_search(sorted_list: list[C], target: C) -> int:
    lo, hi = 0, len(sorted_list) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_list[mid] == target:  # type: ignore[operator]
            return mid
        elif sorted_list[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


@overload
def process(value: int) -> str: ...
@overload
def process(value: str) -> int: ...

def process(value: int | str) -> str | int:
    if isinstance(value, int):
        return str(value)
    return int(value)


if __name__ == "__main__":
    s: Stack[int] = Stack()
    s.push(10)
    s.push(20)
    print(s.pop())   # 20

    q: Queue[str] = Queue()
    q.enqueue("a")
    q.enqueue("b")
    print(q.dequeue())  # a

    p = Pair("hello", 42)
    print(p, p.swap())

    print(find_min([3, 1, 4, 1, 5]))
    print(binary_search([1, 2, 3, 4, 5], 3))
