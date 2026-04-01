"""
Tests for Day 08 — Advanced OOP Patterns
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

from solutions import CallableRegistry, JsonPlugin, PluginBase, Vector2D


class TestVector2D:
    def test_repr(self) -> None:
        assert repr(Vector2D(1.0, 2.0)) == "Vector2D(1.0, 2.0)"

    def test_equality(self) -> None:
        assert Vector2D(1.0, 2.0) == Vector2D(1.0, 2.0)
        assert Vector2D(1.0, 2.0) != Vector2D(1.0, 3.0)

    def test_addition(self) -> None:
        assert Vector2D(1.0, 2.0) + Vector2D(3.0, 4.0) == Vector2D(4.0, 6.0)

    def test_subtraction(self) -> None:
        assert Vector2D(3.0, 4.0) - Vector2D(1.0, 2.0) == Vector2D(2.0, 2.0)

    def test_scalar_mul(self) -> None:
        assert Vector2D(1.0, 2.0) * 3 == Vector2D(3.0, 6.0)

    def test_reverse_mul(self) -> None:
        assert 3 * Vector2D(1.0, 2.0) == Vector2D(3.0, 6.0)

    def test_negation(self) -> None:
        assert -Vector2D(1.0, 2.0) == Vector2D(-1.0, -2.0)

    def test_abs_magnitude(self) -> None:
        assert abs(Vector2D(3.0, 4.0)) == pytest.approx(5.0)

    def test_len(self) -> None:
        assert len(Vector2D(1.0, 2.0)) == 2

    def test_indexing(self) -> None:
        v = Vector2D(1.0, 2.0)
        assert v[0] == 1.0
        assert v[1] == 2.0
        with pytest.raises(IndexError):
            _ = v[2]

    def test_contains(self) -> None:
        v = Vector2D(1.0, 2.0)
        assert 1.0 in v
        assert 3.0 not in v

    def test_iter(self) -> None:
        assert list(Vector2D(1.0, 2.0)) == [1.0, 2.0]

    def test_dot_product(self) -> None:
        v1 = Vector2D(1.0, 0.0)
        v2 = Vector2D(0.0, 1.0)
        assert v1 @ v2 == pytest.approx(0.0)

        v3 = Vector2D(1.0, 2.0)
        v4 = Vector2D(3.0, 4.0)
        assert v3 @ v4 == pytest.approx(11.0)

    def test_normalize(self) -> None:
        v = Vector2D(3.0, 4.0)
        n = v.normalize()
        assert abs(n) == pytest.approx(1.0)

    def test_hashable_in_set(self) -> None:
        s = {Vector2D(1.0, 2.0), Vector2D(1.0, 2.0)}
        assert len(s) == 1


class TestCallableRegistry:
    def test_register_and_call(self) -> None:
        reg = CallableRegistry()

        @reg.register("double")
        def double(x: int) -> int:
            return x * 2

        assert reg("double", 5) == 10

    def test_contains(self) -> None:
        reg = CallableRegistry()

        @reg.register("fn")
        def fn() -> None:
            pass

        assert "fn" in reg
        assert "missing" not in reg

    def test_len(self) -> None:
        reg = CallableRegistry()

        @reg.register("a")
        def a() -> None: pass

        @reg.register("b")
        def b() -> None: pass

        assert len(reg) == 2

    def test_missing_key_raises(self) -> None:
        reg = CallableRegistry()
        with pytest.raises(KeyError):
            reg("nonexistent")


class TestPluginBase:
    def test_plugin_registered(self) -> None:
        assert PluginBase.get_plugin("json") is JsonPlugin

    def test_plugin_process(self) -> None:
        plugin_cls = PluginBase.get_plugin("json")
        assert plugin_cls is not None
        result = plugin_cls().process("data")
        assert result == "json:data"

    def test_registry_is_dict(self) -> None:
        reg = PluginBase.registry()
        assert isinstance(reg, dict)
        assert "json" in reg
