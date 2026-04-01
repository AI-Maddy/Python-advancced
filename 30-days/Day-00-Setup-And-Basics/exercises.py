"""
Day 00 — Exercises
==================

Work through these exercises to cement today's concepts.
Replace each TODO with working code.
"""
from __future__ import annotations


# ---------------------------------------------------------------------------
# Exercise 1: REPL Exploration
# ---------------------------------------------------------------------------
# Run the following in a Python REPL (python3) and record what you learn:
#   type(True)        — what is the type of a boolean?
#   isinstance(True, int)   — is bool a subtype of int?
#   dir([])           — how many methods does a list have?
#   help(str.split)   — what does str.split() do?
#
# Then write a function that takes any object and prints:
#   - Its type
#   - Whether it is an instance of (int, float, complex)
#   - The first 5 non-dunder attributes from dir()

def explore_object(obj: object) -> None:
    """Print type info and first 5 public attributes of obj."""
    # TODO: print type(obj)
    # TODO: print whether obj is numeric (isinstance check with tuple of types)
    # TODO: collect non-dunder names from dir(obj), print first 5
    pass


# ---------------------------------------------------------------------------
# Exercise 2: Hello World Script
# ---------------------------------------------------------------------------
# Write a function that prints a personalised greeting.
# It should use an f-string and include the current date.
# Hint: from datetime import date; date.today()

def hello_world(name: str) -> str:
    """Return a greeting string with today's date embedded.

    Example:
        >>> msg = hello_world("Alice")
        >>> "Alice" in msg
        True
    """
    # TODO: import date from datetime
    # TODO: build and return an f-string greeting including name and today's date
    pass


# ---------------------------------------------------------------------------
# Exercise 3: __name__ Guard
# ---------------------------------------------------------------------------
# Finish the module below so that:
#   - When imported, `compute_square(n)` can be called without side effects
#   - When run directly, it prints the squares of 1–5

def compute_square(n: int) -> int:
    """Return n squared."""
    # TODO: implement
    pass


# The guard should be at the bottom of the file:
# if __name__ == "__main__":
#     for i in range(1, 6):
#         print(f"{i}^2 = {compute_square(i)}")


# ---------------------------------------------------------------------------
# Exercise 4: Introspection Report
# ---------------------------------------------------------------------------
# Write `introspect(obj)` that returns a dict with keys:
#   "type_name"  : str  — name of the type (e.g. "int")
#   "is_numeric" : bool — True if int, float, or complex
#   "public_attrs": list[str] — non-dunder attribute names
#   "callable"   : bool — whether the object is callable

def introspect(obj: object) -> dict[str, object]:
    """Return an introspection report dict for obj."""
    # TODO: build and return the dict described above
    pass


# ---------------------------------------------------------------------------
# Exercise 5: Virtual Environment Checklist
# ---------------------------------------------------------------------------
# This is a hands-on exercise (no code to write):
#
# 1. Open a terminal in this project directory.
# 2. Run: python3 -m venv .venv
# 3. Activate it: source .venv/bin/activate  (Linux/macOS)
#                 .venv\Scripts\activate     (Windows)
# 4. Run: pip install pytest black mypy
# 5. Verify: python -m pytest --version
# 6. Run this exercise file: python exercises.py
# 7. Run the tests: python -m pytest tests/test_day00.py -v
#
# Record the pytest version here (as a string constant):
PYTEST_VERSION: str = "TODO: replace with actual version string"


if __name__ == "__main__":
    # Quick smoke tests of your implementations
    explore_object(42)
    explore_object("hello")
    explore_object([1, 2, 3])

    print(hello_world("Student"))

    for i in range(1, 6):
        sq = compute_square(i)
        print(f"{i}^2 = {sq}")

    report = introspect(3.14)
    print(report)
