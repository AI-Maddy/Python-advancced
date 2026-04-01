"""Day 09 — Exercises: Generics"""
from __future__ import annotations
from typing import Generic, TypeVar, Protocol
T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")

# Exercise 1: Generic Stack[T] with push, pop, peek, is_empty, __len__, __repr__
class Stack(Generic[T]):
    def __init__(self) -> None: self._items: list[T] = []
    def push(self, item: T) -> None: pass  # TODO
    def pop(self) -> T: pass  # TODO
    def peek(self) -> T: pass  # TODO
    def is_empty(self) -> bool: pass  # TODO
    def __len__(self) -> int: pass  # TODO

# Exercise 2: Generic Queue[T] with enqueue, dequeue, is_empty, __len__
from collections import deque
class Queue(Generic[T]):
    def __init__(self) -> None: self._items: deque[T] = deque()
    def enqueue(self, item: T) -> None: pass  # TODO
    def dequeue(self) -> T: pass  # TODO
    def is_empty(self) -> bool: pass  # TODO
    def __len__(self) -> int: pass  # TODO

# Exercise 3: Generic Pair[A,B] with swap()
class Pair(Generic[A, B]):
    def __init__(self, first: A, second: B) -> None: self.first = first; self.second = second
    def swap(self) -> "Pair[B, A]": pass  # TODO

# Exercise 4: find_min with bounded TypeVar (Comparable Protocol)
class Comparable(Protocol):
    def __lt__(self, other: "Comparable") -> bool: ...

C = TypeVar("C", bound="Comparable")
def find_min(items: list[C]) -> C: pass  # TODO

if __name__ == "__main__":
    s: Stack[int] = Stack()
    s.push(1); s.push(2)
    print(s.pop())
