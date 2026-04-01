"""
Day 25 — Solutions: Shape Editor
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
# Solution 1 — Ellipse
# ---------------------------------------------------------------------------

@dataclass
class Ellipse(Shape):
    cx: float
    cy: float
    rx: float
    ry: float

    def __post_init__(self) -> None:
        if self.rx <= 0:
            raise ValueError(f"rx must be > 0, got {self.rx}")
        if self.ry <= 0:
            raise ValueError(f"ry must be > 0, got {self.ry}")

    def accept(self, visitor: Any) -> object:
        return visitor.visit_ellipse(self)

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (
            self.cx - self.rx, self.cy - self.ry,
            self.cx + self.rx, self.cy + self.ry,
        )


# Extend calculators for Ellipse using monkey-patch style additions

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
    e = Ellipse(0, 0, 4, 3)
    area = AreaCalculator().calculate(e)   # type: ignore[arg-type]
    perim = PerimeterCalculator().calculate(e)  # type: ignore[arg-type]
    bb = str(e.bounding_box())
    return (area, perim, bb)


# ---------------------------------------------------------------------------
# Solution 2 — BoundingBoxVisitor
# ---------------------------------------------------------------------------

class BoundingBoxVisitor:
    def visit_circle(self, s: Circle) -> tuple[float, float, float, float]:
        return s.bounding_box()

    def visit_rectangle(self, s: Rectangle) -> tuple[float, float, float, float]:
        return s.bounding_box()

    def visit_triangle(self, s: Triangle) -> tuple[float, float, float, float]:
        return s.bounding_box()

    def visit_polygon(self, s: Polygon) -> tuple[float, float, float, float]:
        return s.bounding_box()

    def visit_group(self, g: ShapeGroup) -> tuple[float, float, float, float]:
        if not g.children:
            return (0.0, 0.0, 0.0, 0.0)
        boxes = [child.accept(self) for child in g.children]
        return (
            min(b[0] for b in boxes),
            min(b[1] for b in boxes),
            max(b[2] for b in boxes),
            max(b[3] for b in boxes),
        )

    def calculate(self, shape: Shape) -> tuple[float, float, float, float]:
        return shape.accept(self)  # type: ignore[return-value]


def exercise2_bounding_box() -> tuple[float, float, float, float]:
    return BoundingBoxVisitor().calculate(Circle(5, 5, 3))


# ---------------------------------------------------------------------------
# Solution 3 — JSON Serialization
# ---------------------------------------------------------------------------

class JsonSerializerVisitor:
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
        d = shape.accept(self)
        return json.dumps(d)


def load_shape(d: dict[str, Any]) -> Shape:
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
    print("Solution 1:", exercise1_ellipse())
    print("Solution 2:", exercise2_bounding_box())
    print("Solution 3:", exercise3_json_serialization())
