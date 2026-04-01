"""
Tests for Day 25 — Shape Editor
Run with: pytest tests/test_shapes.py -v
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from lesson import (
    AreaCalculator, Circle, PerimeterCalculator,
    Polygon, Rectangle, Shape, ShapeGroup, SVGRenderer, Triangle,
)


area   = AreaCalculator()
perim  = PerimeterCalculator()
svg    = SVGRenderer()


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------

def test_circle_invalid_radius() -> None:
    with pytest.raises(ValueError, match="radius"):
        Circle(0, 0, 0)


def test_circle_negative_radius() -> None:
    with pytest.raises(ValueError):
        Circle(0, 0, -5)


def test_rectangle_invalid_width() -> None:
    with pytest.raises(ValueError, match="width"):
        Rectangle(0, 0, 0, 10)


def test_rectangle_invalid_height() -> None:
    with pytest.raises(ValueError, match="height"):
        Rectangle(0, 0, 10, -1)


def test_triangle_collinear_raises() -> None:
    with pytest.raises(ValueError, match="collinear"):
        Triangle(0, 0, 1, 0, 2, 0)   # all on x-axis


def test_polygon_too_few_vertices() -> None:
    with pytest.raises(ValueError, match="3 vertices"):
        Polygon([(0, 0), (1, 1)])


# ---------------------------------------------------------------------------
# Area correctness
# ---------------------------------------------------------------------------

def test_circle_area() -> None:
    c = Circle(0, 0, 5)
    assert area.calculate(c) == pytest.approx(math.pi * 25)


def test_rectangle_area() -> None:
    r = Rectangle(0, 0, 4, 6)
    assert area.calculate(r) == pytest.approx(24.0)


def test_triangle_area_345() -> None:
    """3-4-5 right triangle has area = 6."""
    t = Triangle(0, 0, 4, 0, 0, 3)
    assert area.calculate(t) == pytest.approx(6.0)


def test_polygon_area_square() -> None:
    """Unit square polygon area = 1."""
    sq = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    assert area.calculate(sq) == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Perimeter correctness
# ---------------------------------------------------------------------------

def test_circle_perimeter() -> None:
    c = Circle(0, 0, 1)
    assert perim.calculate(c) == pytest.approx(2 * math.pi)


def test_rectangle_perimeter() -> None:
    r = Rectangle(0, 0, 3, 4)
    assert perim.calculate(r) == pytest.approx(14.0)


def test_triangle_perimeter_345() -> None:
    """3-4-5 triangle perimeter = 12."""
    t = Triangle(0, 0, 3, 0, 0, 4)
    assert perim.calculate(t) == pytest.approx(12.0)


def test_polygon_perimeter_square() -> None:
    """Unit square perimeter = 4."""
    sq = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    assert perim.calculate(sq) == pytest.approx(4.0)


# ---------------------------------------------------------------------------
# Visitor dispatch
# ---------------------------------------------------------------------------

def test_visitor_dispatch_circle() -> None:
    c = Circle(0, 0, 1)
    result = c.accept(area)
    assert isinstance(result, float)


def test_visitor_dispatch_group() -> None:
    """Group visitor sums children."""
    g = ShapeGroup()
    g.add(Rectangle(0, 0, 4, 5))  # area 20
    g.add(Rectangle(0, 0, 2, 3))  # area 6
    assert area.calculate(g) == pytest.approx(26.0)


# ---------------------------------------------------------------------------
# ShapeGroup (Composite)
# ---------------------------------------------------------------------------

def test_group_add_returns_self() -> None:
    g = ShapeGroup()
    result = g.add(Circle(0, 0, 1))
    assert result is g


def test_group_bounding_box() -> None:
    g = ShapeGroup()
    g.add(Circle(0, 0, 5))           # bb: (-5,-5,5,5)
    g.add(Rectangle(10, 10, 4, 4))   # bb: (10,10,14,14)
    bb = g.bounding_box()
    assert bb[0] == pytest.approx(-5)
    assert bb[1] == pytest.approx(-5)
    assert bb[2] == pytest.approx(14)
    assert bb[3] == pytest.approx(14)


def test_nested_groups() -> None:
    inner = ShapeGroup()
    inner.add(Circle(0, 0, 1))   # area = pi
    outer = ShapeGroup()
    outer.add(inner)
    outer.add(Rectangle(0, 0, 2, 2))  # area = 4
    total = area.calculate(outer)
    assert total == pytest.approx(math.pi + 4)


# ---------------------------------------------------------------------------
# SVGRenderer
# ---------------------------------------------------------------------------

def test_svg_circle_contains_circle_tag() -> None:
    c = Circle(10, 20, 5)
    result = svg.render(c)
    assert "<circle" in result
    assert 'r="5"' in result


def test_svg_rectangle_contains_rect_tag() -> None:
    r = Rectangle(1, 2, 3, 4)
    result = svg.render(r)
    assert "<rect" in result
    assert 'width="3"' in result


def test_svg_group_wraps_children() -> None:
    g = ShapeGroup(name="mygroup")
    g.add(Circle(0, 0, 5))
    result = g.accept(svg)
    assert '<g id="mygroup"' in result
    assert "<circle" in result


def test_svg_full_document_valid() -> None:
    c = Circle(50, 50, 25)
    doc = svg.render(c, width=200, height=200)
    assert doc.startswith('<svg')
    assert doc.endswith('</svg>')
    assert 'xmlns="http://www.w3.org/2000/svg"' in doc


# ---------------------------------------------------------------------------
# Bounding box
# ---------------------------------------------------------------------------

def test_circle_bounding_box() -> None:
    c = Circle(5, 5, 3)
    assert c.bounding_box() == (2.0, 2.0, 8.0, 8.0)


def test_rectangle_bounding_box() -> None:
    r = Rectangle(1, 2, 3, 4)
    assert r.bounding_box() == (1.0, 2.0, 4.0, 6.0)


def test_triangle_bounding_box() -> None:
    t = Triangle(0, 0, 4, 0, 2, 3)
    assert t.bounding_box() == (0.0, 0.0, 4.0, 3.0)
