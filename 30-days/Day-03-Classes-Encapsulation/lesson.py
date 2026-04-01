"""
Day 03 — Classes and Encapsulation
====================================

Topics:
  - class statement, __init__, self
  - Instance vs class attributes
  - Name mangling (__private) vs single underscore convention (_protected)
  - @property, @<prop>.setter, @<prop>.deleter
  - __repr__, __str__, __eq__, __hash__
  - @staticmethod vs @classmethod
  - No true private in Python — convention and __mangling
  - Python vs C++ encapsulation comparison
"""
from __future__ import annotations

import math


# ---------------------------------------------------------------------------
# 1. Basic Class Structure
# ---------------------------------------------------------------------------

class Point:
    """A 2D point. Demonstrates __init__, instance attributes, __repr__."""

    # Class attribute — shared by ALL instances (like C++ static member)
    dimensions: int = 2

    def __init__(self, x: float, y: float) -> None:
        # Instance attributes — unique per instance
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Machine-readable representation. Shown in REPL and for debugging."""
        return f"Point(x={self.x!r}, y={self.y!r})"

    def __str__(self) -> str:
        """Human-readable representation. Used by print() and str()."""
        return f"({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        """Value equality. C++ equivalent: operator==."""
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """Must define __hash__ if you define __eq__ (for use in sets/dicts)."""
        return hash((self.x, self.y))

    def distance_to(self, other: "Point") -> float:
        """Return Euclidean distance to another point."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    @staticmethod
    def origin() -> "Point":
        """Factory for the origin point. @staticmethod: no self or cls."""
        return Point(0.0, 0.0)

    @classmethod
    def from_tuple(cls, t: tuple[float, float]) -> "Point":
        """Alternative constructor. @classmethod: cls is the class itself.
        This is the Python equivalent of C++ named constructor idiom.
        """
        return cls(t[0], t[1])


# ---------------------------------------------------------------------------
# 2. Encapsulation: Private and Protected Conventions
# ---------------------------------------------------------------------------
# Python has NO true access control (unlike C++ private/protected/public).
# Conventions:
#   _name   : "protected" — internal use, avoid from outside (one underscore)
#   __name  : "private"   — name-mangled to _ClassName__name; harder to access
#             but NOT actually prevented — just obfuscated

class BankAccount:
    """Bank account demonstrating encapsulation patterns.

    C++ comparison:
      C++:    balance_ is private — compiler enforces no external access
      Python: __balance is name-mangled but still accessible as _BankAccount__balance
              The difference is convention and discoverability, not enforcement.
    """

    _interest_rate: float = 0.03  # "protected" class attribute

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        self._owner = owner           # "protected" — internal
        self.__balance = initial_balance  # "private" — name-mangled

        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")

    # --- Public interface ---

    @property
    def owner(self) -> str:
        """Read-only property — no setter."""
        return self._owner

    @property
    def balance(self) -> float:
        """Read-only property — balance is observable but not directly settable."""
        return self.__balance

    def deposit(self, amount: float) -> None:
        """Add amount to balance."""
        if amount <= 0:
            raise ValueError(f"Deposit amount must be positive, got {amount}")
        self.__balance += amount

    def withdraw(self, amount: float) -> bool:
        """Withdraw amount. Returns False if insufficient funds."""
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be positive")
        if amount > self.__balance:
            return False
        self.__balance -= amount
        return True

    def apply_interest(self) -> None:
        """Apply the class-level interest rate."""
        self.__balance *= (1 + self._interest_rate)

    def __repr__(self) -> str:
        return f"BankAccount(owner={self._owner!r}, balance={self.__balance:.2f})"

    # --- Demonstrate name mangling ---
    # Calling self.__balance inside the class is fine.
    # From outside: account.__balance raises AttributeError.
    # But account._BankAccount__balance works! Python just renames it.


# ---------------------------------------------------------------------------
# 3. @property — Computed Attributes with Validation
# ---------------------------------------------------------------------------

class Circle:
    """Circle demonstrating @property with validation.

    Class invariant: radius >= 0.
    C++ equivalent: private member + getter/setter with validation.
    """

    def __init__(self, radius: float) -> None:
        self.radius = radius  # goes through the setter below

    @property
    def radius(self) -> float:
        """Get radius."""
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        """Set radius — validates the invariant."""
        if value < 0:
            raise ValueError(f"Radius must be non-negative, got {value}")
        self._radius = value

    @radius.deleter
    def radius(self) -> None:
        """Delete radius — unusual, but shows the full protocol."""
        del self._radius

    @property
    def area(self) -> float:
        """Computed property — no setter needed."""
        return math.pi * self._radius ** 2

    @property
    def circumference(self) -> float:
        """Another computed property."""
        return 2 * math.pi * self._radius

    def __repr__(self) -> str:
        return f"Circle(radius={self._radius!r})"


