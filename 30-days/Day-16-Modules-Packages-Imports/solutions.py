"""
Day 16 — Solutions: Modules, Packages & Imports
=================================================
Run with: python solutions.py
"""
from __future__ import annotations

import importlib
import importlib.util
import sys
import textwrap
import types
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Helper — write a file creating parent dirs
# ---------------------------------------------------------------------------

def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content))


# ---------------------------------------------------------------------------
# Solution 1 — sub-package with re-export
# ---------------------------------------------------------------------------

def exercise1_sub_package() -> str:
    """Create mypkg, import greet from it, return greeting."""
    import tempfile
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
# Solution 2 — relative import across modules
# ---------------------------------------------------------------------------

def exercise2_relative_import() -> tuple[int, int]:
    """Create calc package with relative import in multiply.py."""
    import tempfile
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
# Solution 3 — plugin loader with importlib
# ---------------------------------------------------------------------------

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
    """Load upper and reverse plugins, apply to 'hello'."""
    import tempfile
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
# Solution 4 — sys.path + __all__
# ---------------------------------------------------------------------------

def exercise4_all_and_syspath() -> int:
    """Create mymath module, load via sys.path, return square(5)."""
    import tempfile
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
# Solution 5 — importlib.reload
# ---------------------------------------------------------------------------

def exercise5_reload() -> int:
    """Demonstrate importlib.reload() after file change."""
    import tempfile
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
# Run all
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Solution 1:", exercise1_sub_package())
    print("Solution 2:", exercise2_relative_import())
    print("Solution 3:", exercise3_plugin_loader())
    print("Solution 4:", exercise4_all_and_syspath())
    print("Solution 5:", exercise5_reload())
