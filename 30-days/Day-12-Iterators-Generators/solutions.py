"""Day 12 — Solutions: Iterators and Generators"""
from __future__ import annotations

from typing import Iterator, Generator
import itertools


# ---------------------------------------------------------------------------
# Binary Tree Iterator
# ---------------------------------------------------------------------------

class TreeNode:
    def __init__(self, value: int, left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None) -> None:
        self.value = value
        self.left = left
        self.right = right


class BinaryTree:
    """Binary search tree with in-order iterator."""

    def __init__(self) -> None:
        self._root: TreeNode | None = None

    def insert(self, value: int) -> None:
        def _insert(node: TreeNode | None, val: int) -> TreeNode:
            if node is None:
                return TreeNode(val)
            if val < node.value:
                node.left = _insert(node.left, val)
            elif val > node.value:
                node.right = _insert(node.right, val)
            return node
        self._root = _insert(self._root, value)

    def __iter__(self) -> Iterator[int]:
        """In-order traversal using yield from."""
        def inorder(node: TreeNode | None) -> Generator[int, None, None]:
            if node is not None:
                yield from inorder(node.left)
                yield node.value
                yield from inorder(node.right)
        return inorder(self._root)


# ---------------------------------------------------------------------------
# Infinite Fibonacci Generator
# ---------------------------------------------------------------------------

def fibonacci() -> Generator[int, None, None]:
    """Infinite Fibonacci sequence generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def take(n: int, gen: Generator[int, None, None]) -> list[int]:
    """Take first n elements from a generator."""
    return list(itertools.islice(gen, n))


# ---------------------------------------------------------------------------
# Lazy CSV Reader
# ---------------------------------------------------------------------------

def lazy_csv_reader(lines: list[str]) -> Generator[dict[str, str], None, None]:
    """Parse CSV lines lazily (no loading everything into memory)."""
    if not lines:
        return
    headers = [h.strip() for h in lines[0].split(",")]
    for line in lines[1:]:
        if line.strip():
            values = [v.strip() for v in line.split(",")]
            yield dict(zip(headers, values))


# ---------------------------------------------------------------------------
# Range Iterator class
# ---------------------------------------------------------------------------

class NumberRange:
    """Custom range iterator with __iter__ and __next__."""

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        if step == 0:
            raise ValueError("step cannot be zero")
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> Iterator[int]:
        current = self.start
        while (self.step > 0 and current < self.stop) or \
              (self.step < 0 and current > self.stop):
            yield current
            current += self.step

    def __len__(self) -> int:
        return max(0, (self.stop - self.start + self.step - 1) // self.step)


if __name__ == "__main__":
    tree = BinaryTree()
    for v in [5, 3, 7, 1, 4, 6, 8]:
        tree.insert(v)
    print(list(tree))  # [1, 3, 4, 5, 6, 7, 8]

    fibs = take(10, fibonacci())
    print(fibs)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    csv_data = [
        "name,age,city",
        "Alice,30,NYC",
        "Bob,25,LA",
    ]
    for row in lazy_csv_reader(csv_data):
        print(row)

    nr = NumberRange(1, 10, 2)
    print(list(nr))  # [1, 3, 5, 7, 9]
