"""
Tests for Day 07 — ABCs, Protocols, and Duck Typing
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import math
import pytest

from solutions import (
    Drawable,
    LegacyPrinter,
    ManuallyRegistered,
    Printable,
    Priority,
    Sortable,
    SVGCircle,
    SVGRect,
    Temperature,
    render_all,
)


class TestDrawableProtocol:
    def test_svg_circle_is_drawable(self) -> None:
        assert isinstance(SVGCircle(5.0), Drawable)

    def test_svg_rect_is_drawable(self) -> None:
        assert isinstance(SVGRect(3.0, 4.0), Drawable)

    def test_circle_draw(self) -> None:
        c = SVGCircle(5.0)
        result = c.draw()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_circle_area(self) -> None:
        c = SVGCircle(5.0)
        assert c.area() == pytest.approx(math.pi * 25)

    def test_rect_area(self) -> None:
        r = SVGRect(3.0, 4.0)
        assert r.area() == pytest.approx(12.0)

    def test_render_all(self) -> None:
        shapes: list[Drawable] = [SVGCircle(1.0), SVGRect(2.0, 3.0)]
        results = render_all(shapes)
        assert len(results) == 2
        assert all(isinstance(r, str) for r in results)

    def test_non_drawable_not_instance(self) -> None:
        class NotDrawable:
            pass
        assert not isinstance(NotDrawable(), Drawable)


class TestSortableABC:
    def test_temperature_sorted(self) -> None:
        temps = [Temperature(100), Temperature(-10), Temperature(37)]
        sorted_temps = sorted(temps)
        values = [t.celsius for t in sorted_temps]
        assert values == [-10, 37, 100]

    def test_temperature_lt(self) -> None:
        assert Temperature(0) < Temperature(100)

    def test_temperature_gt(self) -> None:
        assert Temperature(100) > Temperature(0)

    def test_temperature_equality(self) -> None:
        assert Temperature(37) == Temperature(37)

    def test_priority_sorted(self) -> None:
        priorities = [Priority("high"), Priority("low"), Priority("critical")]
        sorted_prio = sorted(priorities)
        names = [p.name for p in sorted_prio]
        assert names == ["low", "high", "critical"]

    def test_cannot_instantiate_sortable(self) -> None:
        with pytest.raises(TypeError):
            Sortable()  # type: ignore[abstract]


class TestPrintableVirtualSubclass:
    def test_legacy_printer_is_printable(self) -> None:
        """__subclasshook__ recognises LegacyPrinter via print_me method."""
        printer = LegacyPrinter()
        assert isinstance(printer, Printable)

    def test_manually_registered_is_printable(self) -> None:
        manual = ManuallyRegistered()
        assert isinstance(manual, Printable)

    def test_class_without_print_me_not_printable(self) -> None:
        class NoMethod:
            pass
        assert not isinstance(NoMethod(), Printable)

    def test_legacy_print_me_returns_string(self) -> None:
        result = LegacyPrinter().print_me()
        assert isinstance(result, str)
