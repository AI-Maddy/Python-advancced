"""Visitor Pattern — lets you add new operations to objects without modifying them.

The Visitor pattern represents an operation to be performed on elements of an
object structure.  It lets you define a new operation without changing the
classes of the elements on which it operates (double-dispatch).

Python-specific notes:
- Python supports single dispatch natively via ``functools.singledispatch``,
  but the classic double-dispatch approach (ABC + accept/visit) is shown here
  for pedagogy and to enforce the full interface at class definition time.
- ``@singledispatchmethod`` (Python 3.8+) is an idiomatic alternative.
- ``@abstractmethod`` on each ``visit_*`` method ensures visitors handle all
  shape types.
"""
from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Visitor ABC
# ---------------------------------------------------------------------------

class Visitor(ABC):
    """Abstract visitor declaring a visit method for each element type."""

    @abstractmethod
    def visit_circle(self, circle: Circle) -> object:
        """Visit a ``Circle`` element."""

    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle) -> object:
        """Visit a ``Rectangle`` element."""

    @abstractmethod
    def visit_triangle(self, triangle: Triangle) -> object:
        """Visit a ``Triangle`` element."""


# ---------------------------------------------------------------------------
# Element ABC
# ---------------------------------------------------------------------------

class Shape(ABC):
    """Abstract shape element that accepts visitors."""

    @abstractmethod
    def accept(self, visitor: Visitor) -> object:
        """Call the appropriate *visitor* method for this shape (double-dispatch).

        Args:
            visitor: The visitor to dispatch to.

        Returns:
            Whatever the visitor returns.
        """


# ---------------------------------------------------------------------------
# Concrete elements
# ---------------------------------------------------------------------------

@dataclass
class Circle(Shape):
    """Circle defined by its radius."""
    radius: float

    def accept(self, visitor: Visitor) -> object:
        return visitor.visit_circle(self)


@dataclass
class Rectangle(Shape):
    """Rectangle defined by width and height."""
    width: float
    height: float

    def accept(self, visitor: Visitor) -> object:
        return visitor.visit_rectangle(self)


@dataclass
class Triangle(Shape):
    """Triangle defined by its three side lengths."""
    a: float
    b: float
    c: float

    def accept(self, visitor: Visitor) -> object:
        return visitor.visit_triangle(self)


# ---------------------------------------------------------------------------
# Concrete visitors
# ---------------------------------------------------------------------------

class AreaCalculator(Visitor):
    """Calculates the area of each shape."""

    def visit_circle(self, circle: Circle) -> float:
        area = math.pi * circle.radius ** 2
        print(f"  Circle area (r={circle.radius}): {area:.4f}")
        return area

    def visit_rectangle(self, rectangle: Rectangle) -> float:
        area = rectangle.width * rectangle.height
        print(f"  Rectangle area ({rectangle.width}×{rectangle.height}): {area:.4f}")
        return area

    def visit_triangle(self, triangle: Triangle) -> float:
        # Heron's formula
        s = (triangle.a + triangle.b + triangle.c) / 2
        area = math.sqrt(s * (s - triangle.a) * (s - triangle.b) * (s - triangle.c))
        print(f"  Triangle area ({triangle.a},{triangle.b},{triangle.c}): {area:.4f}")
        return area


class PerimeterCalculator(Visitor):
    """Calculates the perimeter of each shape."""

    def visit_circle(self, circle: Circle) -> float:
        peri = 2 * math.pi * circle.radius
        print(f"  Circle perimeter (r={circle.radius}): {peri:.4f}")
        return peri

    def visit_rectangle(self, rectangle: Rectangle) -> float:
        peri = 2 * (rectangle.width + rectangle.height)
        print(f"  Rectangle perimeter ({rectangle.width}×{rectangle.height}): {peri:.4f}")
        return peri

    def visit_triangle(self, triangle: Triangle) -> float:
        peri = triangle.a + triangle.b + triangle.c
        print(f"  Triangle perimeter ({triangle.a},{triangle.b},{triangle.c}): {peri:.4f}")
        return peri


class SVGRenderer(Visitor):
    """Renders shapes as minimal SVG markup strings."""

    def visit_circle(self, circle: Circle) -> str:
        svg = f'<circle cx="50" cy="50" r="{circle.radius}" />'
        print(f"  SVG: {svg}")
        return svg

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        svg = f'<rect width="{rectangle.width}" height="{rectangle.height}" />'
        print(f"  SVG: {svg}")
        return svg

    def visit_triangle(self, triangle: Triangle) -> str:
        # Simple equilateral-ish polygon for SVG demo
        svg = f'<polygon data-sides="3" data-a="{triangle.a}" />'
        print(f"  SVG: {svg}")
        return svg


# ---------------------------------------------------------------------------
# Client demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    shapes: list[Shape] = [
        Circle(5.0),
        Rectangle(4.0, 6.0),
        Triangle(3.0, 4.0, 5.0),
    ]

    print("=== Area Calculator ===")
    area_calc = AreaCalculator()
    total = sum(float(s.accept(area_calc)) for s in shapes)
    print(f"  Total area: {total:.4f}")

    print("\n=== Perimeter Calculator ===")
    peri_calc = PerimeterCalculator()
    for s in shapes:
        s.accept(peri_calc)

    print("\n=== SVG Renderer ===")
    renderer = SVGRenderer()
    for s in shapes:
        s.accept(renderer)


if __name__ == "__main__":
    main()
