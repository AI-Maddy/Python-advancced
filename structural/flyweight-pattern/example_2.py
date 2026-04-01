"""
Example 2 — Icon cache.

UI icons are heavy to create.  The factory caches loaded icons so each
unique (name, size) pair is only created once regardless of how many
widgets use the same icon.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Icon:
    """Intrinsic: the loaded icon data (shared)."""
    name: str
    size: int
    data: bytes  # In real code: actual image bytes

    def draw(self, x: int, y: int) -> str:
        return f"Icon({self.name},{self.size}px) at ({x},{y})"


class IconCache:
    """Flyweight factory for icons."""

    def __init__(self) -> None:
        self._cache: dict[tuple[str, int], Icon] = {}
        self._load_count = 0

    def load(self, name: str, size: int) -> Icon:
        key = (name, size)
        if key not in self._cache:
            # Simulate expensive load
            self._load_count += 1
            self._cache[key] = Icon(
                name=name,
                size=size,
                data=bytes(f"{name}:{size}".encode()),
            )
        return self._cache[key]

    @property
    def size(self) -> int:
        return len(self._cache)

    @property
    def loads(self) -> int:
        return self._load_count


def main() -> None:
    cache = IconCache()

    # Simulate 100 widgets each requesting the same 3 icons
    widgets = ["toolbar", "sidebar", "menu"] * 33 + ["toolbar"]
    icons_used = []
    for widget in widgets:
        icon = cache.load("save", 16)
        icons_used.append(icon)

    print(f"Widgets: {len(widgets)}, load() calls: {cache.loads}")
    print(f"Unique icons in cache: {cache.size}")

    # All widgets point to the same icon object
    assert len(set(id(i) for i in icons_used)) == 1
    print("All widgets share the same icon object: True")


if __name__ == "__main__":
    main()
