"""
Day 03 — Exercises: Classes and Encapsulation
"""
from __future__ import annotations


# ---------------------------------------------------------------------------
# Exercise 1: BankAccount with Full Validation
# ---------------------------------------------------------------------------
# Create a BankAccount class with:
#   - __init__(owner: str, balance: float = 0.0)
#   - deposit(amount) — raises ValueError if amount <= 0
#   - withdraw(amount) — returns False if insufficient, raises if amount <= 0
#   - transfer(other, amount) — transfer between two accounts
#   - balance property (read-only)
#   - __repr__ and __str__

class BankAccount:
    """Bank account with validation and transfer support."""
    # TODO: implement
    pass


# ---------------------------------------------------------------------------
# Exercise 2: Property Validation — Rectangle
# ---------------------------------------------------------------------------
# Create a Rectangle class where:
#   - width and height are @property with setters
#   - Setting width or height to <= 0 raises ValueError
#   - area and perimeter are computed @property (no setter)
#   - __repr__ shows Rectangle(width=W, height=H)
#   - @classmethod square(cls, side) creates a square

class Rectangle:
    """Rectangle with validated dimensions."""
    # TODO: implement
    pass


# ---------------------------------------------------------------------------
# Exercise 3: __repr__ and __eq__
# ---------------------------------------------------------------------------
# Create a Fraction class (simplified) with:
#   - __init__(numerator, denominator) — stores in reduced form
#   - __repr__ returns "Fraction(3, 4)" style
#   - __str__ returns "3/4" style
#   - __eq__ compares values (3/6 == 1/2)
#   - __add__, __mul__
# Hint: use math.gcd to reduce

class Fraction:
    """Reduced fraction."""
    # TODO: implement
    pass


# ---------------------------------------------------------------------------
# Exercise 4: Class vs Instance Attributes
# ---------------------------------------------------------------------------
# Create a Counter class where:
#   - _instances (class attr) tracks how many Counter objects exist
#   - each instance has a name and a count
#   - @classmethod instance_count() returns total instances created
#   - incrementing one counter does not affect others

class Counter:
    """Counter with class-level instance tracking."""
    # TODO: implement
    pass


if __name__ == "__main__":
    # Test BankAccount
    acc = BankAccount("Alice", 500.0)
    acc.deposit(100.0)
    acc.withdraw(50.0)
    print(acc)

    # Test Rectangle
    r = Rectangle(4.0, 5.0)
    print(r.area, r.perimeter)
    sq = Rectangle.square(6.0)
    print(sq)

    # Test Fraction
    from math import gcd
    f1 = Fraction(1, 2)
    f2 = Fraction(1, 3)
    print(f1 + f2)        # 5/6
    print(f1 == Fraction(2, 4))  # True

    # Test Counter
    c1 = Counter("a")
    c2 = Counter("b")
    print(Counter.instance_count())  # 2
