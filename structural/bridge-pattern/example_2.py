"""
Example 2 — Shape + rendering engine.

Shows how adding a new renderer (PrintRenderer) requires zero changes to
Shape subclasses, demonstrating open/closed principle via the bridge.
"""
from __future__ import annotations

from bridge import AsciiRenderer, Circle, RasterRenderer, Rectangle, VectorRenderer


def main() -> None:
    shapes_by_renderer = [
        ("Vector", VectorRenderer()),
        ("Raster", RasterRenderer()),
        ("ASCII", AsciiRenderer()),
    ]

    for label, renderer in shapes_by_renderer:
        print(f"\n--- {label} ---")
        shapes = [
            Circle(renderer, 5.0),
            Circle(renderer, 10.0),
            Rectangle(renderer, 8.0, 3.0),
        ]
        for shape in shapes:
            print(" ", shape.draw())
        # Resize and redraw
        shapes[0].resize(2.0)
        print("  After resize:", shapes[0].draw())


if __name__ == "__main__":
    main()
