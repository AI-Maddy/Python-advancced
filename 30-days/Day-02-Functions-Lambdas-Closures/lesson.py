"""
Day 02 — Functions, Lambdas, and Closures
==========================================

Topics:
  - def, return, default arguments, *args, **kwargs
  - Python's first-class functions
  - lambda expressions — when to use, limitations
  - Closures and captured variables (nonlocal)
  - Higher-order functions: map, filter, reduce
  - functools.partial
  - Type annotations for callables: Callable[[int, str], bool]
"""
from __future__ import annotations

import functools
from typing import Callable


# ---------------------------------------------------------------------------
# 1. Function Basics: def, return, defaults, *args, **kwargs
# ---------------------------------------------------------------------------

def greet(name: str, times: int = 1) -> str:
    """Return a greeting repeated 'times' times.

    Default arguments work just like C++ default arguments,
    but they are evaluated ONCE at function definition time.
    """
    return (f"Hello, {name}! " * times).strip()


def variadic_sum(*args: int | float) -> float:
    """Accept any number of positional arguments.

    *args collects extra positional arguments into a tuple.
    C++ equivalent: variadic templates or initializer_list.
    """
    return float(sum(args))


def configure(**kwargs: str | int | bool) -> dict[str, str | int | bool]:
    """Accept any keyword arguments.

    **kwargs collects them into a dict.
    """
    return dict(kwargs)


def full_signature(
    required: str,
    /,                     # positional-only before /
    normal: int = 0,
    *args: float,          # variadic positional
    keyword_only: bool = False,  # keyword-only after *
    **kwargs: str,         # variadic keyword
) -> dict[str, object]:
    """Demonstrate all parameter kinds.

    Python 3.8+ positional-only parameters (before /).
    """
    return {
        "required": required,
        "normal": normal,
        "args": args,
        "keyword_only": keyword_only,
        "kwargs": kwargs,
    }


def demo_defaults() -> None:
    """Show default argument gotcha: mutable defaults."""
    # THE MUTABLE DEFAULT GOTCHA — common Python bug
    # C++ doesn't have this because default values are not shared state
    def bad_append(item: int, lst: list[int] = []) -> list[int]:  # noqa: B006
        """BAD: list is created once and shared across calls."""
        lst.append(item)
        return lst

    # First call: list has [1]
    # Second call: same list! now has [1, 2]
    r1 = bad_append(1)
    r2 = bad_append(2)
    print(f"bad_append: r1={r1}, r2={r2}")  # [1, 2], [1, 2] — same list!

    def good_append(item: int, lst: list[int] | None = None) -> list[int]:
        """GOOD: use None as sentinel, create fresh list each call."""
        if lst is None:
            lst = []
        lst.append(item)
        return lst

    r1 = good_append(1)
    r2 = good_append(2)
    print(f"good_append: r1={r1}, r2={r2}")  # [1], [2] — separate lists


# ---------------------------------------------------------------------------
# 2. First-Class Functions
# ---------------------------------------------------------------------------
# In Python (unlike C++), functions are objects.
# You can store them in variables, pass them as arguments, return them.
# C++ achieves similar things with function pointers, std::function, lambdas.

def square(x: int) -> int:
    """Return x squared."""
    return x * x


def cube(x: int) -> int:
    """Return x cubed."""
    return x * x * x


def apply(func: Callable[[int], int], value: int) -> int:
    """Apply func to value. First-class function as parameter."""
    return func(value)


def demo_first_class() -> None:
    """Show functions as first-class objects."""
    # Store function in variable
    operation = square
    print(operation(5))       # 25

    # Pass function as argument
    print(apply(square, 5))   # 25
    print(apply(cube, 3))     # 27

    # Functions have attributes
    print(square.__name__)    # square
    print(square.__doc__)     # Return x squared.

    # Store in a data structure
    ops: dict[str, Callable[[int], int]] = {
        "square": square,
        "cube": cube,
    }
    for name, fn in ops.items():
        print(f"{name}(4) = {fn(4)}")


# ---------------------------------------------------------------------------
# 3. Lambda Expressions
# ---------------------------------------------------------------------------
# lambda is a single-expression anonymous function.
# C++ equivalent: [](params) { return expr; }  (but C++ lambdas are more capable)
# Python lambda limitations:
#   - Single expression only (no statements, no assignment, no multiline)
#   - Cannot have type annotations in the lambda itself

def demo_lambdas() -> None:
    """Show lambda use cases and limitations."""
    # Basic lambda
    double: Callable[[int], int] = lambda x: x * 2
    print(double(5))           # 10

    # Lambda in sorted()
    points = [(1, 5), (3, 2), (2, 8), (4, 1)]
    sorted_by_y = sorted(points, key=lambda p: p[1])
    print(sorted_by_y)         # [(4, 1), (3, 2), (1, 5), (2, 8)]

    # Lambda in max/min
    words = ["banana", "apple", "cherry"]
    longest = max(words, key=lambda w: len(w))
    print(longest)             # cherry (or banana, same length)

    # WHEN TO USE LAMBDA vs def:
    # Use lambda for: short, obvious, single-use comparators/key functions
    # Use def for:   anything that needs a docstring, multiple expressions,
    #                or a meaningful name

    # DON'T assign lambda to a variable if you can use def instead:
    # BAD:  add = lambda a, b: a + b    (mypy will warn)
    # GOOD: def add(a: int, b: int) -> int: return a + b

    # GOOD lambda usage: inline sort key
    data = [{"name": "Bob", "age": 30}, {"name": "Alice", "age": 25}]
    sorted_data = sorted(data, key=lambda d: d["age"])
    print([d["name"] for d in sorted_data])  # ['Alice', 'Bob']


