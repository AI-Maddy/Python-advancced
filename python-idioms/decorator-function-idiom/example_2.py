"""
Example 2 — @functools.lru_cache and stacking decorators.
"""
from __future__ import annotations

import functools
from decorator_function import add_exclamation, expensive_fib, greet, uppercase_result


def main() -> None:
    # Stacking
    print("greet('python'):", greet("python"))

    # Manual stacking to illustrate order
    def say(word: str) -> str:
        return word

    # Applied bottom-up: uppercase first, then exclamation
    stacked = add_exclamation(uppercase_result(say))
    print("Stacked (upper then !):", stacked("hello"))  # "HELLO!"

    # Reversed: exclamation first, then uppercase
    reversed_stack = uppercase_result(add_exclamation(say))
    print("Stacked (! then upper):", reversed_stack("hello"))  # "HELLO!"

    # LRU cache info
    expensive_fib.cache_clear()
    for n in range(35):
        expensive_fib(n)
    info = expensive_fib.cache_info()
    print(f"\nlru_cache hits={info.hits}, misses={info.misses}, size={info.currsize}")

    # cached_property
    from decorator_function import Circle
    c = Circle(10.0)
    a1 = c.area
    a2 = c.area
    print(f"\nCircle area computed once: {a1:.4f} == {a2:.4f}")
    print(f"Cached in __dict__: {'area' in c.__dict__}")


if __name__ == "__main__":
    main()
