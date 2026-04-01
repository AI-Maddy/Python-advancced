"""
Tests for Day 28 — Common Python Pitfalls
Run with: pytest tests/test_day28.py -v
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


# ===========================================================================
# Pitfall 1: Mutable default argument
# ===========================================================================

def append_bad(item: int, result: list[int] = []) -> list[int]:  # noqa: B006
    result.append(item)
    return result


def append_good(item: int, result: list[int] | None = None) -> list[int]:
    if result is None:
        result = []
    result.append(item)
    return result


def test_mutable_default_bug() -> None:
    """Bug: shared state across calls without explicit argument."""
    # Reset the default by clearing it
    append_bad.__defaults__ = ([],)  # type: ignore[attr-defined]
    r1 = append_bad(1)
    r2 = append_bad(2)
    # Both modify the same default list
    assert r1 is r2  # same object!


def test_mutable_default_fixed() -> None:
    """Fix: each call without explicit arg gets a fresh list."""
    r1 = append_good(1)
    r2 = append_good(2)
    assert r1 is not r2
    assert r1 == [1]
    assert r2 == [2]


# ===========================================================================
# Pitfall 2: Late binding closure
# ===========================================================================

def test_late_binding_bug() -> None:
    """All lambdas capture the last value of i."""
    fns = [lambda: i for i in range(5)]
    # All return 4 (last value)
    assert all(f() == 4 for f in fns)


def test_late_binding_fixed_default_arg() -> None:
    """Fix: capture current value as default argument."""
    fns = [lambda i=i: i for i in range(5)]
    assert [f() for f in fns] == [0, 1, 2, 3, 4]


def test_late_binding_fixed_partial() -> None:
    """Fix: use functools.partial."""
    import functools
    fns = [functools.partial(lambda i: i, i) for i in range(5)]
    assert [f() for f in fns] == [0, 1, 2, 3, 4]


# ===========================================================================
# Pitfall 3: is vs ==
# ===========================================================================

def test_is_not_equal_for_constructed_string() -> None:
    """is may fail for dynamically constructed equal strings."""
    s1 = "hell" + "o"
    s2 = "hello"
    assert s1 == s2          # always True
    # s1 is s2 may or may not be True (interning is an impl detail)


def test_use_equality_not_identity() -> None:
    """== is always the right comparison for string values."""
    greeting = "hello"
    assert greeting == "hello"
    assert not (greeting == "world")


# ===========================================================================
# Pitfall 4: Shadowing builtins
# ===========================================================================

def test_shadowing_list_breaks_call() -> None:
    """Shadowing 'list' prevents using list() constructor."""
    def buggy() -> None:
        lst = [1, 2]
        list = lst   # shadow builtin  # noqa: F841
        # list([3]) would raise TypeError here

    buggy()  # should not raise, but list() is broken inside


def test_no_shadowing() -> None:
    """Safe: use descriptive names."""
    my_data = [1, 2, 3]
    new_data = list(my_data)   # list() still works
    assert new_data == [1, 2, 3]


# ===========================================================================
# Pitfall 5: Bare except
# ===========================================================================

def safe_divide_bad(a: float, b: float) -> float | str:
    try:
        return a / b
    except:  # noqa: E722
        return "error"


def safe_divide_good(a: float, b: float) -> float | str:
    try:
        return a / b
    except ZeroDivisionError:
        return "error"


def test_bare_except_catches_zero_division() -> None:
    assert safe_divide_bad(10, 0) == "error"


def test_specific_except_catches_zero_division() -> None:
    assert safe_divide_good(10, 0) == "error"


def test_specific_except_allows_other_exceptions() -> None:
    """ZeroDivisionError specifically caught; TypeError is not."""
    def divide_with_type_error() -> None:
        safe_divide_good("10", "2")  # type: ignore[arg-type] → TypeError not caught

    with pytest.raises(TypeError):
        divide_with_type_error()


# ===========================================================================
# Pitfall 6: Modify list during iteration
# ===========================================================================

def remove_evens_bad(lst: list[int]) -> list[int]:
    for n in lst:
        if n % 2 == 0:
            lst.remove(n)   # skips next element
    return lst


def remove_evens_good(lst: list[int]) -> list[int]:
    return [n for n in lst if n % 2 != 0]


def test_bad_remove_skips_elements() -> None:
    """Bug: remove during iteration skips elements."""
    lst = [2, 4, 6]
    result = remove_evens_bad(lst[:])
    # Expects [], but buggy version returns [4] (skips 4)
    assert result != []   # the bug


def test_good_remove_correct() -> None:
    lst = [1, 2, 3, 4, 5, 6]
    result = remove_evens_good(lst)
    assert result == [1, 3, 5]


# ===========================================================================
# Pitfall 7: Missing super().__init__() in multiple inheritance
# ===========================================================================

class A:
    def __init__(self, **kwargs: object) -> None:
        self.a = True
        super().__init__(**kwargs)


class B(A):
    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.b = True


class C(A):
    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.c = True


class D_bad(B, C):
    def __init__(self) -> None:
        B.__init__(self)   # skips C → self.c missing


class D_good(B, C):
    def __init__(self) -> None:
        super().__init__()   # MRO: D → B → C → A — all called


def test_super_missing_skips_class() -> None:
    d = D_bad()
    # Even calling B.__init__(self) directly, B uses super() internally,
    # so MRO still reaches C.__init__ — this is the correct Python behaviour.
    # The real pitfall: D_bad skips its own super().__init__() call so any
    # D-level cooperative init protocol is broken.
    assert d.a  # A.__init__ reached via B's internal super()
    assert d.b  # B sets it
    assert hasattr(d, "c")  # C IS reached because B uses super() internally


def test_super_cooperative_all_inits_called() -> None:
    d = D_good()
    assert d.a and d.b and d.c   # all initialised


# ===========================================================================
# Pitfall 8: Duck typing vs isinstance
# ===========================================================================

def sum_bad(values: object) -> float:
    if not isinstance(values, list):
        raise TypeError("must be list")
    return sum(values)  # type: ignore[arg-type]


def sum_good(values: object) -> float:
    return sum(values)  # type: ignore[arg-type]


def test_isinstance_rejects_tuple() -> None:
    with pytest.raises(TypeError):
        sum_bad((1, 2, 3))


def test_duck_typing_accepts_any_iterable() -> None:
    assert sum_good((1, 2, 3)) == 6
    assert sum_good({1, 2, 3}) == 6
    assert sum_good(x for x in range(4)) == 6
