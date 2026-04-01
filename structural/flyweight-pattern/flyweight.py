"""
Flyweight Pattern.

Separates intrinsic (shared, immutable) state from extrinsic (per-use,
caller-supplied) state.  FlyweightFactory maintains a cache so objects
with identical intrinsic state are reused.

Example: character rendering — font + color = intrinsic, position = extrinsic.
"""
from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Flyweight (shared intrinsic state)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class CharacterStyle:
    """Immutable intrinsic state: shared across many characters.

    Args:
        font: Font family name.
        color: Text colour.
        size: Font size in pt.
    """

    font: str
    color: str
    size: int

    def render(self, char: str, x: int, y: int) -> str:
        """Render character using shared style at extrinsic position.

        Args:
            char: The glyph to draw.
            x: Horizontal position (extrinsic state).
            y: Vertical position (extrinsic state).
        """
        return (
            f"'{char}' [{self.font}/{self.color}/{self.size}pt] at ({x},{y})"
        )


# ---------------------------------------------------------------------------
# Flyweight factory
# ---------------------------------------------------------------------------
class FlyweightFactory:
    """Creates and caches CharacterStyle flyweights.

    Two calls with the same (font, color, size) return the *same* object.
    """

    def __init__(self) -> None:
        self._cache: dict[tuple[str, str, int], CharacterStyle] = {}

    def get_style(self, font: str, color: str, size: int) -> CharacterStyle:
        """Return a cached flyweight for the given style, creating it if needed."""
        key = (font, color, size)
        if key not in self._cache:
            self._cache[key] = CharacterStyle(font=font, color=color, size=size)
        return self._cache[key]

    @property
    def cache_size(self) -> int:
        """Number of unique flyweights in the cache."""
        return len(self._cache)

    def list_styles(self) -> list[CharacterStyle]:
        return list(self._cache.values())


# ---------------------------------------------------------------------------
# Context — combines a flyweight with extrinsic state
# ---------------------------------------------------------------------------
@dataclass
class CharacterContext:
    """Stores extrinsic state (char + position) and a reference to its style."""

    char: str
    x: int
    y: int
    style: CharacterStyle

    def render(self) -> str:
        return self.style.render(self.char, self.x, self.y)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    factory = FlyweightFactory()

    # Simulate rendering a paragraph — many characters share styles
    text = "Hello"
    style = factory.get_style("Arial", "black", 12)

    contexts = [
        CharacterContext(ch, i * 10, 0, style)
        for i, ch in enumerate(text)
    ]

    for ctx in contexts:
        print(ctx.render())

    # Add a different style
    bold_style = factory.get_style("Arial", "red", 14)
    contexts.append(CharacterContext("!", len(text) * 10, 0, bold_style))
    print(contexts[-1].render())

    print(f"\nUnique styles in cache: {factory.cache_size}")

    # Same style requested again — same object
    same_style = factory.get_style("Arial", "black", 12)
    print(f"Same flyweight reused: {style is same_style}")
