"""pytest tests for bridge pattern."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from bridge import (
    AsciiRenderer,
    Circle,
    RasterRenderer,
    Rectangle,
    Renderer,
    Shape,
    VectorRenderer,
)


class TestRenderers:
    def test_vector_circle(self) -> None:
        r = VectorRenderer()
        result = r.render_circle(5.0)
        assert "5.0" in result or "5" in result

    def test_raster_rectangle(self) -> None:
        r = RasterRenderer()
        result = r.render_rectangle(10.0, 4.0)
        assert "10.0" in result or "10" in result

    def test_ascii_circle(self) -> None:
        r = AsciiRenderer()
        result = r.render_circle(3.0)
        assert isinstance(result, str)


class TestCircle:
    def test_draw_returns_string(self) -> None:
        c = Circle(VectorRenderer(), 5.0)
        assert isinstance(c.draw(), str)

    def test_draw_uses_renderer(self) -> None:
        vec = Circle(VectorRenderer(), 5.0)
        ras = Circle(RasterRenderer(), 5.0)
        assert vec.draw() != ras.draw()

    def test_resize(self) -> None:
        c = Circle(VectorRenderer(), 4.0)
        c.resize(2.0)
        assert c.radius == 8.0

    def test_swap_renderer_at_runtime(self) -> None:
        c = Circle(VectorRenderer(), 5.0)
        before = c.draw()
        c.renderer = RasterRenderer()
        after = c.draw()
        assert before != after


class TestRectangle:
    def test_draw_returns_string(self) -> None:
        r = Rectangle(AsciiRenderer(), 10.0, 5.0)
        assert isinstance(r.draw(), str)

    def test_resize_scales_both_dimensions(self) -> None:
        r = Rectangle(VectorRenderer(), 10.0, 4.0)
        r.resize(0.5)
        assert r.width == 5.0
        assert r.height == 2.0


class TestIndependentVariation:
    def test_same_shape_different_renderers(self) -> None:
        renderers: list[Renderer] = [
            VectorRenderer(), RasterRenderer(), AsciiRenderer()
        ]
        outputs = [Circle(r, 5.0).draw() for r in renderers]
        assert len(set(outputs)) == 3  # all different

    def test_same_renderer_different_shapes(self) -> None:
        renderer = VectorRenderer()
        shapes: list[Shape] = [
            Circle(renderer, 5.0),
            Rectangle(renderer, 10.0, 4.0),
        ]
        outputs = [s.draw() for s in shapes]
        assert len(set(outputs)) == 2
