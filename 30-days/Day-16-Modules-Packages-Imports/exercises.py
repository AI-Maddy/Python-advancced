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
# Helper — write a file creating parent dirs
# ---------------------------------------------------------------------------

def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content))


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
    tmp = Path(tempfile.mkdtemp())

    _write(tmp / "mypkg" / "utils.py", """\
        from __future__ import annotations
        def greet(name: str) -> str:
            return f"Hello, {name}!"
    """)
    _write(tmp / "mypkg" / "__init__.py", """\
        from .utils import greet
        __all__ = ["greet"]
    """)

    if str(tmp) not in sys.path:
        sys.path.insert(0, str(tmp))

    # Force fresh import in case module cached
    for key in list(sys.modules.keys()):
        if key.startswith("mypkg"):
            del sys.modules[key]

    from mypkg import greet  # type: ignore[import]
    result = greet("World")
    # Clean up sys.path
    sys.path.remove(str(tmp))
    return result


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
    tmp = Path(tempfile.mkdtemp())

    _write(tmp / "calc" / "add.py", """\
        from __future__ import annotations
        def add(a: int, b: int) -> int:
            return a + b
    """)
    _write(tmp / "calc" / "multiply.py", """\
        from __future__ import annotations
        from .add import add
        def multiply(a: int, b: int) -> int:
            result = 0
            for _ in range(b):
                result = add(result, a)
            return result
    """)
    _write(tmp / "calc" / "__init__.py", """\
        from .add import add
        from .multiply import multiply
        __all__ = ["add", "multiply"]
    """)

    if str(tmp) not in sys.path:
        sys.path.insert(0, str(tmp))

    for key in list(sys.modules.keys()):
        if key.startswith("calc"):
            del sys.modules[key]

    from calc import add, multiply  # type: ignore[import]
    add_result = add(3, 4)
    mul_result = multiply(3, 4)
    sys.path.remove(str(tmp))
    return (add_result, mul_result)


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
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod.register()

def exercise3_plugin_loader() -> tuple[str, str]:
    """
    Return (upper_result, reverse_result) for input "hello".
    Expected: ("HELLO", "olleh")
    """
    tmp = Path(tempfile.mkdtemp())

    _write(tmp / "plugin_upper.py", """\
        def register():
            return str.upper
    """)
    _write(tmp / "plugin_reverse.py", """\
        def register():
            return lambda s: s[::-1]
    """)

    upper_fn = load_plugin(tmp / "plugin_upper.py", "plugin_upper")
    reverse_fn = load_plugin(tmp / "plugin_reverse.py", "plugin_reverse")

    text = "hello"
    return (upper_fn(text), reverse_fn(text))


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
    tmp = Path(tempfile.mkdtemp())

    _write(tmp / "mymath.py", """\
        from __future__ import annotations
        __all__ = ["square"]

        def square(n: int) -> int:
            return n * n

        def _cube(n: int) -> int:
            return n ** 3
    """)

    if str(tmp) not in sys.path:
        sys.path.insert(0, str(tmp))

    # Remove cached version if present
    sys.modules.pop("mymath", None)
    import mymath  # type: ignore[import]

    assert "square" in mymath.__all__, "square should be in __all__"
    assert "_cube" not in mymath.__all__, "_cube should NOT be in __all__"
    assert callable(mymath._cube), "_cube still accessible by name"

    result = mymath.square(5)
    sys.path.remove(str(tmp))
    return result


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
    tmp = Path(tempfile.mkdtemp())
    mod_path = tmp / "config.py"

    mod_path.write_text("VALUE = 1\n")
    if str(tmp) not in sys.path:
        sys.path.insert(0, str(tmp))
    sys.modules.pop("config", None)

    import config  # type: ignore[import]
    assert config.VALUE == 1

    # Overwrite the file
    mod_path.write_text("VALUE = 99\n")

    # Reload
    importlib.reload(config)
    assert config.VALUE == 99

    sys.path.remove(str(tmp))
    return config.VALUE


# ---------------------------------------------------------------------------
# Run all exercises
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_sub_package())
    print("Exercise 2:", exercise2_relative_import())
    print("Exercise 3:", exercise3_plugin_loader())
    print("Exercise 4:", exercise4_all_and_syspath())
    print("Exercise 5:", exercise5_reload())
