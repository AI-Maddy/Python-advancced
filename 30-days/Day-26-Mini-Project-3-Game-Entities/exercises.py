"""
Day 26 — Exercises: Game Entities (ECS)
=========================================
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from lesson import (
    CharacterState, CharacterStateMachine, Collider, CollisionEvent,
    Component, Entity, EventBus, Health, MovementSystem, Position,
    RenderSystem, Sprite, StateMachineError, System, Velocity, World,
)


# ---------------------------------------------------------------------------
# Exercise 1 — Add InventoryComponent
# ---------------------------------------------------------------------------
# TODO: Implement Inventory(Component) with:
#   - items: list[str] (item names)
#   - max_slots: int (default 10)
#   - add_item(name) → raises InventoryFullError if at capacity
#   - remove_item(name) → raises ItemNotFoundError if not present
#   - has_item(name) → bool

class InventoryFullError(Exception):
    """Raised when inventory has no free slots."""


class ItemNotFoundError(Exception):
    """Raised when removing an item that isn't in inventory."""


@dataclass
class Inventory(Component):
    """TODO: Inventory component."""
    max_slots: int = 10
    items: list[str] = field(default_factory=list)

    def add_item(self, name: str) -> None:
        """TODO: add item, raise InventoryFullError if full."""
        ...

    def remove_item(self, name: str) -> None:
        """TODO: remove item, raise ItemNotFoundError if missing."""
        ...

    def has_item(self, name: str) -> bool:
        """TODO: return True if item is in inventory."""
        ...
        return False


def exercise1_inventory() -> tuple[bool, bool, bool]:
    """
    Return (has_sword_after_add, error_on_remove_missing, error_when_full).
    - Create Inventory(max_slots=2)
    - Add 'sword', verify has_item
    - Try remove 'shield' (should raise)
    - Add 'shield' and 'axe' (axe should raise InventoryFullError)
    """
    # TODO
    ...
    return (False, False, False)


# ---------------------------------------------------------------------------
# Exercise 2 — Add AISystem
# ---------------------------------------------------------------------------
# TODO: Implement AISystem(System) that makes entities move toward the entity
#       with entity_id=0 (the "player") if they have a 'chase' tag.
#       The 'chase' tag is stored in Sprite.name == "enemy".
#       AI step: each frame, adjust enemy Velocity to point toward player
#       at a fixed speed (default 5 units/s).
#
# Only process entities that have Position AND Velocity AND Sprite(name="enemy").

class AISystem(System):
    """TODO: Chase-AI system."""

    def __init__(self, speed: float = 5.0) -> None:
        # TODO
        ...

    def update(self, world: World, dt: float) -> None:
        """TODO: steer all 'enemy' entities toward entity 0 (player)."""
        ...


def exercise2_ai_system() -> tuple[float, float]:
    """
    Create a world with player at (0,0) and enemy at (10,0).
    Add AISystem, run 1 frame (dt=1).
    Return (enemy_vx, enemy_vy) after update.
    Enemy should move toward (0,0): vx negative, vy ~0.
    """
    # TODO
    ...
    return (0.0, 0.0)


# ---------------------------------------------------------------------------
# Exercise 3 — JSON serialization of World state
# ---------------------------------------------------------------------------
# TODO: Implement serialize_world(world: World) -> str (JSON)
# Format:
# {
#   "entities": [
#     {
#       "id": 0,
#       "components": {
#         "Position": {"x": 1.0, "y": 2.0},
#         "Health":   {"hp": 80, "max_hp": 100},
#         ...
#       }
#     }
#   ]
# }
# Only serialize Position, Velocity, Health, Sprite components.

def serialize_world(world: World) -> str:
    """TODO: Return JSON string representing all entities in the world."""
    # TODO
    ...
    return "{}"


def exercise3_serialize() -> tuple[int, bool]:
    """
    Return (number_of_entities_in_json, has_position_key).
    Create 2 entities each with Position and Health.
    """
    # TODO
    ...
    return (0, False)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_inventory())
    print("Exercise 2:", exercise2_ai_system())
    print("Exercise 3:", exercise3_serialize())
