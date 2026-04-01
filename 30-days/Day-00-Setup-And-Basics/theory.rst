Day 00 — Setup and Basics
=========================

Why This Day Matters
--------------------

Before writing meaningful Python you need a reliable foundation: a working
interpreter, an isolated environment for each project, a package manager, and
automated quality gates. Skipping this setup leads to "works on my machine"
bugs and dependency conflicts that are hard to diagnose later.

This day gives you a professional Python workspace that will serve every
subsequent day of the course.


The Python Execution Pipeline
------------------------------

Unlike C++ (compile → link → run), Python is interpreted in two stages::

    Source (.py)
         |
         v
    [ CPython compiler ]  -- parses source, produces bytecode (.pyc)
         |
         v
    [ Python Virtual Machine ]  -- executes bytecode instruction by instruction
         |
         v
    Output / side effects

There is no linker step. Module resolution happens at *import time* (runtime).
The bytecode cache lives in ``__pycache__/`` and is reused when the source
has not changed.


Virtual Environments — Project Isolation
-----------------------------------------

C++ uses separate build trees; Python uses *virtual environments*::

    python3 -m venv .venv           # create
    source .venv/bin/activate       # activate (Linux/macOS)
    .venv\Scripts\activate          # activate (Windows)
    pip install pytest black mypy   # install into the venv only
    deactivate                      # leave the venv

Each project gets its own interpreter symlink and ``site-packages`` directory.
**Always activate your venv before working on a project.**


pyproject.toml — Modern Project Configuration
----------------------------------------------

``pyproject.toml`` is the single source of truth for a Python project (PEP 518,
PEP 621). It replaces ``setup.py``, ``setup.cfg``, ``requirements.txt``:

.. code-block:: toml

    [project]
    name = "my-project"
    version = "0.1.0"
    requires-python = ">=3.11"
    dependencies = ["requests>=2.28"]

    [project.optional-dependencies]
    dev = ["pytest", "black", "mypy", "ruff"]

    [tool.pytest.ini_options]
    testpaths = ["tests"]

    [tool.mypy]
    strict = true

    [tool.black]
    line-length = 88

Install in editable mode: ``pip install -e ".[dev]"``


Running Python Three Ways
--------------------------

(a) **Interactive REPL**::

        python3
        >>> 2 + 2
        4

(b) **Script mode**::

        python3 lesson.py

(c) **Module mode** (``-m`` flag)::

        python3 -m pytest           # run pytest
        python3 -m http.server 8000 # built-in HTTP server
        python3 -m venv .venv       # create venv

The ``-m`` flag locates the named module on ``sys.path``, sets ``__name__ =
"__main__"``, and executes it.  This is why ``python -m pytest`` works even
when ``pytest`` is a package with many sub-modules.


The ``__name__ == "__main__"`` Idiom
--------------------------------------

.. code-block:: python

    def main() -> None:
        print("Hello from main()")

    if __name__ == "__main__":
        main()

When Python **runs** a file directly, ``__name__`` is ``"__main__"``.
When Python **imports** a file, ``__name__`` is the module name (e.g. ``"lesson"``).

This pattern lets a file serve both as a runnable script **and** as an
importable library without executing top-level side effects on import.

C++ has no equivalent — every ``main()`` is a unique entry point.  Python
files are first-class importable modules that can optionally act as scripts.


Dynamic vs Static Typing
--------------------------

+--------------------+----------------------------+----------------------------+
| Feature            | C++                        | Python                     |
+====================+============================+============================+
| Type checking      | Compile time               | Runtime                    |
+--------------------+----------------------------+----------------------------+
| Variable type      | Fixed at declaration       | Can hold any type          |
+--------------------+----------------------------+----------------------------+
| Implicit coercion  | Many (int↔double, etc.)    | Few (no str+int)           |
+--------------------+----------------------------+----------------------------+
| Annotations        | Mandatory                  | Optional (PEP 526)         |
+--------------------+----------------------------+----------------------------+
| Type checker       | Compiler                   | mypy / pyright (external)  |
+--------------------+----------------------------+----------------------------+

Python is *dynamically* typed (types checked at runtime) but *strongly* typed
(no silent coercions between incompatible types).  Type annotations are
optional but strongly recommended — they enable IDE support and static
analysis without changing runtime behaviour.


Key Built-ins for Introspection
--------------------------------

+--------------------+-------------------------------------------------------+
| Function           | Purpose                                               |
+====================+=======================================================+
| ``type(obj)``      | Returns the runtime type of ``obj``                   |
+--------------------+-------------------------------------------------------+
| ``isinstance(o,T)``| True if ``o`` is an instance of ``T`` or subtype     |
+--------------------+-------------------------------------------------------+
| ``issubclass(A,B)``| True if class ``A`` is a subclass of ``B``            |
+--------------------+-------------------------------------------------------+
| ``dir(obj)``       | List of attribute/method names                        |
+--------------------+-------------------------------------------------------+
| ``help(obj)``      | Print docstring documentation                         |
+--------------------+-------------------------------------------------------+
| ``id(obj)``        | Memory address (CPython implementation detail)        |
+--------------------+-------------------------------------------------------+
| ``callable(obj)``  | True if ``obj`` supports ``()`` call syntax           |
+--------------------+-------------------------------------------------------+


Self-Check Questions
--------------------

**Q1: What does ``python3 -m pytest`` do differently from just ``pytest``?**

Using ``-m`` ensures the currently active Python interpreter (and its
``site-packages``) runs pytest, avoiding version mismatch when multiple Python
versions are installed.  It also works even when ``pytest`` is not on ``PATH``.

**Q2: Why should you never install packages with ``pip`` outside a venv?**

Installing globally can break system tools that depend on specific package
versions.  Different projects may require incompatible versions of the same
library.  Venvs provide isolation: each project gets exactly the dependencies
it declared, reproducibly.

**Q3: What is the difference between ``type(x) == int`` and ``isinstance(x, int)``?**

``type(x) == int`` is an exact type check — it returns ``False`` for
subclasses.  ``isinstance(x, int)`` returns ``True`` for any subclass of
``int`` (including ``bool``).  Prefer ``isinstance`` for polymorphic checks;
use ``type()`` equality only when you need to exclude subclasses.

**Q4: What happens if you forget the ``if __name__ == "__main__":`` guard?**

Any top-level code runs immediately when another module imports the file.
This causes unintended side effects: prints, file writes, network calls, or
slow initialisation that run during import.  The guard is the Python
convention for making a file safely importable while still executable as a script.
