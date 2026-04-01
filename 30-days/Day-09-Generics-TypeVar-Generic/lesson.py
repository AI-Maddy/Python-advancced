"""
Day 09 — Generics: TypeVar and Generic
========================================

Topics:
  - typing.TypeVar, typing.Generic[T]
  - Generic classes: Stack[T], Queue[T], Pair[A, B]
  - Bounded TypeVar: T = TypeVar('T', bound=Comparable)
  - typing.ParamSpec for decorator types
  - typing.overload for overloaded function signatures
"""
from __future__ import annotations

from typing import Generic, TypeVar, overload, ParamSpec, Callable
from collections import deque

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")
A = TypeVar("A")
B = TypeVar("B")
P = ParamSpec("P")


# ---------------------------------------------------------------------------
# Generic Stack[T]
# ---------------------------------------------------------------------------

class Stack(Generic[T]):
    """Type-safe LIFO stack.

    Usage:
        stack: Stack[int] = Stack()
        stack.push(1)
        stack.push(2)
        top: int = stack.pop()
    """

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


# ---------------------------------------------------------------------------
# Generic Pair[A, B]
# ---------------------------------------------------------------------------

class Pair(Generic[A, B]):
    """Typed pair of two values."""

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


# ---------------------------------------------------------------------------
# Bounded TypeVar
# ---------------------------------------------------------------------------
from typing import Protocol

class Comparable(Protocol):
    def __lt__(self, other: "Comparable") -> bool: ...
    def __le__(self, other: "Comparable") -> bool: ...

C = TypeVar("C", bound="Comparable")


def find_min(items: list[C]) -> C:
    """Return the minimum element. T must be comparable."""
    if not items:
        raise ValueError("empty sequence")
    result = items[0]
    for item in items[1:]:
        if item < result:
            result = item
    return result


def binary_search(sorted_list: list[C], target: C) -> int:
    """Return index of target in sorted_list, or -1."""
    lo, hi = 0, len(sorted_list) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# ---------------------------------------------------------------------------
# @overload — Multiple Signatures
# ---------------------------------------------------------------------------

@overload
def process(value: int) -> str: ...
@overload
def process(value: str) -> int: ...

def process(value: int | str) -> str | int:
    """Overloaded: int → str, str → int."""
    if isinstance(value, int):
        return str(value)
    return int(value)


# ---------------------------------------------------------------------------
# ParamSpec — Preserving Callable Signatures in Decorators
# ---------------------------------------------------------------------------

def logged(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator that logs calls. ParamSpec preserves the signature."""
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Done {func.__name__} -> {result!r}")
        return result
    return wrapper


@logged
def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    print("=== Stack[int] ===")
    s: Stack[int] = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    print(s)
    print(s.pop())  # 3
    print(len(s))   # 2

    print("\n=== Pair[str, int] ===")
    p: Pair[str, int] = Pair("hello", 42)
    print(p)
    print(p.swap())

    print("\n=== Bounded TypeVar ===")
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"min: {find_min(nums)}")
    print(f"min str: {find_min(['banana', 'apple', 'cherry'])}")
    print(f"search: {binary_search([1,2,3,4,5], 3)}")

    print("\n=== @overload ===")
    print(process(42))        # "42"
    print(process("42"))      # 42

    print("\n=== ParamSpec ===")
    add(3, 4)
