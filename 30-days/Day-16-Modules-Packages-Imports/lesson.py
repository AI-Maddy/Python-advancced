"""
Day 16 — Modules, Packages & Imports
=====================================
Topics:
  - import, from ... import, import as
  - __all__, __init__.py re-exporting
  - Relative imports, importlib dynamic import
  - Circular import avoidance patterns
  - sys.path, namespace packages
"""
from __future__ import annotations

import importlib
import importlib.util
import sys
import types
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. Basic import forms
# ---------------------------------------------------------------------------

# Standard library — plain import
import os
import os.path as osp           # alias with 'as'

from collections import OrderedDict, defaultdict   # selective import
from typing import Any

def demo_basic_imports() -> None:
    """Show the three basic import styles."""
    # 1) import module
    cwd = os.getcwd()

    # 2) import module as alias
    home = osp.expanduser("~")

    # 3) from module import name
    od: OrderedDict[str, int] = OrderedDict(a=1, b=2)
    dd: defaultdict[str, list[int]] = defaultdict(list)
    dd["x"].append(42)

    print(f"cwd={cwd!r}  home={home!r}  od={dict(od)}  dd={dict(dd)}")


# ---------------------------------------------------------------------------
# 2. __all__ — controls 'from module import *'
# ---------------------------------------------------------------------------
# In a real module file you would define:
#
#   __all__ = ["PublicClass", "public_function"]
#
# Anything not listed is still importable by name, but 'import *' skips it.
# Defining __all__ is considered good practice; it documents the public API.

def _private_helper() -> str:
    """Not exported via __all__."""
    return "internal"

def public_function() -> str:
    """Exported via __all__."""
    return "public"

__all__ = ["public_function", "demo_basic_imports"]


# ---------------------------------------------------------------------------
# 3. sys.path — where Python looks for modules
# ---------------------------------------------------------------------------

def inspect_sys_path() -> None:
    """Print current module search path."""
    print("sys.path entries:")
    for i, p in enumerate(sys.path):
        print(f"  [{i}] {p}")

def temporarily_add_path(directory: str) -> None:
    """Demonstrate adding a directory to sys.path at runtime."""
    if directory not in sys.path:
        sys.path.insert(0, directory)
        print(f"Added {directory!r} to sys.path[0]")
    else:
        print(f"{directory!r} already in sys.path")


# ---------------------------------------------------------------------------
# 4. importlib — dynamic imports
# ---------------------------------------------------------------------------

def dynamic_import(module_name: str) -> types.ModuleType:
    """Import a module by string name at runtime."""
    mod = importlib.import_module(module_name)
    print(f"Dynamically imported: {mod.__name__} (file: {getattr(mod, '__file__', 'built-in')})")
    return mod


