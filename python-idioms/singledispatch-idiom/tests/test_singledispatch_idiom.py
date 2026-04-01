"""pytest tests for singledispatch idiom."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from singledispatch_idiom import (
    Bird,
    Cat,
    Dog,
    Formatter,
    make_sound,
    serialise,
)


class TestSerialise:
    def test_int_dispatch(self) -> None:
        assert serialise(42) == "INT:42"

    def test_float_dispatch(self) -> None:
        assert serialise(3.14) == "FLOAT:3.1400"

    def test_str_dispatch(self) -> None:
        assert serialise("hi") == "STR:'hi'"

    def test_list_dispatch(self) -> None:
        result = serialise([1, 2])
        assert "LIST:" in result
        assert "INT:1" in result

    def test_dict_dispatch(self) -> None:
        result = serialise({"a": 1})
        assert "DICT:" in result

    def test_fallback_for_unknown_type(self) -> None:
        result = serialise(None)
        assert "None" in result

    def test_fallback_for_tuple(self) -> None:
        result = serialise((1, 2))
        assert result == repr((1, 2))


class TestMakeSound:
    def test_dog_sound(self) -> None:
        assert "Woof" in make_sound(Dog("Rex"))

    def test_cat_sound(self) -> None:
        assert "Meow" in make_sound(Cat("Whiskers"))

    def test_bird_sound(self) -> None:
        assert "Tweet" in make_sound(Bird("Tweety"))

    def test_fallback_for_unknown(self) -> None:
        result = make_sound("not an animal")
        assert "???" in result

    def test_correct_name_in_sound(self) -> None:
        assert "Buddy" in make_sound(Dog("Buddy"))


class TestFormatter:
    def setup_method(self) -> None:
        self.fmt = Formatter()

    def test_int_formatted(self) -> None:
        result = self.fmt.format(1_000)
        assert "1,000" in result

    def test_float_formatted(self) -> None:
        result = self.fmt.format(3.14159)
        assert "3.14" in result

    def test_bool_true(self) -> None:
        assert self.fmt.format(True) == "YES"

    def test_bool_false(self) -> None:
        assert self.fmt.format(False) == "NO"

    def test_list_formatted(self) -> None:
        result = self.fmt.format([1, 2.5])
        assert "[" in result
        assert "|" in result

    def test_fallback_for_string(self) -> None:
        result = self.fmt.format("hello")
        assert result == "hello"


class TestDispatchRegistration:
    def test_dispatch_for_int(self) -> None:
        impl = serialise.dispatch(int)
        assert impl is not serialise.dispatch(object)

    def test_dispatch_for_str(self) -> None:
        impl = serialise.dispatch(str)
        assert impl is not serialise.dispatch(object)

    def test_dispatch_for_unknown_is_fallback(self) -> None:
        impl = serialise.dispatch(set)
        # set falls back to the generic object handler
        assert impl == serialise.dispatch(object)
