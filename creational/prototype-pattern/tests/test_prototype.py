"""pytest tests for prototype pattern."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from prototype import Circle, Rectangle, ShapeRegistry


class TestCircle:
    def test_clone_is_equal(self) -> None:
        c = Circle(10, "blue")
        clone = c.clone()
        assert c == clone

    def test_clone_is_not_identical(self) -> None:
        c = Circle(10, "blue")
        clone = c.clone()
        assert c is not clone

    def test_deep_copy_independence(self) -> None:
        c = Circle(10, "blue")
        c.tags.append("original")
        clone = c.clone()
        clone.tags.append("cloned")
        assert "cloned" not in c.tags

    def test_mutating_clone_does_not_affect_original(self) -> None:
        c = Circle(10, "blue")
        clone = c.clone()
        clone.color = "red"
        assert c.color == "blue"


class TestRectangle:
    def test_clone_is_equal(self) -> None:
        r = Rectangle(100, 50, "green")
        clone = r.clone()
        assert r == clone

    def test_clone_is_not_identical(self) -> None:
        r = Rectangle(100, 50, "green")
        assert r is not r.clone()

    def test_nested_deep_copy(self) -> None:
        r = Rectangle(100, 50, "green")
        r.children.append(Circle(5, "red"))
        clone = r.clone()
        clone.children.clear()
        assert len(r.children) == 1  # original unaffected


class TestShapeRegistry:
    def setup_method(self) -> None:
        self.registry = ShapeRegistry()
        self.registry.register("circle", Circle(20, "yellow"))
        self.registry.register("rect", Rectangle(80, 40, "purple"))

    def test_clone_returns_equal_object(self) -> None:
        c = self.registry.clone("circle")
        assert isinstance(c, Circle)
        assert c == Circle(20, "yellow")

    def test_clone_returns_different_object(self) -> None:
        c1 = self.registry.clone("circle")
        c2 = self.registry.clone("circle")
        assert c1 is not c2

    def test_mutating_clone_does_not_affect_registry(self) -> None:
        c = self.registry.clone("circle")
        assert isinstance(c, Circle)
        c.color = "black"
        c2 = self.registry.clone("circle")
        assert isinstance(c2, Circle)
        assert c2.color == "yellow"

    def test_unknown_key_raises(self) -> None:
        import pytest
        with pytest.raises(KeyError):
            self.registry.clone("hexagon")

    def test_keys_returns_registered_names(self) -> None:
        assert set(self.registry.keys()) == {"circle", "rect"}
