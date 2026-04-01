"""Iterator Pattern — provides a way to traverse elements of a collection sequentially.

Python natively supports the iterator protocol via ``__iter__`` / ``__next__``.
This module shows both the explicit ABC approach (for teaching purposes) and
the idiomatic Python protocol on a binary tree.

Python-specific notes:
- Python's ``Iterator`` ABC is in ``collections.abc``; any class implementing
  ``__iter__`` and ``__next__`` is accepted as an iterator without subclassing.
- Generator functions (``yield``) are the most Pythonic way to write iterators.
- The ``TreeNode`` class uses ``__iter__`` to delegate to ``InorderIterator``.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import Generic, Iterator as IteratorT, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Abstract iterator (for illustration; Python's protocol is sufficient)
# ---------------------------------------------------------------------------

class Iterator(ABC, Generic[T]):
    """Abstract iterator that mirrors Python's iterator protocol."""

    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        """Return self."""

    @abstractmethod
    def __next__(self) -> T:
        """Return the next element or raise ``StopIteration``."""


# ---------------------------------------------------------------------------
# Binary tree structure
# ---------------------------------------------------------------------------

@dataclass
class TreeNode:
    """A node in a binary tree.

    Attributes:
        value: The value stored at this node.
        left:  Left child node, or ``None``.
        right: Right child node, or ``None``.
    """
    value: int
    left: TreeNode | None = field(default=None, repr=False)
    right: TreeNode | None = field(default=None, repr=False)

    def __iter__(self) -> IteratorT[int]:
        """Default iteration is inorder traversal."""
        return InorderIterator(self)


# ---------------------------------------------------------------------------
# Concrete iterators
# ---------------------------------------------------------------------------

class InorderIterator(Iterator[int]):
    """Left → Root → Right inorder traversal.

    Uses an explicit stack to avoid recursion limits on large trees.
    """

    def __init__(self, root: TreeNode | None) -> None:
        self._stack: list[TreeNode] = []
        self._current: TreeNode | None = root

    def __iter__(self) -> InorderIterator:
        return self

    def __next__(self) -> int:
        while self._current is not None:
            self._stack.append(self._current)
            self._current = self._current.left
        if not self._stack:
            raise StopIteration
        node = self._stack.pop()
        self._current = node.right
        return node.value


class PreorderIterator(Iterator[int]):
    """Root → Left → Right preorder traversal."""

    def __init__(self, root: TreeNode | None) -> None:
        self._stack: list[TreeNode] = [root] if root else []

    def __iter__(self) -> PreorderIterator:
        return self

    def __next__(self) -> int:
        if not self._stack:
            raise StopIteration
        node = self._stack.pop()
        # Push right first so left is processed first
        if node.right:
            self._stack.append(node.right)
        if node.left:
            self._stack.append(node.left)
        return node.value


class PostorderIterator(Iterator[int]):
    """Left → Right → Root postorder traversal.

    Uses two stacks to avoid modifying the tree.
    """

    def __init__(self, root: TreeNode | None) -> None:
        self._result: deque[int] = deque()
        if root:
            stack = [root]
            while stack:
                node = stack.pop()
                self._result.appendleft(node.value)
                if node.left:
                    stack.append(node.left)
                if node.right:
                    stack.append(node.right)

    def __iter__(self) -> PostorderIterator:
        return self

    def __next__(self) -> int:
        if not self._result:
            raise StopIteration
        return self._result.popleft()


# ---------------------------------------------------------------------------
# Client demonstration
# ---------------------------------------------------------------------------

def build_bst(*values: int) -> TreeNode | None:
    """Build a simple BST from *values*."""
    root: TreeNode | None = None

    def insert(node: TreeNode | None, val: int) -> TreeNode:
        if node is None:
            return TreeNode(val)
        if val < node.value:
            node.left = insert(node.left, val)
        else:
            node.right = insert(node.right, val)
        return node

    for v in values:
        root = insert(root, v)
    return root


def main() -> None:
    root = build_bst(5, 3, 7, 1, 4, 6, 8)

    print("Inorder   (should be sorted):", list(InorderIterator(root)))
    print("Preorder  :", list(PreorderIterator(root)))
    print("Postorder :", list(PostorderIterator(root)))

    # Python for-loop uses __iter__ → InorderIterator
    print("for-loop  :", [v for v in root])  # type: ignore[union-attr]


if __name__ == "__main__":
    main()
