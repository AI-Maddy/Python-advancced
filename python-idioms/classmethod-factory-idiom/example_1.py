"""
Example 1 — Named constructors for a Colour value object.
"""
from __future__ import annotations


class Colour:
    """Colour with RGB + HSL representations and multiple constructors."""

    def __init__(self, r: int, g: int, b: int) -> None:
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def from_hex(cls, hex_str: str) -> Colour:
        """Create from a hex string like ``'#ff8800'`` or ``'ff8800'``."""
        s = hex_str.lstrip("#")
        return cls(int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))

    @classmethod
    def from_tuple(cls, t: tuple[int, int, int]) -> Colour:
        """Create from an (r, g, b) tuple."""
        return cls(*t)

    @classmethod
    def white(cls) -> Colour:
        return cls(255, 255, 255)

    @classmethod
    def black(cls) -> Colour:
        return cls(0, 0, 0)

    @classmethod
    def red(cls) -> Colour:
        return cls(255, 0, 0)

    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def __repr__(self) -> str:
        return f"Colour({self.r}, {self.g}, {self.b})"


def main() -> None:
    c1 = Colour.from_hex("#ff8800")
    c2 = Colour.from_tuple((128, 64, 32))
    c3 = Colour.white()
    c4 = Colour.black()

    for c in (c1, c2, c3, c4):
        print(f"  {c} → {c.to_hex()}")


if __name__ == "__main__":
    main()
