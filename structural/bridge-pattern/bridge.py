"""
Bridge Pattern.

Decouples an abstraction (Shape) from its implementation (Renderer) so
both can vary independently.  The shape does not know *how* it is drawn —
it delegates to a Renderer implementation object.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Implementation hierarchy
# ---------------------------------------------------------------------------
class Renderer(ABC):
    """Implementation interface — how to draw primitives."""

    @abstractmethod
    def render_circle(self, radius: float) -> str: ...

    @abstractmethod
    def render_rectangle(self, width: float, height: float) -> str: ...


class VectorRenderer(Renderer):
    """Renders shapes as SVG-like vector paths."""

    def render_circle(self, radius: float) -> str:
        return f"<circle r='{radius}'/>"

    def render_rectangle(self, width: float, height: float) -> str:
        return f"<rect w='{width}' h='{height}'/>"


class RasterRenderer(Renderer):
    """Renders shapes as rasterised bitmaps."""

    def render_circle(self, radius: float) -> str:
        return f"Drawing raster circle with radius {radius:.1f}px"

    def render_rectangle(self, width: float, height: float) -> str:
        return f"Drawing raster rect {width:.1f}x{height:.1f}px"


class AsciiRenderer(Renderer):
    """Renders shapes as ASCII-art descriptions."""

    def render_circle(self, radius: float) -> str:
        return f"(O) [r={radius}]"

    def render_rectangle(self, width: float, height: float) -> str:
        return f"[=] [{width}x{height}]"


# ---------------------------------------------------------------------------
# Abstraction hierarchy
# ---------------------------------------------------------------------------
class Shape(ABC):
    """Abstraction — holds a reference to a Renderer implementation."""

    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer

    @abstractmethod
    def draw(self) -> str:
        """Draw this shape using the assigned renderer."""

    @abstractmethod
    def resize(self, factor: float) -> None:
        """Resize this shape by a scaling factor."""


class Circle(Shape):
    """Refined abstraction: circle shape.

    Args:
        renderer: The rendering back-end to use.
        radius: Circle radius.
    """

    def __init__(self, renderer: Renderer, radius: float) -> None:
        super().__init__(renderer)
        self.radius = radius

    def draw(self) -> str:
        return self.renderer.render_circle(self.radius)

    def resize(self, factor: float) -> None:
        self.radius *= factor


class Rectangle(Shape):
    """Refined abstraction: rectangle shape.

    Args:
        renderer: The rendering back-end to use.
        width: Rectangle width.
        height: Rectangle height.
    """

    def __init__(self, renderer: Renderer, width: float, height: float) -> None:
        super().__init__(renderer)
        self.width = width
        self.height = height

    def draw(self) -> str:
        return self.renderer.render_rectangle(self.width, self.height)

    def resize(self, factor: float) -> None:
        self.width *= factor
        self.height *= factor


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    renderers: list[Renderer] = [
        VectorRenderer(), RasterRenderer(), AsciiRenderer()
    ]
    for renderer in renderers:
        circle = Circle(renderer, 5.0)
        rect = Rectangle(renderer, 10.0, 4.0)
        print(circle.draw())
        print(rect.draw())

    # Swap renderer at runtime
    c = Circle(VectorRenderer(), 3.0)
    print(f"\nBefore: {c.draw()}")
    c.renderer = RasterRenderer()
    print(f"After swap: {c.draw()}")

    c.resize(2.0)
    print(f"After resize: {c.draw()}")
