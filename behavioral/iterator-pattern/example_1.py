"""Iterator Pattern — Example 1: Binary Tree Traversal.

Builds a more complex tree and demonstrates all three traversal orders,
comparing results and verifying BST inorder property.
"""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from iterator_pattern import (
    InorderIterator,
    PostorderIterator,
    PreorderIterator,
    TreeNode,
    build_bst,
)


def main() -> None:
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    root = build_bst(*values)
    assert root is not None

    inorder = list(InorderIterator(root))
    preorder = list(PreorderIterator(root))
    postorder = list(PostorderIterator(root))

    print("Values inserted :", values)
    print("Inorder (sorted):", inorder)
    print("Preorder        :", preorder)
    print("Postorder       :", postorder)

    # BST invariant: inorder traversal yields sorted sequence
    assert inorder == sorted(values), "BST inorder must be sorted"
    print("\nBST invariant verified: inorder is sorted.")

    # Verify all three contain the same elements
    assert sorted(inorder) == sorted(preorder) == sorted(postorder)
    print("All traversals contain the same elements.")

    # Single-node tree
    single = TreeNode(42)
    print(f"\nSingle node inorder: {list(InorderIterator(single))}")

    # Empty tree
    print(f"Empty tree inorder: {list(InorderIterator(None))}")


if __name__ == "__main__":
    main()
