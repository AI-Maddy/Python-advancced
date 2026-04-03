"""Day 12 — Exercises: Iterators and Generators"""
from __future__ import annotations
from typing import Iterator, Generator


class BinaryTree:
    class Node:
        def __init__(self, v: int, l: "BinaryTree.Node|None"=None, r: "BinaryTree.Node|None"=None) -> None:
            self.value=v; self.left=l; self.right=r
    def __init__(self) -> None: self._root: "BinaryTree.Node|None" = None
    def insert(self, v: int) -> None:
        def _insert(node: "BinaryTree.Node|None", val: int) -> "BinaryTree.Node":
            if node is None:
                return BinaryTree.Node(val)
            if val < node.value:
                node.left = _insert(node.left, val)
            elif val > node.value:
                node.right = _insert(node.right, val)
            return node
        self._root = _insert(self._root, v)

    def __iter__(self) -> Iterator[int]:
        def inorder(node: "BinaryTree.Node|None") -> Generator[int, None, None]:
            if node is not None:
                yield from inorder(node.left)
                yield node.value
                yield from inorder(node.right)
        return inorder(self._root)


def fibonacci() -> Generator[int, None, None]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def lazy_csv_reader(lines: list[str]) -> Generator[dict[str, str], None, None]:
    if not lines:
        return
    headers = [h.strip() for h in lines[0].split(",")]
    for line in lines[1:]:
        if line.strip():
            values = [v.strip() for v in line.split(",")]
            yield dict(zip(headers, values))


class NumberRange:
    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.start=start; self.stop=stop; self.step=step
    def __iter__(self) -> Iterator[int]:
        current = self.start
        while (self.step > 0 and current < self.stop) or \
              (self.step < 0 and current > self.stop):
            yield current
            current += self.step


if __name__ == "__main__":
    import itertools
    fibs = list(itertools.islice(fibonacci(), 8))
    print(fibs)
