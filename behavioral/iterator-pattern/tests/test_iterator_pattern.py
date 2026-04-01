"""Tests for the Iterator Pattern implementation."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from iterator_pattern import (
    InorderIterator,
    Iterator,
    PostorderIterator,
    PreorderIterator,
    TreeNode,
    build_bst,
)


def make_tree() -> TreeNode:
    """Build a known BST: 5 is root, 3 left, 7 right, 1/4 under 3, 6/8 under 7."""
    return build_bst(5, 3, 7, 1, 4, 6, 8)  # type: ignore[return-value]


class TestInorderIterator:
    def test_sorted_sequence_for_bst(self) -> None:
        root = make_tree()
        assert list(InorderIterator(root)) == [1, 3, 4, 5, 6, 7, 8]

    def test_single_node(self) -> None:
        assert list(InorderIterator(TreeNode(42))) == [42]

    def test_empty_tree(self) -> None:
        assert list(InorderIterator(None)) == []

    def test_stop_iteration_raised(self) -> None:
        it = InorderIterator(None)
        with pytest.raises(StopIteration):
            next(it)

    def test_iter_returns_self(self) -> None:
        it = InorderIterator(make_tree())
        assert iter(it) is it


class TestPreorderIterator:
    def test_root_first(self) -> None:
        root = make_tree()
        result = list(PreorderIterator(root))
        assert result[0] == 5  # root

    def test_all_values_present(self) -> None:
        root = make_tree()
        assert sorted(PreorderIterator(root)) == [1, 3, 4, 5, 6, 7, 8]

    def test_empty_tree(self) -> None:
        assert list(PreorderIterator(None)) == []

    def test_stop_iteration_raised(self) -> None:
        it = PreorderIterator(None)
        with pytest.raises(StopIteration):
            next(it)


class TestPostorderIterator:
    def test_root_last(self) -> None:
        root = make_tree()
        result = list(PostorderIterator(root))
        assert result[-1] == 5  # root is last in postorder

    def test_all_values_present(self) -> None:
        root = make_tree()
        assert sorted(PostorderIterator(root)) == [1, 3, 4, 5, 6, 7, 8]

    def test_empty_tree(self) -> None:
        assert list(PostorderIterator(None)) == []

    def test_stop_iteration_raised(self) -> None:
        it = PostorderIterator(None)
        with pytest.raises(StopIteration):
            next(it)


class TestTreeNodeProtocol:
    def test_for_loop_uses_inorder(self) -> None:
        root = make_tree()
        assert list(root) == list(InorderIterator(build_bst(5, 3, 7, 1, 4, 6, 8)))  # type: ignore[arg-type]

    def test_abc_not_instantiable(self) -> None:
        with pytest.raises(TypeError):
            Iterator()  # type: ignore[abstract]
