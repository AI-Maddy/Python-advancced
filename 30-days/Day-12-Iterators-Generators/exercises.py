"""Day 12 — Exercises: Iterators and Generators"""
from __future__ import annotations
from typing import Iterator, Generator


class BinaryTree:
    class Node:
        def __init__(self, v: int, l: "BinaryTree.Node|None"=None, r: "BinaryTree.Node|None"=None) -> None:
            self.value=v; self.left=l; self.right=r
    def __init__(self) -> None: self._root: "BinaryTree.Node|None" = None
    def insert(self, v: int) -> None: pass  # TODO
    def __iter__(self) -> Iterator[int]: pass  # TODO: in-order


def fibonacci() -> Generator[int, None, None]:
    pass  # TODO: infinite fib


def lazy_csv_reader(lines: list[str]) -> Generator[dict[str, str], None, None]:
    pass  # TODO: yield dicts per row


class NumberRange:
    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.start=start; self.stop=stop; self.step=step
    def __iter__(self) -> Iterator[int]: pass  # TODO


if __name__ == "__main__":
    import itertools
    fibs = list(itertools.islice(fibonacci(), 8))
    print(fibs)
