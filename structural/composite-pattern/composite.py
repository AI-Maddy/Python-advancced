"""
Composite Pattern.

Leaf and Composite objects both implement the Component interface, so
clients treat individual files and whole directory trees uniformly.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Component ABC
# ---------------------------------------------------------------------------
class Component(ABC):
    """Uniform interface for both leaves and composites."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._parent: Component | None = None

    @property
    def parent(self) -> Component | None:
        return self._parent

    @parent.setter
    def parent(self, parent: Component | None) -> None:
        self._parent = parent

    @abstractmethod
    def operation(self) -> str:
        """Return a string representation of this component."""

    @abstractmethod
    def size(self) -> int:
        """Return the total size of this component in bytes."""

    def add(self, component: Component) -> None:
        raise NotImplementedError(f"{type(self).__name__} cannot have children")

    def remove(self, component: Component) -> None:
        raise NotImplementedError(f"{type(self).__name__} cannot have children")

    @property
    def children(self) -> list[Component]:
        return []

    def is_composite(self) -> bool:
        return False


# ---------------------------------------------------------------------------
# Leaf
# ---------------------------------------------------------------------------
class File(Component):
    """Leaf node — a single file.

    Args:
        name: File name.
        size_bytes: File size in bytes.
    """

    def __init__(self, name: str, size_bytes: int = 0) -> None:
        super().__init__(name)
        self._size = size_bytes

    def operation(self) -> str:
        return f"File({self.name}, {self._size}B)"

    def size(self) -> int:
        return self._size


# ---------------------------------------------------------------------------
# Composite
# ---------------------------------------------------------------------------
class Directory(Component):
    """Composite node — a directory containing files and sub-directories.

    Args:
        name: Directory name.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._children: list[Component] = []

    def add(self, component: Component) -> None:
        self._children.append(component)
        component.parent = self

    def remove(self, component: Component) -> None:
        self._children.remove(component)
        component.parent = None

    @property
    def children(self) -> list[Component]:
        return list(self._children)

    def is_composite(self) -> bool:
        return True

    def operation(self) -> str:
        lines = [f"Dir({self.name})/"]
        for child in self._children:
            # Indent child lines
            for line in child.operation().splitlines():
                lines.append(f"  {line}")
        return "\n".join(lines)

    def size(self) -> int:
        return sum(child.size() for child in self._children)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    root = Directory("root")
    src = Directory("src")
    tests = Directory("tests")

    src.add(File("main.py", 1200))
    src.add(File("utils.py", 800))

    tests.add(File("test_main.py", 600))
    tests.add(File("test_utils.py", 400))

    root.add(src)
    root.add(tests)
    root.add(File("README.md", 300))

    print(root.operation())
    print(f"\nTotal size: {root.size()} B")
    print(f"src size: {src.size()} B")
