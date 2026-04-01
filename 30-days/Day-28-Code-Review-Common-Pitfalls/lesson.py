"""
Day 28 — Code Review: Common Python Pitfalls
==============================================
Each section shows the BUGGY code, explains WHY it's wrong,
then shows the FIX.
"""
from __future__ import annotations

from typing import Any


print("=" * 60)
print("Day 28 — Common Python Pitfalls")
print("=" * 60)

# ===========================================================================
# Pitfall 1: Mutable Default Argument
# ===========================================================================
print("\n--- Pitfall 1: Mutable Default Argument ---")

# BAD — the list [] is created ONCE at function definition time,
# and shared across ALL calls that don't pass an explicit argument.

def append_to_BAD(item: int, result: list[int] = []) -> list[int]:  # noqa: B006
    """BUGGY: shared mutable default."""
    result.append(item)
    return result

print("Bad version:")
print(append_to_BAD(1))   # [1]
print(append_to_BAD(2))   # [1, 2] — surprise! not [2]
print(append_to_BAD(3))   # [1, 2, 3]

# FIX — use None as sentinel, create fresh list inside the function.

def append_to_GOOD(item: int, result: list[int] | None = None) -> list[int]:
    """FIXED: use None sentinel."""
    if result is None:
        result = []
    result.append(item)
    return result

print("Good version:")
print(append_to_GOOD(1))  # [1]
print(append_to_GOOD(2))  # [2]
print(append_to_GOOD(3))  # [3]


# ===========================================================================
# Pitfall 2: Late Binding Closure
# ===========================================================================
print("\n--- Pitfall 2: Late Binding Closure ---")

# BAD — all lambdas capture the variable `i`, NOT its value at creation time.
# By the time the lambda is called, the loop has finished and i == 4.

bad_funcs = [lambda: i for i in range(5)]
print("Bad lambdas (all return 4):", [f() for f in bad_funcs])

# FIX 1 — capture current value via default argument.
good_funcs = [lambda i=i: i for i in range(5)]
print("Good lambdas (default arg):", [f() for f in good_funcs])

# FIX 2 — use functools.partial.
import functools
good_funcs2 = [functools.partial(lambda i: i, i) for i in range(5)]
print("Good lambdas (partial):    ", [f() for f in good_funcs2])


# ===========================================================================
# Pitfall 3: `is` vs `==` for Strings
# ===========================================================================
print("\n--- Pitfall 3: 'is' vs '==' for strings ---")

# BAD — `is` checks object identity, not equality.
# String interning is an implementation detail — unreliable.

s = "hello"
# BAD: s is "hello"   # may True in CPython due to interning, but not guaranteed
# FIX:
print(f"s == 'hello': {s == 'hello'}")   # always correct
print(f"s is 'hello': {s is 'hello'}")   # true only due to interning — don't rely on it

# With concatenation: no interning
t = "hel" + "lo"
print(f"t == 'hello': {t == 'hello'}")  # True
print(f"t is s:       {t is s}")        # might be False — implementation-dependent


# ===========================================================================
# Pitfall 4: Shadowing Builtins
# ===========================================================================
print("\n--- Pitfall 4: Shadowing builtins ---")

# BAD — assigning to names like list, type, id, input, print
# shadows the built-in and breaks all subsequent uses.

def bad_shadow() -> None:
    list_data = [1, 2, 3]  # fine
    list = list_data        # SHADOWS the built-in 'list'!
    try:
        new = list([4, 5])  # TypeError: 'list' object is not callable
    except TypeError as e:
        print(f"  Shadow bug: {e}")

bad_shadow()

# FIX — use descriptive names
def good_naming() -> None:
    data = [1, 2, 3]
    new_data = list(data) + [4, 5]
    print(f"  Good: {new_data}")

good_naming()


# ===========================================================================
# Pitfall 5: Bare `except:` clause
# ===========================================================================
print("\n--- Pitfall 5: Bare except ---")

# BAD — catches ALL exceptions including SystemExit, KeyboardInterrupt, etc.
def bad_except() -> None:
    try:
        x = int("abc")
    except:           # catches EVERYTHING — bad!
        print("  Caught something (but what?)")

