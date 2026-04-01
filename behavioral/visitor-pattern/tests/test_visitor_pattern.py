"""Tests for the Visitor Pattern implementation."""
from __future__ import annotations

import math
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from visitor_pattern import (
    AreaCalculator,
    Circle,
    PerimeterCalculator,
    Rectangle,
    SVGRenderer,
    Shape,
    Triangle,
    Visitor,
)


class TestDoubleDispatch:
    """Verify that accept() calls the correct visit method."""

    def test_circle_calls_visit_circle(self) -> None:
        visited: list[str] = []

        class TrackingVisitor(Visitor):
            def visit_circle(self, c: Circle) -> None:
                visited.append("circle")
            def visit_rectangle(self, r: Rectangle) -> None:
                visited.append("rectangle")
            def visit_triangle(self, t: Triangle) -> None:
                visited.append("triangle")

        Circle(1.0).accept(TrackingVisitor())
        assert visited == ["circle"]

    def test_rectangle_calls_visit_rectangle(self) -> None:
        visited: list[str] = []

        class TrackingVisitor(Visitor):
            def visit_circle(self, c: Circle) -> None:
                visited.append("circle")
            def visit_rectangle(self, r: Rectangle) -> None:
                visited.append("rectangle")
            def visit_triangle(self, t: Triangle) -> None:
                visited.append("triangle")

        Rectangle(2.0, 3.0).accept(TrackingVisitor())
        assert visited == ["rectangle"]

    def test_triangle_calls_visit_triangle(self) -> None:
        visited: list[str] = []

        class TrackingVisitor(Visitor):
            def visit_circle(self, c: Circle) -> None:
                visited.append("circle")
            def visit_rectangle(self, r: Rectangle) -> None:
                visited.append("rectangle")
            def visit_triangle(self, t: Triangle) -> None:
                visited.append("triangle")

        Triangle(3.0, 4.0, 5.0).accept(TrackingVisitor())
        assert visited == ["triangle"]


class TestAreaCalculator:
    calc = AreaCalculator()

    def test_circle_area(self) -> None:
        result = Circle(5.0).accept(self.calc)
        assert abs(float(result) - math.pi * 25) < 1e-9

    def test_rectangle_area(self) -> None:
        result = Rectangle(4.0, 6.0).accept(self.calc)
        assert result == pytest.approx(24.0)

    def test_triangle_area_right(self) -> None:
        # 3-4-5 right triangle: area = 6
        result = Triangle(3.0, 4.0, 5.0).accept(self.calc)
        assert result == pytest.approx(6.0)


class TestPerimeterCalculator:
    calc = PerimeterCalculator()

    def test_circle_perimeter(self) -> None:
        result = Circle(3.0).accept(self.calc)
        assert float(result) == pytest.approx(2 * math.pi * 3.0)

    def test_rectangle_perimeter(self) -> None:
        result = Rectangle(5.0, 10.0).accept(self.calc)
        assert result == pytest.approx(30.0)

    def test_triangle_perimeter(self) -> None:
        result = Triangle(3.0, 4.0, 5.0).accept(self.calc)
        assert result == pytest.approx(12.0)


class TestSVGRenderer:
    renderer = SVGRenderer()

    def test_circle_svg(self) -> None:
        result = str(Circle(10.0).accept(self.renderer))
        assert "circle" in result.lower()
        assert "10.0" in result

    def test_rectangle_svg(self) -> None:
        result = str(Rectangle(20.0, 30.0).accept(self.renderer))
        assert "rect" in result.lower()

    def test_triangle_svg(self) -> None:
        result = str(Triangle(1.0, 1.0, 1.0).accept(self.renderer))
        assert "polygon" in result.lower() or "triangle" in result.lower() or "data-sides" in result


class TestABCs:
    def test_visitor_abc_not_instantiable(self) -> None:
        with pytest.raises(TypeError):
            Visitor()  # type: ignore[abstract]

    def test_shape_abc_not_instantiable(self) -> None:
        with pytest.raises(TypeError):
            Shape()  # type: ignore[abstract]

    def test_concrete_shapes_are_shape_instances(self) -> None:
        for shape in (Circle(1.0), Rectangle(1.0, 1.0), Triangle(1.0, 1.0, 1.0)):
            assert isinstance(shape, Shape)
