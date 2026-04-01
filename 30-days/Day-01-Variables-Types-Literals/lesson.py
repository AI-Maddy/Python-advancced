"""
Day 01 — Variables, Types, and Literals
========================================

Topics:
  - Python built-in types: int, float, complex, bool, str, bytes
  - Dynamic typing vs C++ static typing
  - Type annotations (PEP 526) — optional but recommended
  - None type, truthiness, is vs ==
  - int arbitrary precision (vs C++ fixed-width integers)
  - f-strings, string methods
  - type(), isinstance(), issubclass()
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. Built-in Numeric Types
# ---------------------------------------------------------------------------

def demo_numeric_types() -> None:
    """Show int, float, complex and their properties."""

    # int — arbitrary precision (unlike C++ int which overflows)
    small: int = 42
    big: int = 10 ** 100          # googol — no overflow in Python!
    negative: int = -7

    print(f"small  = {small},  type = {type(small).__name__}")
    print(f"big    = {big}")
    print(f"negative = {negative}")

    # C++ comparison:
    #   int x = INT_MAX; x + 1;   // undefined behaviour (signed overflow)
    # Python:
    import sys
    max_int = sys.maxsize          # platform-dependent but NOT a hard cap
    print(f"sys.maxsize = {max_int}")
    print(f"sys.maxsize + 1 = {max_int + 1}")   # just works!

    # Integer literals
    dec = 255
    hex_val = 0xFF          # hexadecimal
    oct_val = 0o377         # octal
    bin_val = 0b11111111    # binary
    sep_val = 1_000_000     # underscores for readability (PEP 515)
    print(f"decimal={dec}, hex={hex_val}, oct={oct_val}, bin={bin_val}")
    assert dec == hex_val == oct_val == bin_val == 255

    # float — IEEE 754 double precision (64-bit), same as C++ double
    pi: float = 3.14159265358979
    scientific: float = 6.022e23   # Avogadro's number
    print(f"pi={pi}, Avogadro={scientific}")

    # Floating-point precision: identical to C++
    print(0.1 + 0.2)          # 0.30000000000000004 — classic IEEE 754 issue
    print(0.1 + 0.2 == 0.3)   # False — same in C++!

    # Use decimal for exact decimal arithmetic
    from decimal import Decimal
    print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))   # True

    # complex — built into the language (not a library type like in C++)
    z: complex = 3 + 4j
    print(f"z = {z}, real={z.real}, imag={z.imag}, abs={abs(z)}")
    print(f"conjugate: {z.conjugate()}")


# ---------------------------------------------------------------------------
# 2. bool — subtype of int
# ---------------------------------------------------------------------------

def demo_bool() -> None:
    """Show bool's special relationship with int."""
    # bool IS-A int — one of Python's quirks
    print(isinstance(True, int))   # True!
    print(True + True)             # 2
    print(True * 5)                # 5
    print(False + 1)               # 1

    # Boolean literals
    t: bool = True
    f: bool = False

    # Truthiness — Python's "truthy"/"falsy" system
    # Falsy values: False, 0, 0.0, 0j, "", b"", [], (), {}, set(), None
    falsy_values = [False, 0, 0.0, 0j, "", b"", [], (), {}, set(), None]
    for val in falsy_values:
        assert not val, f"{val!r} should be falsy"

    # Truthy: everything else
    truthy_values = [True, 1, -1, 0.001, "x", [0], (None,)]
    for val in truthy_values:
        assert val, f"{val!r} should be truthy"

    # C++ comparison: C++ also has truthiness (0 is false, nonzero is true)
    # Python extends it to all objects via __bool__ or __len__

    # bool() constructor
    print(bool(0))      # False
    print(bool(""))     # False
    print(bool([]))     # False
    print(bool(42))     # True
    print(bool("hi"))   # True


# ---------------------------------------------------------------------------
# 3. None — Python's "null"
# ---------------------------------------------------------------------------

def demo_none() -> None:
    """Show None, its type, and the is vs == distinction."""
    n = None
    print(type(n))               # <class 'NoneType'>
    print(n is None)             # True — correct way to test for None
    print(n == None)             # True — also works but less idiomatic

    # is vs == :
    #   is  checks IDENTITY (same object in memory, like C++ pointer equality)
    #   ==  checks EQUALITY (same value, via __eq__)

    a = [1, 2, 3]
    b = [1, 2, 3]   # different object, same value
    c = a           # same object

    print(a == b)   # True  — same value
    print(a is b)   # False — different objects
    print(a is c)   # True  — same object

    # ALWAYS use 'is' for None checks, never ==
    # The reasons:
    #   1. None is a singleton — there is exactly one None object
    #   2. == can be overloaded; 'is' cannot
    def process(value: int | None = None) -> str:
        if value is None:           # idiomatic
            return "no value"
        return f"got {value}"

    print(process())         # no value
    print(process(0))        # got 0   (0 is falsy but not None!)
    print(process(42))       # got 42


