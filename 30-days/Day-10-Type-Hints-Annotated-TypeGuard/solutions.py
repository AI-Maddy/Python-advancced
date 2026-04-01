"""Day 10 — Solutions: Type Hints, Annotated, TypeGuard"""
from __future__ import annotations

from typing import Annotated, Final, Literal, TypeAlias, TypeGuard, Union, get_type_hints
import re


# Type aliases
JsonValue: TypeAlias = Union[str, int, float, bool, None, list["JsonValue"], dict[str, "JsonValue"]]
Percentage: TypeAlias = Annotated[float, "must be 0.0-1.0"]

# Final constants
MAX_RETRIES: Final[int] = 3
DEFAULT_HOST: Final[str] = "localhost"


# TypeGuard for type narrowing
def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    """Return True iff every element in val is a str."""
    return all(isinstance(x, str) for x in val)


def is_positive_int(val: object) -> TypeGuard[int]:
    """Return True iff val is a positive integer."""
    return isinstance(val, int) and not isinstance(val, bool) and val > 0


# Annotated for validation metadata
PositiveFloat = Annotated[float, "positive", lambda x: x > 0]
EmailStr = Annotated[str, "email", re.compile(r"[^@]+@[^@]+\.[^@]+")]


def parse_status(status: Literal["active", "inactive", "pending"]) -> str:
    """Accept only specific string literals."""
    return f"Status is: {status}"


def format_percentage(value: Percentage) -> str:
    """Format a 0.0-1.0 percentage as human-readable."""
    return f"{value * 100:.1f}%"


def narrow_and_process(items: list[object]) -> list[str]:
    """Use TypeGuard to narrow list[object] to list[str]."""
    if is_str_list(items):
        return [s.upper() for s in items]  # s is str here
    return [str(item) for item in items]


if __name__ == "__main__":
    print(parse_status("active"))
    print(format_percentage(0.75))
    print(narrow_and_process(["hello", "world"]))
    print(narrow_and_process([1, 2, 3]))
    print(is_positive_int(5))
    print(is_positive_int(-1))
    print(is_positive_int(True))  # False — excluded bools
