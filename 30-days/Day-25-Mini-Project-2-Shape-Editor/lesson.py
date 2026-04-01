"""
Day 25 — Mini-Project 2: Shape Editor
=======================================
Shape hierarchy with Visitor pattern:
  Shape ABC → Circle, Rectangle, Triangle, Polygon
  ShapeVisitor Protocol
  AreaCalculator, PerimeterCalculator, SVGRenderer visitors
  ShapeGroup (Composite pattern)
  @dataclass with __post_init__ validation
"""
from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol


# ===========================================================================
# ShapeVisitor Protocol
# ===========================================================================

class ShapeVisitor(Protocol):
    """
    Visitor that can process any concrete shape.
    Implement all visit_* methods to handle each shape type.
    """

    def visit_circle(self, shape: Circle) -> object: ...
    def visit_rectangle(self, shape: Rectangle) -> object: ...
    def visit_triangle(self, shape: Triangle) -> object: ...
    def visit_polygon(self, shape: Polygon) -> object: ...
    def visit_group(self, group: ShapeGroup) -> object: ...


# ===========================================================================
# Shape ABC
# ===========================================================================

class Shape(ABC):
    """Abstract base shape."""

    @abstractmethod
    def accept(self, visitor: ShapeVisitor) -> object:
        """Dispatch to the correct visitor method."""

    @abstractmethod
    def bounding_box(self) -> tuple[float, float, float, float]:
        """Return (x_min, y_min, x_max, y_max)."""


# ===========================================================================
# Concrete shapes
# ===========================================================================

@dataclass
class Circle(Shape):
    """
    Circle with centre (cx, cy) and radius.

    Attributes:
        cx: Centre x coordinate.
        cy: Centre y coordinate.
        radius: Must be > 0.
    """
    cx: float
    cy: float
    radius: float

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError(f"Circle radius must be > 0, got {self.radius}")

    def accept(self, visitor: ShapeVisitor) -> object:
        return visitor.visit_circle(self)

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (
            self.cx - self.radius,
            self.cy - self.radius,
            self.cx + self.radius,
            self.cy + self.radius,
        )


@dataclass
class Rectangle(Shape):
    """
    Axis-aligned rectangle.

    Attributes:
        x: Left edge x coordinate.
        y: Bottom edge y coordinate.
        width: Must be > 0.
        height: Must be > 0.
    """
    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError(f"Rectangle width must be > 0, got {self.width}")
        if self.height <= 0:
            raise ValueError(f"Rectangle height must be > 0, got {self.height}")

    def accept(self, visitor: ShapeVisitor) -> object:
        return visitor.visit_rectangle(self)

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.x + self.width, self.y + self.height)


@dataclass
class Triangle(Shape):
    """
    Triangle defined by three vertices (x1,y1), (x2,y2), (x3,y3).

    Validation: vertices must not be collinear (non-zero area).
    """
    x1: float
    y1: float
    x2: float
    y2: float
    x3: float
    y3: float

    def __post_init__(self) -> None:
        area = abs(
            (self.x1 * (self.y2 - self.y3)
             + self.x2 * (self.y3 - self.y1)
             + self.x3 * (self.y1 - self.y2)) / 2
        )
        if area == 0:
            raise ValueError("Triangle vertices are collinear (zero area)")

    def accept(self, visitor: ShapeVisitor) -> object:
        return visitor.visit_triangle(self)

    def bounding_box(self) -> tuple[float, float, float, float]:
        xs = [self.x1, self.x2, self.x3]
        ys = [self.y1, self.y2, self.y3]
        return (min(xs), min(ys), max(xs), max(ys))


@dataclass
class Polygon(Shape):
    """
    Arbitrary closed polygon defined by a list of (x, y) vertices.
    Must have at least 3 distinct vertices.
    """
    vertices: list[tuple[float, float]]

    def __post_init__(self) -> None:
        if len(self.vertices) < 3:
            raise ValueError(f"Polygon needs at least 3 vertices, got {len(self.vertices)}")

    def accept(self, visitor: ShapeVisitor) -> object:
        return visitor.visit_polygon(self)

    def bounding_box(self) -> tuple[float, float, float, float]:
        xs = [v[0] for v in self.vertices]
        ys = [v[1] for v in self.vertices]
        return (min(xs), min(ys), max(xs), max(ys))


# ===========================================================================
# ShapeGroup — Composite pattern
# ===========================================================================

@dataclass
class ShapeGroup(Shape):
    """
    A group of shapes treated as a single shape (Composite pattern).
    Visitors operate recursively on all children.
    """
    children: list[Shape] = field(default_factory=list)
    name: str = "group"

    def add(self, shape: Shape) -> ShapeGroup:
        """Add a child shape; return self for chaining."""
        self.children.append(shape)
        return self

    def accept(self, visitor: ShapeVisitor) -> object:
        return visitor.visit_group(self)

    def bounding_box(self) -> tuple[float, float, float, float]:
        if not self.children:
            return (0.0, 0.0, 0.0, 0.0)
        boxes = [c.bounding_box() for c in self.children]
        return (
            min(b[0] for b in boxes),
            min(b[1] for b in boxes),
            max(b[2] for b in boxes),
            max(b[3] for b in boxes),
        )


# ===========================================================================
# AreaCalculator visitor
# ===========================================================================