# FIX — catch specific exceptions
def good_except() -> None:
    try:
        x = int("abc")
    except ValueError as e:
        print(f"  Caught specific: {e}")
    except TypeError as e:
        print(f"  Caught type error: {e}")

bad_except()
good_except()


# ===========================================================================
# Pitfall 6: Modifying a List While Iterating
# ===========================================================================
print("\n--- Pitfall 6: Modify list during iteration ---")

# BAD — skips elements because the list shrinks as we iterate.
numbers = [1, 2, 3, 4, 5, 6]
bad_numbers = numbers[:]
for n in bad_numbers:
    if n % 2 == 0:
        bad_numbers.remove(n)   # skips the next element!
print(f"Bad (missed some evens): {bad_numbers}")  # [1, 3, 5] — 4 was skipped

# FIX 1 — iterate over a copy
numbers = [1, 2, 3, 4, 5, 6]
for n in numbers[:]:   # iterate over slice (copy)
    if n % 2 == 0:
        numbers.remove(n)
print(f"Good (copy): {numbers}")

# FIX 2 — list comprehension
numbers = [1, 2, 3, 4, 5, 6]
numbers = [n for n in numbers if n % 2 != 0]
print(f"Good (comprehension): {numbers}")


# ===========================================================================
# Pitfall 7: Missing super().__init__() in multi-inheritance
# ===========================================================================
print("\n--- Pitfall 7: Missing super().__init__() ---")

class A:
    def __init__(self) -> None:
        self.a_initialized = True
        print("  A.__init__")

class B(A):
    def __init__(self) -> None:
        # BAD: A.__init__(self) directly — skips MRO
        # FIX:
        super().__init__()
        self.b_initialized = True
        print("  B.__init__")

class C(A):
    def __init__(self) -> None:
        super().__init__()
        self.c_initialized = True
        print("  C.__init__")

class D(B, C):
    """Diamond: D → B → C → A."""
    def __init__(self) -> None:
        super().__init__()   # MRO: D → B → C → A
        print("  D.__init__")

print("D() with super() (MRO respected):")
d = D()
print(f"  a_init={d.a_initialized}, b_init={d.b_initialized}, c_init={d.c_initialized}")


# ===========================================================================
# Pitfall 8: Overusing isinstance (vs duck typing)
# ===========================================================================
print("\n--- Pitfall 8: isinstance overuse ---")

# BAD — rigid type-checking breaks duck typing
def bad_sum(values: Any) -> float:
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    return sum(values)

# FIX — duck typing: accept any iterable with numeric items
def good_sum(values: Any) -> float:
    return sum(values)   # works with list, tuple, generator, set, etc.

print("Good sum of generator:", good_sum(x * x for x in range(5)))


# ===========================================================================
# Pitfall 9: Missing __all__ in module
# ===========================================================================
print("\n--- Pitfall 9: Missing __all__ ---")
# Without __all__, `from module import *` exports EVERYTHING including
# internal helpers and imported names — pollutes caller's namespace.
# FIX: always define __all__ in public modules.

__all__ = ["append_to_GOOD", "good_sum"]


# ===========================================================================
# Pitfall 10: __init__ doing I/O
# ===========================================================================
print("\n--- Pitfall 10: __init__ doing I/O ---")

# BAD — side effects in __init__ make the class hard to test and instantiate.
class BadService:
    def __init__(self, host: str) -> None:
        self.host = host
        # self._conn = connect(host)   # I/O!  Raises if network down, hard to mock.

# FIX — lazy initialization or factory method.
class GoodService:
    def __init__(self, host: str) -> None:
        self.host = host
        self._conn: Any = None   # not connected yet

    def connect(self) -> None:
        """Explicit connect — caller controls when I/O happens."""
        # self._conn = _do_connect(self.host)
        print(f"  Connecting to {self.host}...")

    @classmethod
    def from_env(cls) -> GoodService:
        """Factory that reads config — keeps __init__ clean."""
        import os
        host = os.environ.get("SERVICE_HOST", "localhost")
        return cls(host)

GoodService("db.example.com").connect()

print("\nAll pitfalls demonstrated. See tests/test_day28.py for assertions.")