# ---------------------------------------------------------------------------
# 4. str — Unicode strings
# ---------------------------------------------------------------------------

def demo_strings() -> None:
    """Show string literals, methods, and f-strings."""
    # str in Python 3 is always Unicode (unlike C++ char which is bytes)
    # C++ std::string == bytes; Python str == Unicode text

    greeting: str = "Hello, World!"
    multiline: str = """
    Line 1
    Line 2
    """
    raw: str = r"C:\Users\name\file.txt"   # raw: backslashes are literal

    # String methods (str is immutable — all methods return new strings)
    print(greeting.upper())               # HELLO, WORLD!
    print(greeting.lower())               # hello, world!
    print(greeting.replace("World", "Python"))
    print(greeting.split(", "))          # ['Hello', 'World!']
    print("  spaces  ".strip())          # "spaces"
    print("abc".center(9, "-"))          # ---abc---
    print("hello".startswith("he"))      # True
    print("hello".endswith("lo"))        # True
    print(", ".join(["a", "b", "c"]))    # a, b, c

    # f-strings — the recommended way to format strings (Python 3.6+)
    name = "Python"
    version = 3.12
    pi = 3.14159265358979

    print(f"Welcome to {name} {version}!")
    print(f"pi = {pi:.4f}")              # 4 decimal places
    print(f"pi = {pi:.2e}")             # scientific notation
    print(f"42 in hex: {42:#x}")        # 0x2a
    print(f"{'left':<10}|{'right':>10}")
    print(f"{'center':^20}")
    print(f"1 + 1 = {1 + 1}")           # expressions in f-strings

    # Python 3.12: f-string nesting and = for debugging
    x = 42
    print(f"{x=}")      # x=42  — debugging f-string

    # bytes vs str
    text: str = "café"
    encoded: bytes = text.encode("utf-8")   # str → bytes
    decoded: str = encoded.decode("utf-8")  # bytes → str
    print(f"text={text!r}, bytes={encoded!r}, decoded={decoded!r}")
    print(type(encoded))   # <class 'bytes'>


# ---------------------------------------------------------------------------
# 5. Type Annotations (PEP 526)
# ---------------------------------------------------------------------------

def demo_annotations() -> None:
    """Show type annotation syntax — optional but recommended."""
    # Basic variable annotation
    age: int = 25
    price: float = 9.99
    name: str = "Alice"
    active: bool = True

    # Without initial value (declaration only)
    count: int          # declares but doesn't bind — accessing raises NameError

    # Container types (Python 3.9+ built-in syntax)
    names: list[str] = ["Alice", "Bob"]
    scores: dict[str, int] = {"Alice": 95}
    coords: tuple[float, float] = (1.0, 2.0)
    unique: set[int] = {1, 2, 3}

    # Optional (may be None)
    from typing import Optional
    maybe_int: Optional[int] = None          # old style
    maybe_int2: int | None = None            # new style (Python 3.10+)

    # Function annotations
    def greet(name: str, times: int = 1) -> str:
        return (f"Hello, {name}! " * times).strip()

    print(greet("Alice"))
    print(greet("Bob", 3))

    # IMPORTANT: annotations are NOT enforced at runtime by default
    x: int = "this is a string"   # No error at runtime!
    # To get enforcement, use mypy: mypy --strict lesson.py

    # Inspect annotations at runtime
    print(greet.__annotations__)
    # {'name': <class 'str'>, 'times': <class 'int'>, 'return': <class 'str'>}


# ---------------------------------------------------------------------------
# 6. type(), isinstance(), issubclass()
# ---------------------------------------------------------------------------

def demo_type_checks() -> None:
    """Show the three type-checking functions."""

    # type() — exact type (no subclass)
    print(type(42))          # <class 'int'>
    print(type(42) is int)   # True
    print(type(True) is bool) # True
    print(type(True) is int)  # False — exact match, no inheritance

    # isinstance() — includes inheritance (preferred)
    print(isinstance(42, int))       # True
    print(isinstance(True, int))     # True — bool IS-A int
    print(isinstance(True, bool))    # True

    # isinstance with multiple types
    def is_number(x: object) -> bool:
        return isinstance(x, (int, float, complex))

    print(is_number(42))      # True
    print(is_number(3.14))    # True
    print(is_number("hi"))    # False

    # issubclass() — for checking class relationships
    print(issubclass(bool, int))    # True
    print(issubclass(int, object))  # True — everything inherits from object
    print(issubclass(str, int))     # False

    # All Python classes ultimately inherit from object
    class MyClass:
        pass
    print(issubclass(MyClass, object))  # True


if __name__ == "__main__":
    print("=== Numeric Types ===")
    demo_numeric_types()
    print("\n=== Bool ===")
    demo_bool()
    print("\n=== None ===")
    demo_none()
    print("\n=== Strings ===")
    demo_strings()
    print("\n=== Type Annotations ===")
    demo_annotations()
    print("\n=== Type Checks ===")
    demo_type_checks()
