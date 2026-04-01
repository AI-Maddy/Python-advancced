"""Day 10 — Exercises"""
from __future__ import annotations
from typing import Annotated, Final, Literal, TypeAlias, TypeGuard

# Ex 1: is_str_list TypeGuard
def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    pass  # TODO

# Ex 2: is_positive_int TypeGuard (exclude bool)
def is_positive_int(val: object) -> TypeGuard[int]:
    pass  # TODO

# Ex 3: TypeAlias for JsonValue (recursive)
from typing import Union
JsonValue: TypeAlias = Union[str, int, float, bool, None, list["JsonValue"], dict[str, "JsonValue"]]  # already done

# Ex 4: parse_status with Literal type
def parse_status(status: Literal["active", "inactive", "pending"]) -> str:
    pass  # TODO

# Ex 5: format_percentage with Annotated type
Percentage = Annotated[float, "0.0 to 1.0"]
def format_percentage(value: Percentage) -> str:
    pass  # TODO: f"{value * 100:.1f}%"

if __name__ == "__main__":
    print(is_str_list(["a", "b"]))
    print(is_positive_int(5))
