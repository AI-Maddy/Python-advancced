"""
Day 00 — Setup and Basics
==========================

Before writing meaningful Python, you need a reliable foundation:
a working interpreter, a virtual environment, a package manager, and
tooling that catches problems before they reach review.

Topics:
  - Python installation, venv, pip, pyproject.toml
  - Running Python: interactive, script, -m flag
  - print(), help(), type(), dir()
  - Python REPL tips
  - __name__ == "__main__" idiom
  - VSCode / PyCharm setup overview
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. The Python Execution Model
# ---------------------------------------------------------------------------
# Unlike C++ (compile → link → run), Python is interpreted:
#
#   Source (.py)
#        |
#        v
#   [ CPython compiler ]  -- parses, produces bytecode (.pyc in __pycache__)
#        |
#        v
#   Bytecode (.pyc)
#        |
#        v
#   [ Python Virtual Machine ]  -- executes bytecode
#        |
#        v
#   Output / side effects
#
# There is no separate linker step. Import resolution happens at runtime.

# ---------------------------------------------------------------------------
# 2. Built-in Introspection Functions
# ---------------------------------------------------------------------------

def demo_builtins() -> None:
    """Demonstrate print, type, isinstance, dir, help."""

    # print() — most flexible output function
    print("Hello, Python!")                          # basic
    print("Pi is approximately", 3.14159)           # multiple args joined by sep
    print("a", "b", "c", sep="-")                   # custom separator: a-b-c
    print("no newline", end="")                     # suppress trailing newline
    print(" — same line")

    # type() — returns the runtime type of any object
    x = 42
    print(type(x))            # <class 'int'>
    print(type("hello"))      # <class 'str'>
    print(type(3.14))         # <class 'float'>
    print(type([1, 2, 3]))    # <class 'list'>
    print(type(None))         # <class 'NoneType'>

    # isinstance() — preferred over type() equality for polymorphism
    print(isinstance(x, int))        # True
    print(isinstance(True, int))     # True — bool IS-A int in Python!
    print(isinstance(x, (int, str))) # True — checks against a tuple of types

    # dir() — list attributes and methods of any object
    sample_list = [1, 2, 3]
    print([m for m in dir(sample_list) if not m.startswith("_")])
    # Shows: append, clear, copy, count, extend, index, insert, pop, remove, reverse, sort

    # id() — memory address of an object (CPython implementation detail)
    a = "hello"
    b = "hello"
    print(id(a), id(b))      # May be the same (string interning)
    print(a is b)            # True for interned strings (CPython detail)

    # help() — interactive documentation; outputs RST-formatted docstring
    # help(str.upper)        # uncomment in REPL to see full docs


# ---------------------------------------------------------------------------
# 3. Python's Type System vs C++
# ---------------------------------------------------------------------------
# C++ is STATICALLY and STRONGLY typed:
#   int x = 5;     // type fixed at compile time
#   x = "hello";   // compile error
#
# Python is DYNAMICALLY and STRONGLY typed:
#   - Dynamic: variables hold references; the type lives on the *object*, not the variable
#   - Strong: no silent coercions between incompatible types (unlike JavaScript)

def demo_dynamic_typing() -> None:
    """Show how Python's dynamic typing differs from C++ static typing."""
    # A variable is a label; the label can be reattached to any object
    x = 42
    print(type(x))    # int
    x = "now I'm a string"  # rebind x to a different type
    print(type(x))    # str
    x = [1, 2, 3]
    print(type(x))    # list

    # Strong typing: Python won't silently coerce
    try:
        result = "3" + 5     # TypeError: can only concatenate str (not "int") to str
    except TypeError as e:
        print(f"TypeError caught: {e}")

    # Explicit conversion is fine
    result = int("3") + 5   # 8


# ---------------------------------------------------------------------------
# 4. Virtual Environments — Python's equivalent of separate project toolchains
# ---------------------------------------------------------------------------
# In the terminal (not in this script):
#
#   python3 -m venv .venv          # Create a virtual environment
#   source .venv/bin/activate      # Activate it (Linux/macOS)
#   .venv\Scripts\activate         # Activate it (Windows)
#   pip install pytest black mypy  # Install packages inside the venv
#   deactivate                     # Leave the venv
#
# WHY: each project gets its own isolated package set.
# Equivalent to having separate build trees in CMake.