# ---------------------------------------------------------------------------
# 4. Class Methods and Static Methods
# ---------------------------------------------------------------------------

class Temperature:
    """Temperature in Celsius. Demonstrates @classmethod factory pattern."""

    def __init__(self, celsius: float) -> None:
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @property
    def kelvin(self) -> float:
        return self._celsius + 273.15

    # --- @classmethod factories (named constructor idiom) ---
    # C++ equivalent: static factory functions

    @classmethod
    def from_fahrenheit(cls, f: float) -> "Temperature":
        """Create from Fahrenheit value."""
        return cls((f - 32) * 5 / 9)

    @classmethod
    def from_kelvin(cls, k: float) -> "Temperature":
        """Create from Kelvin value."""
        if k < 0:
            raise ValueError(f"Kelvin cannot be negative: {k}")
        return cls(k - 273.15)

    # --- @staticmethod ---
    # No access to cls or self. Just a namespaced function.

    @staticmethod
    def is_valid_celsius(value: float) -> bool:
        """Return True if value is above absolute zero in Celsius."""
        return value >= -273.15

    def __repr__(self) -> str:
        return f"Temperature({self._celsius:.2f}°C)"


# ---------------------------------------------------------------------------
# 5. __repr__, __str__, __eq__, __hash__ in depth
# ---------------------------------------------------------------------------

class Color:
    """RGB colour — demonstrates all comparison/hashing dunder methods."""

    def __init__(self, r: int, g: int, b: int) -> None:
        for name, val in [("r", r), ("g", g), ("b", b)]:
            if not 0 <= val <= 255:
                raise ValueError(f"{name} must be 0-255, got {val}")
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self) -> str:
        """repr: should ideally be eval()-able."""
        return f"Color({self.r}, {self.g}, {self.b})"

    def __str__(self) -> str:
        """str: human-friendly hex notation."""
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return NotImplemented
        return (self.r, self.g, self.b) == (other.r, other.g, other.b)

    def __hash__(self) -> int:
        """Required to use Color as a dict key or in a set."""
        return hash((self.r, self.g, self.b))

    def __lt__(self, other: "Color") -> bool:
        """Brightness comparison (average of channels)."""
        return (self.r + self.g + self.b) < (other.r + other.g + other.b)

    def blend(self, other: "Color") -> "Color":
        """Return average of two colours."""
        return Color(
            (self.r + other.r) // 2,
            (self.g + other.g) // 2,
            (self.b + other.b) // 2,
        )


if __name__ == "__main__":
    print("=== Point ===")
    p1 = Point(1.0, 2.0)
    p2 = Point.from_tuple((3.0, 4.0))
    origin = Point.origin()
    print(repr(p1))           # Point(x=1.0, y=2.0)
    print(str(p1))            # (1.0, 2.0)
    print(p1 == Point(1.0, 2.0))   # True
    print(p1.distance_to(origin))  # ~2.236
    print(f"Class attribute: {Point.dimensions}")

    print("\n=== BankAccount ===")
    acc = BankAccount("Alice", 1000.0)
    acc.deposit(200.0)
    acc.withdraw(50.0)
    print(acc)                # BankAccount(owner='Alice', balance=1150.00)
    print(acc.balance)        # 1150.0
    # print(acc.__balance)    # AttributeError
    print(acc._BankAccount__balance)  # 1150.0 — mangling doesn't truly hide it

    print("\n=== Circle ===")
    c = Circle(5.0)
    print(f"area={c.area:.4f}, circumference={c.circumference:.4f}")
    try:
        c.radius = -1.0
    except ValueError as e:
        print(f"Caught: {e}")

    print("\n=== Temperature ===")
    boiling = Temperature(100.0)
    body = Temperature.from_fahrenheit(98.6)
    abs_zero = Temperature.from_kelvin(0.0)
    print(boiling, boiling.fahrenheit)
    print(body, body.celsius)
    print(abs_zero)

    print("\n=== Color ===")
    red = Color(255, 0, 0)
    blue = Color(0, 0, 255)
    purple = red.blend(blue)
    print(str(red), repr(red))
    print(str(purple))
    colours = {red, blue, purple}  # uses __hash__ and __eq__
    print(len(colours))   # 3
