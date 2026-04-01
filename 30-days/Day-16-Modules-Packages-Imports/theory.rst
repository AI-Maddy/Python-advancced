Day 16 — Modules, Packages & Imports
=====================================

Key Concepts
------------

Module
    A single ``.py`` file.  Every module has a ``__name__`` attribute
    (``"__main__"`` when run directly, otherwise the dotted path).

Package
    A directory containing ``__init__.py`` (regular package) or without one
    (namespace package, PEP 420).

Import Forms
------------

.. code-block:: python

    import os                        # whole module
    import os.path as osp            # alias
    from collections import deque    # selective import
    from . import sibling            # relative (inside package only)
    from ..utils import helper       # relative to parent

Module Search Order (sys.path)
------------------------------

1. The script's own directory (or ``""`` in interactive mode).
2. ``PYTHONPATH`` environment variable entries.
3. Installation-dependent defaults (site-packages, stdlib).

Manipulate at runtime: ``sys.path.insert(0, "/extra/path")``.

``__all__``
-----------

Defines the public API for ``from module import *``.  Names absent from
``__all__`` are still importable by explicit name.

.. code-block:: python

    __all__ = ["PublicClass", "public_fn"]

``__init__.py`` Re-exporting
-----------------------------

Re-export names so callers can use a short import path:

.. code-block:: python

    # package/__init__.py
    from .models import User
    from .utils import slugify
    __all__ = ["User", "slugify"]

Dynamic Import (``importlib``)
------------------------------

.. code-block:: python

    mod = importlib.import_module("json")               # by name string
    spec = importlib.util.spec_from_file_location(...)  # from file path
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    importlib.reload(mod)                               # reload after change

Circular Import Avoidance
--------------------------

* **Local import** — move ``import`` inside the function body.
* **Import module, not name** — ``import pkg.mod`` instead of
  ``from pkg.mod import Name``.
* **TYPE_CHECKING guard** — imports under ``if TYPE_CHECKING:`` are
  invisible at runtime, breaking the cycle for annotation-only needs.

Namespace Packages (PEP 420)
-----------------------------

A directory *without* ``__init__.py`` becomes a namespace package.
Multiple directories on ``sys.path`` can share the same package name,
enabling distributed/split packages across repositories.

Best Practices
--------------

* Keep ``__init__.py`` files small — only re-exports.
* Always define ``__all__`` in public modules.
* Prefer absolute imports in application code; use relative imports inside
  libraries.
* Use ``importlib`` for plugin systems rather than ``eval`` / ``exec``.
* Avoid side effects at module import time (I/O, network calls, heavy
  computation).
