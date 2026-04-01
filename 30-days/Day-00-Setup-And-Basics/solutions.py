"""
Day 00 — Solutions
==================
"""
from __future__ import annotations

from datetime import date


# ---------------------------------------------------------------------------
# Exercise 1
# ---------------------------------------------------------------------------

def explore_object(obj: object) -> None:
    """Print type info and first 5 public attributes of obj."""
    print(f"Type       : {type(obj)}")
    print(f"Is numeric : {isinstance(obj, (int, float, complex))}")
    public_attrs = [a for a in dir(obj) if not a.startswith("_")][:5]
    print(f"First 5 attrs: {public_attrs}")
    print()


# ---------------------------------------------------------------------------
# Exercise 2
# ---------------------------------------------------------------------------

def hello_world(name: str) -> str:
    """Return a greeting string with today's date embedded."""
    today = date.today()
    return f"Hello, {name}! Today is {today.strftime('%A, %B %d %Y')}."


# ---------------------------------------------------------------------------
# Exercise 3
# ---------------------------------------------------------------------------

def compute_square(n: int) -> int:
    """Return n squared."""
    return n * n


# ---------------------------------------------------------------------------
# Exercise 4
# ---------------------------------------------------------------------------

def introspect(obj: object) -> dict[str, object]:
    """Return an introspection report dict for obj."""
    return {
        "type_name": type(obj).__name__,
        "is_numeric": isinstance(obj, (int, float, complex)),
        "public_attrs": [a for a in dir(obj) if not a.startswith("_")],
        "callable": callable(obj),
    }


# ---------------------------------------------------------------------------
# Exercise 5 (no code — hands-on only)
# ---------------------------------------------------------------------------
PYTEST_VERSION: str = "see: python -m pytest --version"


if __name__ == "__main__":
    explore_object(42)
    explore_object("hello")
    explore_object([1, 2, 3])

    print(hello_world("Student"))

    for i in range(1, 6):
        print(f"{i}^2 = {compute_square(i)}")

    report = introspect(3.14)
    for k, v in report.items():
        print(f"  {k}: {v}")
