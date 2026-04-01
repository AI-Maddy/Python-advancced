"""
Day 25 — Exercises: Shape Editor
==================================
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from typing import Any

from lesson import (
    AreaCalculator, Circle, PerimeterCalculator, Polygon,
    Rectangle, Shape, ShapeGroup, ShapeVisitor, SVGRenderer, Triangle,
)


# ---------------------------------------------------------------------------
# Exercise 1 — Add Ellipse shape
# ---------------------------------------------------------------------------
# TODO: Implement Ellipse(Shape) with semi-axes rx > 0 and ry > 0.
#   - area = π * rx * ry
#   - perimeter ≈ π * (3*(rx+ry) - sqrt((3*rx+ry)*(rx+3*ry)))  (Ramanujan approx)
#   - accept(visitor) → visitor.visit_ellipse(self)
#   - bounding_box: based on cx, cy, rx, ry
# Also add visit_ellipse to AreaCalculator, PerimeterCalculator, SVGRenderer.

@dataclass
class Ellipse(Shape):
    """TODO: Ellipse with centre (cx, cy) and semi-axes rx, ry."""
    cx: float
    cy: float
    rx: float
    ry: float

    def __post_init__(self) -> None:
        # TODO: validate rx > 0 and ry > 0
        ...

    def accept(self, visitor: Any) -> object:
        # TODO: call visitor.visit_ellipse(self)
        ...
        return None

    def bounding_box(self) -> tuple[float, float, float, float]:
        # TODO
        ...
        return (0.0, 0.0, 0.0, 0.0)


def exercise1_ellipse() -> tuple[float, float, str]:
    """Return (area, perimeter_approx, bounding_box_str) for Ellipse(0,0,4,3)."""
    # TODO: extend AreaCalculator / PerimeterCalculator to handle Ellipse
    ...
    return (0.0, 0.0, "")


# ---------------------------------------------------------------------------
# Exercise 2 — Bounding Box visitor
# ---------------------------------------------------------------------------
# TODO: Implement BoundingBoxVisitor that returns the bounding box
#       (x_min, y_min, x_max, y_max) for any shape.
#       For groups, return the union of all children's bounding boxes.
#       Hint: Shape.bounding_box() already provides this — use it!

class BoundingBoxVisitor:
    """TODO: visitor that returns bounding box tuple."""

    def visit_circle(self, shape: Circle) -> tuple[float, float, float, float]:
        ...
        return (0.0, 0.0, 0.0, 0.0)

    def visit_rectangle(self, shape: Rectangle) -> tuple[float, float, float, float]:
        ...
        return (0.0, 0.0, 0.0, 0.0)

    def visit_triangle(self, shape: Triangle) -> tuple[float, float, float, float]:
        ...
        return (0.0, 0.0, 0.0, 0.0)

    def visit_polygon(self, shape: Polygon) -> tuple[float, float, float, float]:
        ...
        return (0.0, 0.0, 0.0, 0.0)

    def visit_group(self, group: ShapeGroup) -> tuple[float, float, float, float]:
        ...
        return (0.0, 0.0, 0.0, 0.0)

    def calculate(self, shape: Shape) -> tuple[float, float, float, float]:
        return shape.accept(self)  # type: ignore[return-value]


def exercise2_bounding_box() -> tuple[float, float, float, float]:
    """Return bounding box of Circle(5, 5, 3). Expected: (2,2,8,8)."""
    # TODO
    ...
    return (0.0, 0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# Exercise 3 — JSON Serialization visitor
# ---------------------------------------------------------------------------
# TODO: Implement JsonSerializerVisitor that converts any shape to a dict
#       (for JSON serialization).  Then write load_shape(d: dict) -> Shape.
#
# Format:
#   {"type": "circle",    "cx": 0, "cy": 0, "radius": 5}
#   {"type": "rectangle", "x": 0, "y": 0, "width": 10, "height": 5}
#   {"type": "triangle",  "x1":0,"y1":0,"x2":3,"y2":0,"x3":0,"y3":4}
#   {"type": "polygon",   "vertices": [[0,0],[1,0],[1,1],[0,1]]}
#   {"type": "group",     "name": "g1", "children": [...]}

class JsonSerializerVisitor:
    """TODO: serialize shapes to dicts."""

    def visit_circle(self, s: Circle) -> dict[str, Any]:
        ...
        return {}

    def visit_rectangle(self, s: Rectangle) -> dict[str, Any]:
        ...
        return {}

    def visit_triangle(self, s: Triangle) -> dict[str, Any]:
        ...
        return {}

    def visit_polygon(self, s: Polygon) -> dict[str, Any]:
        ...
        return {}

    def visit_group(self, g: ShapeGroup) -> dict[str, Any]:
        ...
        return {}

    def serialize(self, shape: Shape) -> str:
        """Return JSON string."""
        d = shape.accept(self)
        return json.dumps(d)


def load_shape(d: dict[str, Any]) -> Shape:
    """TODO: Reconstruct a Shape from a dict produced by JsonSerializerVisitor."""
    # TODO
    ...
    raise ValueError(f"Unknown shape type: {d.get('type')}")


def exercise3_json_serialization() -> tuple[str, bool]:
    """
    Serialize a Circle, then deserialize and check it's a Circle
    with the same radius.  Return (json_string, round_trip_ok).
    """
    # TODO
    ...
    return ("", False)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_ellipse())
    print("Exercise 2:", exercise2_bounding_box())
    print("Exercise 3:", exercise3_json_serialization())
