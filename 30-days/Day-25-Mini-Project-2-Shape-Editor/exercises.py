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
        if self.rx <= 0:
            raise ValueError(f"rx must be > 0, got {self.rx}")
        if self.ry <= 0:
            raise ValueError(f"ry must be > 0, got {self.ry}")

    def accept(self, visitor: Any) -> object:
        # TODO: call visitor.visit_ellipse(self)
        return visitor.visit_ellipse(self)

    def bounding_box(self) -> tuple[float, float, float, float]:
        # TODO
        return (
            self.cx - self.rx, self.cy - self.ry,
            self.cx + self.rx, self.cy + self.ry,
        )


def _area_visit_ellipse(self: AreaCalculator, e: Ellipse) -> float:
    return math.pi * e.rx * e.ry


def _perim_visit_ellipse(self: PerimeterCalculator, e: Ellipse) -> float:
    # Ramanujan approximation
    h = ((e.rx - e.ry) / (e.rx + e.ry)) ** 2
    return math.pi * (e.rx + e.ry) * (1 + 3 * h / (10 + math.sqrt(4 - 3 * h)))


def _svg_visit_ellipse(self: SVGRenderer, e: Ellipse) -> str:
    return (
        f'<ellipse cx="{e.cx}" cy="{e.cy}" rx="{e.rx}" ry="{e.ry}" '
        f'fill="none" stroke="black"/>'
    )


AreaCalculator.visit_ellipse = _area_visit_ellipse        # type: ignore[attr-defined]
PerimeterCalculator.visit_ellipse = _perim_visit_ellipse  # type: ignore[attr-defined]
SVGRenderer.visit_ellipse = _svg_visit_ellipse            # type: ignore[attr-defined]


def exercise1_ellipse() -> tuple[float, float, str]:
    """Return (area, perimeter_approx, bounding_box_str) for Ellipse(0,0,4,3)."""
    e = Ellipse(0, 0, 4, 3)
    area = AreaCalculator().calculate(e)   # type: ignore[arg-type]
    perim = PerimeterCalculator().calculate(e)  # type: ignore[arg-type]
    bb = str(e.bounding_box())
    return (area, perim, bb)


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
        return shape.bounding_box()

    def visit_rectangle(self, shape: Rectangle) -> tuple[float, float, float, float]:
        return shape.bounding_box()

    def visit_triangle(self, shape: Triangle) -> tuple[float, float, float, float]:
        return shape.bounding_box()

    def visit_polygon(self, shape: Polygon) -> tuple[float, float, float, float]:
        return shape.bounding_box()

    def visit_group(self, group: ShapeGroup) -> tuple[float, float, float, float]:
        if not group.children:
            return (0.0, 0.0, 0.0, 0.0)
        boxes = [child.accept(self) for child in group.children]
        return (
            min(b[0] for b in boxes),
            min(b[1] for b in boxes),
            max(b[2] for b in boxes),
            max(b[3] for b in boxes),
        )

    def calculate(self, shape: Shape) -> tuple[float, float, float, float]:
        return shape.accept(self)  # type: ignore[return-value]


def exercise2_bounding_box() -> tuple[float, float, float, float]:
    """Return bounding box of Circle(5, 5, 3). Expected: (2,2,8,8)."""
    return BoundingBoxVisitor().calculate(Circle(5, 5, 3))


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
        return {"type": "circle", "cx": s.cx, "cy": s.cy, "radius": s.radius}

    def visit_rectangle(self, s: Rectangle) -> dict[str, Any]:
        return {"type": "rectangle", "x": s.x, "y": s.y, "width": s.width, "height": s.height}

    def visit_triangle(self, s: Triangle) -> dict[str, Any]:
        return {"type": "triangle",
                "x1": s.x1, "y1": s.y1, "x2": s.x2, "y2": s.y2, "x3": s.x3, "y3": s.y3}

    def visit_polygon(self, s: Polygon) -> dict[str, Any]:
        return {"type": "polygon", "vertices": list(s.vertices)}

    def visit_group(self, g: ShapeGroup) -> dict[str, Any]:
        return {
            "type": "group",
            "name": g.name,
            "children": [child.accept(self) for child in g.children],
        }

    def serialize(self, shape: Shape) -> str:
        """Return JSON string."""
        d = shape.accept(self)
        return json.dumps(d)


def load_shape(d: dict[str, Any]) -> Shape:
    """TODO: Reconstruct a Shape from a dict produced by JsonSerializerVisitor."""
    t = d["type"]
    if t == "circle":
        return Circle(d["cx"], d["cy"], d["radius"])
    if t == "rectangle":
        return Rectangle(d["x"], d["y"], d["width"], d["height"])
    if t == "triangle":
        return Triangle(d["x1"], d["y1"], d["x2"], d["y2"], d["x3"], d["y3"])
    if t == "polygon":
        return Polygon([tuple(v) for v in d["vertices"]])
    if t == "group":
        g = ShapeGroup(name=d.get("name", "group"))
        for child_dict in d.get("children", []):
            g.add(load_shape(child_dict))
        return g
    raise ValueError(f"Unknown shape type: {t!r}")


def exercise3_json_serialization() -> tuple[str, bool]:
    """
    Serialize a Circle, then deserialize and check it's a Circle
    with the same radius.  Return (json_string, round_trip_ok).
    """
    serializer = JsonSerializerVisitor()
    original = Circle(10, 20, 5)
    json_str = serializer.serialize(original)
    loaded = load_shape(json.loads(json_str))
    round_trip_ok = isinstance(loaded, Circle) and loaded.radius == original.radius
    return (json_str, round_trip_ok)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_ellipse())
    print("Exercise 2:", exercise2_bounding_box())
    print("Exercise 3:", exercise3_json_serialization())
