"""
Example 2 — Game sprite factory via prototype registry.

Pre-configured sprite prototypes are cloned and placed at runtime positions.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Self


@dataclass
class Sprite:
    """Game sprite prototype."""
    name: str
    width: int
    height: int
    color: str
    animations: list[str] = field(default_factory=list)
    # Extrinsic state set per-instance:
    x: float = 0.0
    y: float = 0.0

    def clone(self) -> Self:
        return copy.deepcopy(self)

    def place(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Sprite({self.name!r} at ({self.x},{self.y}))"


class SpriteFactory:
    """Registry of named sprite prototypes."""

    _registry: dict[str, Sprite] = {}

    @classmethod
    def register(cls, sprite: Sprite) -> None:
        cls._registry[sprite.name] = sprite

    @classmethod
    def create(cls, name: str, x: float = 0, y: float = 0) -> Sprite:
        sprite = cls._registry[name].clone()
        sprite.place(x, y)
        return sprite


def main() -> None:
    # Register prototypes once at startup
    SpriteFactory.register(Sprite("enemy", 32, 32, "red", ["walk", "attack", "die"]))
    SpriteFactory.register(Sprite("coin", 16, 16, "gold", ["spin"]))
    SpriteFactory.register(Sprite("hero", 48, 48, "blue", ["idle", "run", "jump"]))

    # Spawn many instances cheaply
    enemies = [SpriteFactory.create("enemy", x=i * 50.0, y=100.0) for i in range(5)]
    coins = [SpriteFactory.create("coin", x=i * 30.0, y=200.0) for i in range(8)]
    hero = SpriteFactory.create("hero", x=240.0, y=300.0)

    print("Hero:", hero)
    for e in enemies:
        print("Enemy:", e)
    print(f"Spawned {len(coins)} coins")

    # Mutating a clone doesn't affect prototype
    enemies[0].animations.append("rage")
    fresh_enemy = SpriteFactory.create("enemy")
    assert "rage" not in fresh_enemy.animations
    print("Prototype animations unaffected:", fresh_enemy.animations)


if __name__ == "__main__":
    main()
