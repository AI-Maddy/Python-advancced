"""
Day 26 — Solutions: Game Entities (ECS)
=========================================
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from typing import Any

from lesson import (
    CharacterState, CharacterStateMachine, Collider, CollisionEvent,
    Component, Entity, EventBus, Health, MovementSystem, Position,
    RenderSystem, Sprite, StateMachineError, System, Velocity, World,
)


# ---------------------------------------------------------------------------
# Solution 1 — InventoryComponent
# ---------------------------------------------------------------------------

class InventoryFullError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


@dataclass
class Inventory(Component):
    max_slots: int = 10
    items: list[str] = field(default_factory=list)

    def add_item(self, name: str) -> None:
        if len(self.items) >= self.max_slots:
            raise InventoryFullError(f"Inventory full ({self.max_slots} slots)")
        self.items.append(name)

    def remove_item(self, name: str) -> None:
        if name not in self.items:
            raise ItemNotFoundError(f"{name!r} not in inventory")
        self.items.remove(name)

    def has_item(self, name: str) -> bool:
        return name in self.items


def exercise1_inventory() -> tuple[bool, bool, bool]:
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
# Solution 2 — AISystem
# ---------------------------------------------------------------------------

class AISystem(System):
    def __init__(self, speed: float = 5.0) -> None:
        self.speed = speed

    def update(self, world: World, dt: float) -> None:
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
# Solution 3 — JSON World Serialization
# ---------------------------------------------------------------------------

def serialize_world(world: World) -> str:
    all_entities = set()
    for comp_store in world._components.values():
        all_entities.update(comp_store.keys())

    output: list[dict[str, Any]] = []
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
    print("Solution 1:", exercise1_inventory())
    print("Solution 2:", exercise2_ai_system())
    print("Solution 3:", exercise3_serialize())
