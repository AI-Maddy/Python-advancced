"""
Day 16 — Exercises: Modules, Packages & Imports
=================================================
Complete each TODO.  Run with: python exercises.py
"""
from __future__ import annotations

import importlib
import importlib.util
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Exercise 1 — Create a sub-package and use relative import
# ---------------------------------------------------------------------------
# TODO:
#   a) In a temporary directory, create the following layout:
#        mypkg/__init__.py      — re-exports 'greet' from .utils
#        mypkg/utils.py         — defines greet(name: str) -> str
#   b) Add the temporary directory to sys.path.
#   c) Import 'greet' from 'mypkg' and call it.
#
# Hint: use textwrap.dedent + Path.write_text to create the files.

def exercise1_sub_package() -> str:
    """
    Dynamically create a sub-package, import from it, and return the greeting.
    Should return "Hello, World!"
    """
    # TODO: implement
    ...
    return ""


# ---------------------------------------------------------------------------
# Exercise 2 — Relative import simulation
# ---------------------------------------------------------------------------
# TODO:
#   Create a package 'calc' with:
#       calc/__init__.py  → re-exports add, multiply
#       calc/add.py       → def add(a, b): return a + b
#       calc/multiply.py  → def multiply(a, b): return a * b
#   (multiply.py should import 'add' using a relative import: from .add import add)
#   Load the package and verify multiply(3, 4) == 12 and add(3, 4) == 7.

def exercise2_relative_import() -> tuple[int, int]:
    """
    Return (add_result, multiply_result) for inputs (3, 4).
    Expected: (7, 12)
    """
    # TODO: implement
    ...
    return (0, 0)


# ---------------------------------------------------------------------------
# Exercise 3 — Plugin loader with importlib
# ---------------------------------------------------------------------------
# TODO:
#   a) Create two plugin files in a temp directory:
#        plugin_upper.py  — register() returns a callable that uppercases a string
#        plugin_reverse.py — register() returns a callable that reverses a string
#   b) Implement a load_plugin(path: Path, name: str) -> callable function using
#      importlib.util.spec_from_file_location.
#   c) Load both plugins and apply them to the string "hello".

def load_plugin(path: Path, name: str) -> Any:
    """Load a plugin .py file and return result of its register() function."""
    # TODO: implement using importlib.util
    ...

def exercise3_plugin_loader() -> tuple[str, str]:
    """
    Return (upper_result, reverse_result) for input "hello".
    Expected: ("HELLO", "olleh")
    """
    # TODO: implement
    ...
    return ("", "")


# ---------------------------------------------------------------------------
# Exercise 4 — sys.path manipulation + __all__
# ---------------------------------------------------------------------------
# TODO:
#   a) Create a module 'mymath.py' in a temp directory with:
#        __all__ = ["square"]
#        def square(n): return n * n
#        def _cube(n): return n ** 3   # private
#   b) Add the temp dir to sys.path, import mymath.
#   c) Verify that dir(mymath) contains 'square' and that _cube is accessible
#      by name but not listed in __all__.
#   d) Return the result of mymath.square(5).

def exercise4_all_and_syspath() -> int:
    """
    Create module, load via sys.path, return square(5).
    Expected: 25
    """
    # TODO: implement
    ...
    return 0


# ---------------------------------------------------------------------------
# Exercise 5 — importlib.reload demo
# ---------------------------------------------------------------------------
# TODO:
#   a) Create a module 'config.py' in a temp directory with: VALUE = 1
#   b) Import it, verify VALUE == 1.
#   c) Overwrite config.py with VALUE = 99.
#   d) Use importlib.reload() to reload the module.
#   e) Verify VALUE == 99 after reload.
#   f) Return the reloaded VALUE.

def exercise5_reload() -> int:
    """
    Demonstrate importlib.reload().  Return reloaded VALUE (expected: 99).
    """
    # TODO: implement
    ...
    return 0


# ---------------------------------------------------------------------------
# Run all exercises
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_sub_package())
    print("Exercise 2:", exercise2_relative_import())
    print("Exercise 3:", exercise3_plugin_loader())
    print("Exercise 4:", exercise4_all_and_syspath())
    print("Exercise 5:", exercise5_reload())
