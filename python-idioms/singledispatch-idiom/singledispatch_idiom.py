"""
Singledispatch Idiom — type-based function overloading.

Equivalent to C++ function overloading or tag dispatch.

Demonstrates:
* @functools.singledispatch with fallback
* @<func>.register for additional types
* functools.singledispatchmethod for class methods
"""
from __future__ import annotations

import functools
from dataclasses import dataclass
from functools import singledispatch, singledispatchmethod


# ---------------------------------------------------------------------------
# 1. @singledispatch — serialise any value to a string
# ---------------------------------------------------------------------------
@singledispatch
def serialise(value: object) -> str:
    """Generic fallback: repr of unknown types.

    Args:
        value: Any Python object.

    Returns:
        A string representation.
    """
    return repr(value)


@serialise.register(int)
def _serialise_int(value: int) -> str:
    return f"INT:{value}"


@serialise.register(float)
def _serialise_float(value: float) -> str:
    return f"FLOAT:{value:.4f}"


@serialise.register(str)
def _serialise_str(value: str) -> str:
    return f"STR:{value!r}"


@serialise.register(list)
def _serialise_list(value: list) -> str:
    inner = ", ".join(serialise(item) for item in value)
    return f"LIST:[{inner}]"


@serialise.register(dict)
def _serialise_dict(value: dict) -> str:
    pairs = ", ".join(f"{serialise(k)}: {serialise(v)}" for k, v in value.items())
    return f"DICT:{{{pairs}}}"


# ---------------------------------------------------------------------------
# 2. @singledispatch for type-based processing
# ---------------------------------------------------------------------------
@dataclass
class Dog:
    name: str


@dataclass
class Cat:
    name: str


@dataclass
class Bird:
    name: str


@singledispatch
def make_sound(animal: object) -> str:
    """Fallback for unknown animal types."""
    return f"{animal!r} says ???"


@make_sound.register(Dog)
def _dog_sound(animal: Dog) -> str:
    return f"{animal.name} says Woof!"


@make_sound.register(Cat)
def _cat_sound(animal: Cat) -> str:
    return f"{animal.name} says Meow!"


@make_sound.register(Bird)
def _bird_sound(animal: Bird) -> str:
    return f"{animal.name} says Tweet!"


# ---------------------------------------------------------------------------
# 3. singledispatchmethod for class methods
# ---------------------------------------------------------------------------
class Formatter:
    """Formats different value types using singledispatchmethod."""

    @singledispatchmethod
    def format(self, value: object) -> str:
        """Fallback formatter."""
        return str(value)

    @format.register(int)
    def _format_int(self, value: int) -> str:
        return f"#{value:,d}"

    @format.register(float)
    def _format_float(self, value: float) -> str:
        return f"{value:.2f}"

    @format.register(bool)
    def _format_bool(self, value: bool) -> str:
        return "YES" if value else "NO"

    @format.register(list)
    def _format_list(self, value: list) -> str:
        return "[" + " | ".join(self.format(v) for v in value) + "]"


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # serialise dispatch
    for val in (42, 3.14, "hello", [1, 2.0, "x"], {"a": 1}, None, (1, 2)):
        print(f"  {type(val).__name__:8}: {serialise(val)}")

    # animal sounds
    print()
    for animal in (Dog("Rex"), Cat("Whiskers"), Bird("Tweety"), "not an animal"):
        print(f"  {make_sound(animal)}")

    # singledispatchmethod
    print()
    fmt = Formatter()
    for val in (1_000_000, 3.14159, True, False, [1, 2.5, False]):
        print(f"  {fmt.format(val)}")