# ---------------------------------------------------------------------------
# 4. Closures and nonlocal
# ---------------------------------------------------------------------------
# A closure is a function that captures variables from its enclosing scope.
# Python closures capture by REFERENCE (like C++ [&] capture).
# C++ captures by value by default; Python captures by reference by default.

def make_counter(start: int = 0) -> Callable[[], int]:
    """Return a stateful counter function (closure)."""
    count = start

    def counter() -> int:
        nonlocal count        # declare we want to modify the outer variable
        count += 1
        return count

    return counter


def make_adder(n: int) -> Callable[[int], int]:
    """Return a function that adds n to its argument."""
    # n is captured by reference; since it's not modified, no nonlocal needed
    def adder(x: int) -> int:
        return x + n
    return adder


def demo_closures() -> None:
    """Show closure behaviour including the late-binding gotcha."""
    counter = make_counter()
    print(counter())   # 1
    print(counter())   # 2
    print(counter())   # 3

    # Two independent counters
    c1 = make_counter()
    c2 = make_counter(10)
    print(c1(), c2())    # 1, 11

    add5 = make_adder(5)
    add10 = make_adder(10)
    print(add5(3))    # 8
    print(add10(3))   # 13

    # THE LATE-BINDING GOTCHA — classic Python closure bug
    # All closures in a loop share the SAME variable binding
    bad_funcs: list[Callable[[], int]] = [lambda: i for i in range(3)]  # noqa: B023
    print([f() for f in bad_funcs])  # [2, 2, 2] — all capture the LAST i!

    # Fix: capture by value using a default argument
    good_funcs: list[Callable[[], int]] = [
        (lambda i=i: i) for i in range(3)
    ]
    print([f() for f in good_funcs])  # [0, 1, 2] — each captures its own i


# ---------------------------------------------------------------------------
# 5. Higher-Order Functions: map, filter, reduce
# ---------------------------------------------------------------------------

def demo_higher_order() -> None:
    """Show map, filter, reduce — and why list comprehensions are often better."""
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # map — applies a function to each element, returns iterator
    squares_iter = map(square, nums)
    squares = list(squares_iter)
    print(f"map squares: {squares}")

    # filter — keeps elements where function returns True
    evens = list(filter(lambda x: x % 2 == 0, nums))
    print(f"filter evens: {evens}")

    # reduce — fold left (like std::accumulate in C++)
    from functools import reduce
    product = reduce(lambda a, b: a * b, nums)
    print(f"reduce product: {product}")   # 3628800

    # List comprehensions are usually clearer than map/filter
    squares_comp = [x * x for x in nums]          # clearer than map
    evens_comp = [x for x in nums if x % 2 == 0]  # clearer than filter
    print(f"list comp squares: {squares_comp}")
    print(f"list comp evens: {evens_comp}")

    # Generator expressions (lazy, no intermediate list)
    total = sum(x * x for x in nums)   # lazy evaluation
    print(f"sum of squares: {total}")


# ---------------------------------------------------------------------------
# 6. functools.partial — Partial Application
# ---------------------------------------------------------------------------
# partial creates a new function with some arguments pre-filled.
# C++ equivalent: std::bind or lambda capture

def power(base: float, exponent: float) -> float:
    """Return base raised to exponent."""
    return base ** exponent


def demo_partial() -> None:
    """Show partial application with functools.partial."""
    square_fn = functools.partial(power, exponent=2)
    cube_fn = functools.partial(power, exponent=3)

    print(square_fn(5))   # 25.0
    print(cube_fn(3))     # 27.0

    # partial with positional args
    double = functools.partial(lambda a, b: a * b, 2)
    print(double(7))   # 14

    # Real-world use: pre-configure a print separator
    print_csv = functools.partial(print, sep=",", end="\n")
    print_csv("a", "b", "c")   # a,b,c


# ---------------------------------------------------------------------------
# 7. Type Annotations for Callables
# ---------------------------------------------------------------------------

def demo_callable_types() -> None:
    """Show Callable type annotations."""
    from typing import Callable

    # Callable[[arg_types...], return_type]
    def apply_twice(f: Callable[[int], int], x: int) -> int:
        return f(f(x))

    print(apply_twice(square, 3))   # 81  (3^2 = 9, 9^2 = 81)

    # Callable with no args
    def call_it(f: Callable[[], str]) -> str:
        return f()

    print(call_it(lambda: "hello"))

    # Callable with **kwargs or *args — use Callable[..., ReturnType]
    from typing import Any
    def call_any(f: Callable[..., Any], *args: Any) -> Any:
        return f(*args)


if __name__ == "__main__":
    print("=== Function Basics ===")
    print(greet("Alice"))
    print(greet("Bob", 3))
    print(variadic_sum(1, 2, 3, 4, 5))
    print(configure(host="localhost", port=8080, debug=True))
    demo_defaults()

    print("\n=== First-Class Functions ===")
    demo_first_class()

    print("\n=== Lambdas ===")
    demo_lambdas()

    print("\n=== Closures ===")
    demo_closures()

    print("\n=== Higher-Order Functions ===")
    demo_higher_order()

    print("\n=== Partial ===")
    demo_partial()

    print("\n=== Callable Types ===")
    demo_callable_types()
