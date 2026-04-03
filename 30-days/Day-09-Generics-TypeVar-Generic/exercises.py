"""Day 09 — Exercises: Generics"""
from __future__ import annotations
from typing import Generic, TypeVar, Protocol
T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")

# Exercise 1: Generic Stack[T] with push, pop, peek, is_empty, __len__, __repr__
class Stack(Generic[T]):
    def __init__(self) -> None: self._items: list[T] = []

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

# Exercise 2: Generic Queue[T] with enqueue, dequeue, is_empty, __len__
from collections import deque
class Queue(Generic[T]):
    def __init__(self) -> None: self._items: deque[T] = deque()

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

# Exercise 3: Generic Pair[A,B] with swap()
class Pair(Generic[A, B]):
    def __init__(self, first: A, second: B) -> None: self.first = first; self.second = second

    def swap(self) -> "Pair[B, A]":
        return Pair(self.second, self.first)

# Exercise 4: find_min with bounded TypeVar (Comparable Protocol)
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

if __name__ == "__main__":
    s: Stack[int] = Stack()
    s.push(1); s.push(2)
    print(s.pop())
