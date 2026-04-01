"""
Tests for Day 16 — Modules, Packages & Imports
Run with: pytest tests/test_day16.py -v
"""
from __future__ import annotations

import importlib
import sys
import textwrap
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helpers shared across tests
# ---------------------------------------------------------------------------

def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content))


@pytest.fixture()
def tmp_dir(tmp_path: Path) -> Path:
    """A fresh temporary directory for each test."""
    return tmp_path


# ---------------------------------------------------------------------------
# 1. sys.path manipulation
# ---------------------------------------------------------------------------

def test_sys_path_insert(tmp_dir: Path) -> None:
    """Adding a path to sys.path makes modules in that dir importable."""
    (tmp_dir / "mysample.py").write_text("VALUE = 42\n")
    sys.path.insert(0, str(tmp_dir))
    try:
        sys.modules.pop("mysample", None)
        import mysample  # type: ignore[import]
        assert mysample.VALUE == 42
    finally:
        sys.path.remove(str(tmp_dir))
        sys.modules.pop("mysample", None)


# ---------------------------------------------------------------------------
# 2. __all__ behaviour
# ---------------------------------------------------------------------------

def test_all_filters_star_import(tmp_dir: Path) -> None:
    """Names not in __all__ are excluded from 'import *' but still accessible."""
    _write(tmp_dir / "pubmod.py", """\
        __all__ = ["public"]
        def public(): return "pub"
        def _private(): return "priv"
    """)
    sys.path.insert(0, str(tmp_dir))
    try:
        sys.modules.pop("pubmod", None)
        import pubmod  # type: ignore[import]
        assert "public" in pubmod.__all__
        assert "_private" not in pubmod.__all__
        assert pubmod._private() == "priv"  # still accessible
    finally:
        sys.path.remove(str(tmp_dir))
        sys.modules.pop("pubmod", None)


# ---------------------------------------------------------------------------
# 3. importlib.import_module
# ---------------------------------------------------------------------------

def test_dynamic_import_stdlib() -> None:
    """importlib.import_module returns the correct stdlib module."""
    json = importlib.import_module("json")
    assert hasattr(json, "dumps")
    assert json.dumps({"k": 1}) == '{"k": 1}'


# ---------------------------------------------------------------------------
# 4. importlib.util — loading from file path
# ---------------------------------------------------------------------------

def test_import_from_path(tmp_dir: Path) -> None:
    """spec_from_file_location loads a module from an arbitrary path."""
    plugin = tmp_dir / "myplugin.py"
    plugin.write_text("def register(): return lambda x: x * 2\n")

    spec = importlib.util.spec_from_file_location("myplugin", plugin)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]

    fn = mod.register()
    assert fn(21) == 42


# ---------------------------------------------------------------------------
# 5. importlib.reload
# ---------------------------------------------------------------------------

def test_reload_picks_up_changes(tmp_dir: Path) -> None:
    """importlib.reload re-executes the module file."""
    mod_path = tmp_dir / "dynconfig.py"
    mod_path.write_text("VALUE = 1\n")
    sys.path.insert(0, str(tmp_dir))
    try:
        sys.modules.pop("dynconfig", None)
        import dynconfig  # type: ignore[import]
        assert dynconfig.VALUE == 1

        mod_path.write_text("VALUE = 99\n")
        importlib.reload(dynconfig)
        assert dynconfig.VALUE == 99
    finally:
        sys.path.remove(str(tmp_dir))
        sys.modules.pop("dynconfig", None)


# ---------------------------------------------------------------------------
# 6. Package with __init__.py re-export
# ---------------------------------------------------------------------------

def test_package_reexport(tmp_dir: Path) -> None:
    """__init__.py re-exporting makes names available at package level."""
    _write(tmp_dir / "mypkg" / "utils.py", """\
        def greet(name: str) -> str:
            return f"Hello, {name}!"
    """)
    _write(tmp_dir / "mypkg" / "__init__.py", """\
        from .utils import greet
        __all__ = ["greet"]
    """)
    sys.path.insert(0, str(tmp_dir))
    try:
        for key in list(sys.modules.keys()):
            if key.startswith("mypkg"):
                del sys.modules[key]
        from mypkg import greet  # type: ignore[import]
        assert greet("Test") == "Hello, Test!"
    finally:
        sys.path.remove(str(tmp_dir))
        for key in list(sys.modules.keys()):
            if key.startswith("mypkg"):
                del sys.modules[key]


# ---------------------------------------------------------------------------
# 7. Relative import inside package
# ---------------------------------------------------------------------------

def test_relative_import_in_package(tmp_dir: Path) -> None:
    """Relative imports resolve correctly inside a package."""
    _write(tmp_dir / "calc" / "add.py", """\
        def add(a, b):
            return a + b
    """)
    _write(tmp_dir / "calc" / "multiply.py", """\
        from .add import add
        def multiply(a, b):
            result = 0
            for _ in range(b):
                result = add(result, a)
            return result
    """)
    _write(tmp_dir / "calc" / "__init__.py", """\
        from .add import add
        from .multiply import multiply
        __all__ = ["add", "multiply"]
    """)
    sys.path.insert(0, str(tmp_dir))
    try:
        for key in list(sys.modules.keys()):
            if key.startswith("calc"):
                del sys.modules[key]
        from calc import add, multiply  # type: ignore[import]
        assert add(3, 4) == 7
        assert multiply(3, 4) == 12
    finally:
        sys.path.remove(str(tmp_dir))
        for key in list(sys.modules.keys()):
            if key.startswith("calc"):
                del sys.modules[key]