# ---------------------------------------------------------------------------
# 5. pyproject.toml — Modern Python project configuration
# ---------------------------------------------------------------------------
# pyproject.toml replaces setup.py, setup.cfg, requirements.txt, tox.ini.
# A minimal example (this is documentation, not executable):
#
#   [project]
#   name = "my-project"
#   version = "0.1.0"
#   requires-python = ">=3.11"
#   dependencies = ["requests>=2.28", "pydantic>=2.0"]
#
#   [project.optional-dependencies]
#   dev = ["pytest", "black", "mypy", "ruff"]
#
#   [tool.pytest.ini_options]
#   testpaths = ["tests"]
#
#   [tool.mypy]
#   strict = true
#
#   [tool.black]
#   line-length = 88
#
#   [tool.ruff]
#   select = ["E", "F", "UP", "B"]
#
# Install the project in editable mode: pip install -e ".[dev]"

# ---------------------------------------------------------------------------
# 6. Running Python Three Ways
# ---------------------------------------------------------------------------
# (a) Interactive REPL:
#       python3
#       >>> 2 + 2
#       4
#       >>> exit()
#
# (b) Script mode:
#       python3 lesson.py
#
# (c) Module mode (-m flag):
#       python3 -m pytest              # runs pytest as a module
#       python3 -m http.server 8000    # built-in HTTP server
#       python3 -m json.tool data.json # pretty-print JSON
#       python3 -m venv .venv          # create venv
#
# The -m flag:
#   1. Locates the named module on sys.path
#   2. Sets __name__ to "__main__"
#   3. Executes it
# This is why `python -m pytest` works even when pytest is a package.

# ---------------------------------------------------------------------------
# 7. The __name__ == "__main__" Idiom
# ---------------------------------------------------------------------------
# When Python imports a module, __name__ is set to the module's name.
# When Python RUNS a file directly, __name__ is set to "__main__".
#
# This lets a file serve BOTH as a runnable script AND an importable module.
#
# C++ equivalent: there is none — every C++ program has exactly one main().
# Python files are first-class importable modules that can optionally act as scripts.

def main() -> None:
    """Entry point when running this file directly."""
    print("=== Day 00: Setup and Basics ===\n")
    demo_builtins()
    print()
    demo_dynamic_typing()
    print()

    # Show __name__ behaviour
    print(f"This module's __name__: {__name__}")
    # If you run `python lesson.py`, this prints: __main__
    # If another file does `import lesson`, this prints: lesson

    # f-strings (Python 3.6+) — preferred string formatting
    name = "Python"
    version = 3.11
    print(f"Welcome to {name} {version}!")
    print(f"2 + 2 = {2 + 2}")
    print(f"pi ≈ {3.14159:.4f}")       # format spec: 4 decimal places
    print(f"{'left':<10}|{'right':>10}")  # alignment

    # Multi-line f-string
    data = {"language": "Python", "paradigm": "multi"}
    print(
        f"Language: {data['language']}\n"
        f"Paradigm: {data['paradigm']}"
    )


# ---------------------------------------------------------------------------
# 8. Tooling Quick Reference
# ---------------------------------------------------------------------------
# Code formatter: black (or ruff format)
#   black lesson.py
#
# Linter/style: ruff (replaces flake8, pylint for most checks)
#   ruff check .
#
# Type checker: mypy or pyright
#   mypy --strict lesson.py
#
# Test runner: pytest
#   pytest tests/
#
# VSCode setup:
#   - Install Python extension (ms-python.python)
#   - Select interpreter: Ctrl+Shift+P → "Python: Select Interpreter" → pick .venv
#   - Install Pylance for IntelliSense (uses pyright under the hood)
#   - Install Black formatter and enable "Format on Save"
#   - .vscode/settings.json:
#       {
#         "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
#         "editor.formatOnSave": true,
#         "[python]": { "editor.defaultFormatter": "ms-python.black-formatter" }
#       }


if __name__ == "__main__":
    main()
