"""
Day 03 — Exercises: Classes and Encapsulation
"""
from __future__ import annotations

import math


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

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._owner = owner
        self.__balance = balance

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def balance(self) -> float:
        return self.__balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"Deposit must be positive, got {amount}")
        self.__balance += amount

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError(f"Withdrawal must be positive, got {amount}")
        if amount > self.__balance:
            return False
        self.__balance -= amount
        return True

    def transfer(self, other: "BankAccount", amount: float) -> bool:
        """Transfer amount to other account."""
        if self.withdraw(amount):
            other.deposit(amount)
            return True
        return False

    def __repr__(self) -> str:
        return f"BankAccount(owner={self._owner!r}, balance={self.__balance:.2f})"

    def __str__(self) -> str:
        return f"{self._owner}'s account: ${self.__balance:.2f}"


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

    def __init__(self, width: float, height: float) -> None:
        self.width = width    # goes through setter
        self.height = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"Width must be positive, got {value}")
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"Height must be positive, got {value}")
        self._height = value

    @property
    def area(self) -> float:
        return self._width * self._height

    @property
    def perimeter(self) -> float:
        return 2 * (self._width + self._height)

    @classmethod
    def square(cls, side: float) -> "Rectangle":
        return cls(side, side)

    def __repr__(self) -> str:
        return f"Rectangle(width={self._width!r}, height={self._height!r})"


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

    def __init__(self, numerator: int, denominator: int) -> None:
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        # Normalise sign to numerator
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
        g = math.gcd(abs(numerator), denominator)
        self._num = numerator // g
        self._den = denominator // g

    @property
    def numerator(self) -> int:
        return self._num

    @property
    def denominator(self) -> int:
        return self._den

    def __repr__(self) -> str:
        return f"Fraction({self._num}, {self._den})"

    def __str__(self) -> str:
        return f"{self._num}/{self._den}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Fraction):
            return NotImplemented
        return self._num == other._num and self._den == other._den

    def __hash__(self) -> int:
        return hash((self._num, self._den))

    def __add__(self, other: "Fraction") -> "Fraction":
        return Fraction(
            self._num * other._den + other._num * self._den,
            self._den * other._den,
        )

    def __mul__(self, other: "Fraction") -> "Fraction":
        return Fraction(self._num * other._num, self._den * other._den)


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

    _instances: int = 0

    def __init__(self, name: str) -> None:
        self.name = name
        self._count = 0
        Counter._instances += 1

    def increment(self, by: int = 1) -> None:
        self._count += by

    @property
    def count(self) -> int:
        return self._count

    @classmethod
    def instance_count(cls) -> int:
        return cls._instances

    def __repr__(self) -> str:
        return f"Counter(name={self.name!r}, count={self._count})"


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