class AreaCalculator:
    """
    Visitor that computes the total area of a shape or group.

    For a ShapeGroup, returns the sum of children's areas.
    """

    def visit_circle(self, shape: Circle) -> float:
        """Area = π r²."""
        return math.pi * shape.radius ** 2

    def visit_rectangle(self, shape: Rectangle) -> float:
        """Area = width × height."""
        return shape.width * shape.height

    def visit_triangle(self, shape: Triangle) -> float:
        """Area via shoelace formula."""
        return abs(
            (shape.x1 * (shape.y2 - shape.y3)
             + shape.x2 * (shape.y3 - shape.y1)
             + shape.x3 * (shape.y1 - shape.y2)) / 2
        )

    def visit_polygon(self, shape: Polygon) -> float:
        """Area via shoelace formula."""
        n = len(shape.vertices)
        total = 0.0
        for i in range(n):
            x1, y1 = shape.vertices[i]
            x2, y2 = shape.vertices[(i + 1) % n]
            total += x1 * y2 - x2 * y1
        return abs(total) / 2

    def visit_group(self, group: ShapeGroup) -> float:
        """Sum areas of all children."""
        return sum(child.accept(self) for child in group.children)  # type: ignore[misc]

    def calculate(self, shape: Shape) -> float:
        """Public entry point."""
        return shape.accept(self)  # type: ignore[return-value]


# ===========================================================================
# PerimeterCalculator visitor
# ===========================================================================

class PerimeterCalculator:
    """Visitor that computes perimeter / circumference."""

    def visit_circle(self, shape: Circle) -> float:
        """Circumference = 2πr."""
        return 2 * math.pi * shape.radius

    def visit_rectangle(self, shape: Rectangle) -> float:
        """Perimeter = 2(w + h)."""
        return 2 * (shape.width + shape.height)

    def visit_triangle(self, shape: Triangle) -> float:
        """Sum of three side lengths."""
        def dist(ax: float, ay: float, bx: float, by: float) -> float:
            return math.sqrt((bx - ax) ** 2 + (by - ay) ** 2)
        return (
            dist(shape.x1, shape.y1, shape.x2, shape.y2)
            + dist(shape.x2, shape.y2, shape.x3, shape.y3)
            + dist(shape.x3, shape.y3, shape.x1, shape.y1)
        )

    def visit_polygon(self, shape: Polygon) -> float:
        """Sum of all edge lengths."""
        total = 0.0
        n = len(shape.vertices)
        for i in range(n):
            x1, y1 = shape.vertices[i]
            x2, y2 = shape.vertices[(i + 1) % n]
            total += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return total

    def visit_group(self, group: ShapeGroup) -> float:
        """Sum perimeters of all children."""
        return sum(child.accept(self) for child in group.children)  # type: ignore[misc]

    def calculate(self, shape: Shape) -> float:
        """Public entry point."""
        return shape.accept(self)  # type: ignore[return-value]


# ===========================================================================
# SVGRenderer visitor
# ===========================================================================

class SVGRenderer:
    """
    Visitor that generates an SVG string for a shape or group.
    Produces minimal valid SVG elements.
    """

    def visit_circle(self, shape: Circle) -> str:
        return (
            f'<circle cx="{shape.cx}" cy="{shape.cy}" r="{shape.radius}" '
            f'fill="none" stroke="black"/>'
        )

    def visit_rectangle(self, shape: Rectangle) -> str:
        return (
            f'<rect x="{shape.x}" y="{shape.y}" '
            f'width="{shape.width}" height="{shape.height}" '
            f'fill="none" stroke="black"/>'
        )

    def visit_triangle(self, shape: Triangle) -> str:
        pts = f"{shape.x1},{shape.y1} {shape.x2},{shape.y2} {shape.x3},{shape.y3}"
        return f'<polygon points="{pts}" fill="none" stroke="black"/>'

    def visit_polygon(self, shape: Polygon) -> str:
        pts = " ".join(f"{x},{y}" for x, y in shape.vertices)
        return f'<polygon points="{pts}" fill="none" stroke="black"/>'

    def visit_group(self, group: ShapeGroup) -> str:
        inner = "\n  ".join(child.accept(self) for child in group.children)  # type: ignore[misc]
        return f'<g id="{group.name}">\n  {inner}\n</g>'

    def render(self, shape: Shape, width: int = 400, height: int = 400) -> str:
        """Return full SVG document string."""
        content = shape.accept(self)
        return (
            f'<svg width="{width}" height="{height}" '
            f'xmlns="http://www.w3.org/2000/svg">\n{content}\n</svg>'
        )


# ===========================================================================
# Main demo
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 25 — Shape Editor")
    print("=" * 60)

    area_calc = AreaCalculator()
    perim_calc = PerimeterCalculator()
    svg_renderer = SVGRenderer()

    shapes: list[Shape] = [
        Circle(cx=100, cy=100, radius=50),
        Rectangle(x=10, y=10, width=80, height=40),
        Triangle(x1=0, y1=0, x2=3, y2=0, x3=0, y3=4),
        Polygon(vertices=[(0,0), (4,0), (4,3), (0,3)]),
    ]

    print("\nIndividual shapes:")
    for s in shapes:
        name = type(s).__name__
        area  = area_calc.calculate(s)
        perim = perim_calc.calculate(s)
        print(f"  {name}: area={area:.4f}, perimeter={perim:.4f}")

    # Composite
    group = ShapeGroup(name="scene")
    group.add(Circle(50, 50, 30))
    group.add(Rectangle(0, 0, 100, 60))

    print(f"\nGroup area:      {area_calc.calculate(group):.4f}")
    print(f"Group perimeter: {perim_calc.calculate(group):.4f}")
    print(f"Group bounding box: {group.bounding_box()}")

    # SVG
    print("\nSVG for circle:")
    print(svg_renderer.render(Circle(100, 100, 50)))

    # Validation
    try:
        Circle(0, 0, -5)
    except ValueError as e:
        print(f"\nValidation caught: {e}")
