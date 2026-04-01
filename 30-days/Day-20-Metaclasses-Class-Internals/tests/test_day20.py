"""
Tests for Day 20 — Metaclasses & Class Internals
Run with: pytest tests/test_day20.py -v
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import math
from collections import OrderedDict
from typing import Any, ClassVar

import pytest


# ---------------------------------------------------------------------------
# SingletonMeta tests
# ---------------------------------------------------------------------------

class SingletonMeta(type):
    _instances: ClassVar[dict[type, Any]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in SingletonMeta._instances:
            SingletonMeta._instances[cls] = super().__call__(*args, **kwargs)
        return SingletonMeta._instances[cls]


class Config(metaclass=SingletonMeta):
    def __init__(self, value: int = 0) -> None:
        self.value = value


@pytest.fixture(autouse=True)
def clear_singleton_cache() -> None:
    """Reset singleton registry between tests."""
    SingletonMeta._instances.clear()


def test_singleton_same_instance() -> None:
    a = Config()
    b = Config()
    assert a is b


def test_singleton_shared_state() -> None:
    c1 = Config()
    c1.value = 99
    c2 = Config()
    assert c2.value == 99


def test_singleton_different_classes_independent() -> None:
    class AnotherSingleton(metaclass=SingletonMeta):
        pass

    c = Config()
    a = AnotherSingleton()
    assert c is not a


# ---------------------------------------------------------------------------
# RegistryMeta tests
# ---------------------------------------------------------------------------

class RegistryMeta(type):
    def __init__(cls, name: str, bases: tuple[type, ...], ns: dict[str, Any]) -> None:
        super().__init__(name, bases, ns)
        if not hasattr(cls, "_registry"):
            cls._registry: dict[str, type] = {}
        elif not name.startswith("_"):
            cls._registry[name] = cls


class _Animal(metaclass=RegistryMeta):
    def speak(self) -> str:
        raise NotImplementedError

    @classmethod
    def get(cls, name: str) -> type[_Animal]:
        return cls._registry[name]


class Dog(_Animal):
    def speak(self) -> str:
        return "Woof"


class Cat(_Animal):
    def speak(self) -> str:
        return "Meow"


def test_registry_contains_subclasses() -> None:
    assert "Dog" in _Animal._registry
    assert "Cat" in _Animal._registry


def test_registry_excludes_abstract() -> None:
    assert "_Animal" not in _Animal._registry


def test_registry_get_and_instantiate() -> None:
    cls = _Animal.get("Dog")
    assert cls().speak() == "Woof"


def test_registry_missing_raises_key_error() -> None:
    with pytest.raises(KeyError):
        _Animal.get("Fish")


# ---------------------------------------------------------------------------
# OrderedMeta tests
# ---------------------------------------------------------------------------

class OrderedFieldMeta(type):
    @classmethod
    def __prepare__(mcs, name: str, bases: tuple[type, ...], **kw: Any) -> OrderedDict[str, Any]:
        return OrderedDict()

    def __new__(mcs, name: str, bases: tuple[type, ...], ns: OrderedDict[str, Any], **kw: Any) -> OrderedFieldMeta:
        cls = super().__new__(mcs, name, bases, dict(ns))
        cls._field_order: list[str] = [k for k in ns if not k.startswith("__")]
        return cls


class MyForm(metaclass=OrderedFieldMeta):
    alpha: str = ""
    beta: str = ""
    gamma: str = ""


def test_ordered_meta_field_order() -> None:
    assert MyForm._field_order == ["alpha", "beta", "gamma"]


def test_ordered_meta_excludes_dunders() -> None:
    assert "__module__" not in MyForm._field_order
    assert "__qualname__" not in MyForm._field_order


# ---------------------------------------------------------------------------
# __init_subclass__ tests
# ---------------------------------------------------------------------------

class Plugin:
    _plugins: ClassVar[dict[str, type[Plugin]]] = {}

    def __init_subclass__(cls, name: str = "", **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if name:
            Plugin._plugins[name] = cls

    def run(self) -> str:
        raise NotImplementedError


class AlphaPlugin(Plugin, name="alpha"):
    def run(self) -> str:
        return "alpha running"


class BetaPlugin(Plugin, name="beta"):
    def run(self) -> str:
        return "beta running"


def test_init_subclass_registration() -> None:
    assert "alpha" in Plugin._plugins
    assert "beta" in Plugin._plugins


def test_init_subclass_run() -> None:
    p = Plugin._plugins["alpha"]()
    assert p.run() == "alpha running"


def test_init_subclass_unnamed_not_registered() -> None:
    class UnnamedPlugin(Plugin):
        def run(self) -> str:
            return "unnamed"

    assert "UnnamedPlugin" not in Plugin._plugins


# ---------------------------------------------------------------------------
# type() dynamic class creation
# ---------------------------------------------------------------------------

def make_point_class() -> type:
    def _init(self: Any, x: float, y: float) -> None:
        self.x, self.y = x, y

    def _distance(self: Any) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    return type("Point", (object,), {"__init__": _init, "distance": _distance})


def test_dynamic_class_name() -> None:
    Point = make_point_class()
    assert Point.__name__ == "Point"


def test_dynamic_class_instance() -> None:
    Point = make_point_class()
    p = Point(3, 4)  # type: ignore[call-arg]
    assert p.distance() == pytest.approx(5.0)


def test_dynamic_class_is_type_of_type() -> None:
    Point = make_point_class()
    assert type(Point) is type
