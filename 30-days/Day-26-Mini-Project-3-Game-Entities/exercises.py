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
        if len(self.items) >= self.max_slots:
            raise InventoryFullError(f"Inventory full ({self.max_slots} slots)")
        self.items.append(name)

    def remove_item(self, name: str) -> None:
        """TODO: remove item, raise ItemNotFoundError if missing."""
        if name not in self.items:
            raise ItemNotFoundError(f"{name!r} not in inventory")
        self.items.remove(name)

    def has_item(self, name: str) -> bool:
        """TODO: return True if item is in inventory."""
        return name in self.items


def exercise1_inventory() -> tuple[bool, bool, bool]:
    """
    Return (has_sword_after_add, error_on_remove_missing, error_when_full).
    - Create Inventory(max_slots=2)
    - Add 'sword', verify has_item
    - Try remove 'shield' (should raise)
    - Add 'shield' and 'axe' (axe should raise InventoryFullError)
    """
    inv = Inventory(max_slots=2)
    inv.add_item("sword")
    has_sword = inv.has_item("sword")

    remove_error = False
    try:
        inv.remove_item("shield")
    except ItemNotFoundError:
        remove_error = True

    inv.add_item("shield")
    full_error = False
    try:
        inv.add_item("axe")
    except InventoryFullError:
        full_error = True

    return (has_sword, remove_error, full_error)


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
        self.speed = speed

    def update(self, world: World, dt: float) -> None:
        """TODO: steer all 'enemy' entities toward entity 0 (player)."""
        import math
        player_pos = world.get_component(0, Position)
        if player_pos is None:
            return
        for entity in world.get_entities_with(Position, Velocity, Sprite):
            sprite = world.get_component(entity, Sprite)
            if sprite and sprite.name == "enemy":
                pos = world.get_component(entity, Position)
                vel = world.get_component(entity, Velocity)
                if pos and vel:
                    dx = player_pos.x - pos.x
                    dy = player_pos.y - pos.y
                    dist = math.sqrt(dx ** 2 + dy ** 2)
                    if dist > 0:
                        vel.dx = (dx / dist) * self.speed
                        vel.dy = (dy / dist) * self.speed


def exercise2_ai_system() -> tuple[float, float]:
    """
    Create a world with player at (0,0) and enemy at (10,0).
    Add AISystem, run 1 frame (dt=1).
    Return (enemy_vx, enemy_vy) after update.
    Enemy should move toward (0,0): vx negative, vy ~0.
    """
    world = World()

    player = world.create_entity()   # entity 0
    world.add_component(player, Position(0, 0))
    world.add_component(player, Sprite("player"))

    enemy = world.create_entity()    # entity 1
    world.add_component(enemy, Position(10, 0))
    world.add_component(enemy, Velocity(0, 0))
    world.add_component(enemy, Sprite("enemy"))

    ai = AISystem(speed=5.0)
    world.add_system(ai)
    world.update(dt=1.0)

    vel = world.get_component(enemy, Velocity)
    return (vel.dx if vel else 0.0, vel.dy if vel else 0.0)


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
    all_entities: set[int] = set()
    for comp_store in world._components.values():
        all_entities.update(comp_store.keys())

    output: list[dict] = []
    for eid in sorted(all_entities):
        comps: dict[str, Any] = {}
        pos = world.get_component(eid, Position)
        vel = world.get_component(eid, Velocity)
        health = world.get_component(eid, Health)
        sprite = world.get_component(eid, Sprite)

        if pos:
            comps["Position"] = {"x": pos.x, "y": pos.y}
        if vel:
            comps["Velocity"] = {"dx": vel.dx, "dy": vel.dy}
        if health:
            comps["Health"] = {"hp": health.hp, "max_hp": health.max_hp}
        if sprite:
            comps["Sprite"] = {"name": sprite.name, "layer": sprite.layer}

        output.append({"id": eid, "components": comps})

    return json.dumps({"entities": output}, indent=2)


def exercise3_serialize() -> tuple[int, bool]:
    """
    Return (number_of_entities_in_json, has_position_key).
    Create 2 entities each with Position and Health.
    """
    world = World()
    for i in range(2):
        e = world.create_entity()
        world.add_component(e, Position(float(i), float(i)))
        world.add_component(e, Health(100, 100))

    json_str = serialize_world(world)
    data = json.loads(json_str)
    entities = data["entities"]
    has_position = any("Position" in e["components"] for e in entities)
    return (len(entities), has_position)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_inventory())
    print("Exercise 2:", exercise2_ai_system())
    print("Exercise 3:", exercise3_serialize())
