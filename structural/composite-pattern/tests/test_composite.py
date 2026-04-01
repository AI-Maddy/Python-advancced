"""pytest tests for composite pattern."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from composite import Directory, File


class TestFile:
    def test_size_returns_given_value(self) -> None:
        f = File("a.txt", 500)
        assert f.size() == 500

    def test_operation_contains_name(self) -> None:
        f = File("hello.py", 100)
        assert "hello.py" in f.operation()

    def test_is_not_composite(self) -> None:
        f = File("x.py")
        assert not f.is_composite()

    def test_add_raises(self) -> None:
        f = File("x.py")
        with pytest.raises(NotImplementedError):
            f.add(File("y.py"))

    def test_children_is_empty(self) -> None:
        f = File("x.py")
        assert f.children == []


class TestDirectory:
    def setup_method(self) -> None:
        self.root = Directory("root")
        self.sub = Directory("sub")
        self.f1 = File("a.py", 100)
        self.f2 = File("b.py", 200)
        self.f3 = File("c.py", 50)

    def test_size_sums_leaf_sizes(self) -> None:
        self.root.add(self.f1)
        self.root.add(self.f2)
        assert self.root.size() == 300

    def test_nested_size(self) -> None:
        self.sub.add(self.f3)
        self.root.add(self.f1)
        self.root.add(self.sub)
        assert self.root.size() == 150

    def test_operation_contains_all_names(self) -> None:
        self.root.add(self.f1)
        self.root.add(self.f2)
        result = self.root.operation()
        assert "a.py" in result
        assert "b.py" in result
        assert "root" in result

    def test_is_composite(self) -> None:
        assert self.root.is_composite()

    def test_children_returns_direct_children(self) -> None:
        self.root.add(self.f1)
        self.root.add(self.sub)
        assert len(self.root.children) == 2

    def test_remove_child(self) -> None:
        self.root.add(self.f1)
        self.root.add(self.f2)
        self.root.remove(self.f1)
        assert self.f1 not in self.root.children

    def test_parent_set_on_add(self) -> None:
        self.root.add(self.f1)
        assert self.f1.parent is self.root

    def test_parent_cleared_on_remove(self) -> None:
        self.root.add(self.f1)
        self.root.remove(self.f1)
        assert self.f1.parent is None

    def test_empty_directory_size_is_zero(self) -> None:
        assert self.root.size() == 0