def import_from_path(module_name: str, file_path: Path) -> types.ModuleType:
    """
    Load a .py file as a module without it being on sys.path.
    Useful for plugin loaders.
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot find module spec for {file_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod          # register so relative imports work
    spec.loader.exec_module(mod)            # type: ignore[union-attr]
    return mod


# ---------------------------------------------------------------------------
# 5. Circular import avoidance patterns
# ---------------------------------------------------------------------------
# Problem: module A imports B, B imports A → ImportError or partial module.
#
# Pattern 1 — Local (deferred) import:
#   def func():
#       from . import heavy_module    # import happens only when func() runs
#       return heavy_module.do()
#
# Pattern 2 — Import the *module*, not the name:
#   import package.submodule          # OK even if submodule imports package
#   package.submodule.SomeClass()
#
# Pattern 3 — TYPE_CHECKING guard (avoids runtime circular, keeps type info):
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from collections.abc import Sequence  # only imported by type-checkers

def process(items: "Sequence[int]") -> int:
    """Uses forward reference string to avoid runtime import."""
    return sum(items)


# ---------------------------------------------------------------------------
# 6. Namespace packages (PEP 420)
# ---------------------------------------------------------------------------
# A directory WITHOUT __init__.py is a "namespace package".
# Multiple directories on sys.path can contribute to the same package name.
# Useful for splitting a large project across repos.
#
# Example layout (no __init__.py needed):
#
#   repo_a/myns/plugin_a.py
#   repo_b/myns/plugin_b.py
#
# Both directories on sys.path → `import myns.plugin_a` and
# `import myns.plugin_b` both work, sharing the 'myns' namespace.

def demo_namespace_package_concept() -> None:
    """Explain namespace packages without creating files."""
    print(
        "Namespace packages: a directory without __init__.py.\n"
        "Multiple sys.path roots can contribute sub-modules to the same\n"
        "top-level package name (PEP 420 / PEP 382)."
    )


# ---------------------------------------------------------------------------
# 7. __init__.py re-exporting
# ---------------------------------------------------------------------------
# Inside a package's __init__.py you can re-export names so callers use:
#   from mypackage import SomeClass
# instead of:
#   from mypackage.submodule import SomeClass
#
# Example __init__.py content:
#
#   from .models import User, Product      # re-export
#   from .utils import slugify
#   __all__ = ["User", "Product", "slugify"]


# ---------------------------------------------------------------------------
# 8. Simulated plugin loader using importlib
# ---------------------------------------------------------------------------

class PluginLoader:
    """
    Dynamically discover and load plugins from a directory.

    Each plugin file must expose a ``register()`` function that returns a
    callable or object implementing the plugin interface.
    """

    def __init__(self, plugin_dir: Path) -> None:
        self.plugin_dir = plugin_dir
        self._plugins: dict[str, Any] = {}

    def discover(self) -> list[str]:
        """Return names of all .py files in the plugin directory."""
        return [p.stem for p in self.plugin_dir.glob("*.py") if p.stem != "__init__"]

    def load(self, name: str) -> Any:
        """Load plugin by name and cache it."""
        if name in self._plugins:
            return self._plugins[name]
        file_path = self.plugin_dir / f"{name}.py"
        mod = import_from_path(f"plugins.{name}", file_path)
        plugin = mod.register()   # convention: each plugin exports register()
        self._plugins[name] = plugin
        print(f"Loaded plugin {name!r}: {plugin}")
        return plugin

    def load_all(self) -> dict[str, Any]:
        """Load every discovered plugin."""
        for name in self.discover():
            self.load(name)
        return dict(self._plugins)


# ---------------------------------------------------------------------------
# 9. Relative imports (conceptual, can't run in __main__)
# ---------------------------------------------------------------------------
# Inside a package:
#   from . import sibling_module        # same package
#   from .. import parent_module        # parent package
#   from ..other import SomeClass       # sibling of parent
#
# Relative imports only work inside packages (not in scripts run directly).
# Use 'python -m package.module' to enable relative imports in scripts.


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Day 16 — Modules, Packages & Imports")
    print("=" * 60)

    print("\n--- Basic imports ---")
    demo_basic_imports()

    print("\n--- sys.path (first 5 entries) ---")
    for entry in sys.path[:5]:
        print(f"  {entry!r}")

    print("\n--- Dynamic import of 'json' ---")
    json_mod = dynamic_import("json")
    result = json_mod.dumps({"day": 16, "topic": "imports"})
    print(f"json.dumps result: {result}")

    print("\n--- Namespace packages ---")
    demo_namespace_package_concept()

    print("\n--- __all__ demo ---")
    print(f"Exported names: {__all__}")
    print(f"Private helper still callable: {_private_helper()}")

    print("\n--- PluginLoader (no real directory) ---")
    # Would work with a real directory containing plugin .py files:
    # loader = PluginLoader(Path("/tmp/plugins"))
    # loader.load_all()
    print("PluginLoader class defined — see exercises for hands-on use.")

    print("\nDone!")
