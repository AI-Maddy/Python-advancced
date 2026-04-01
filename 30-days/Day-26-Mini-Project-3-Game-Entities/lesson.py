"""
Day 26 — Mini-Project 3: Game Entities (ECS)
=============================================
Entity Component System:
  Entity (int ID), Component ABC, System ABC
  Components: Position, Velocity, Health, Sprite, Collider
  Systems: MovementSystem, CollisionSystem, RenderSystem
  World: entity registry + system runner
  State machine: CharacterState enum + transitions
  Observer: EventBus with typed events
"""
from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, ClassVar, TypeVar

T = TypeVar("T")

# ===========================================================================
# Entity — just an integer ID
# ===========================================================================

Entity = int   # type alias — entities are just integer IDs


class EntityManager:
    """Generates unique entity IDs."""

    def __init__(self) -> None:
        self._next_id: int = 0

    def create(self) -> Entity:
        """Create and return a new entity ID."""
        eid = self._next_id
        self._next_id += 1
        return eid


# ===========================================================================
# Component ABC
# ===========================================================================

class Component(ABC):
    """Marker base class for all ECS components."""


# ===========================================================================
# Concrete Components
# ===========================================================================

@dataclass
class Position(Component):
    """2D world position."""
    x: float = 0.0
    y: float = 0.0

    def distance_to(self, other: Position) -> float:
        """Euclidean distance to another position."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


@dataclass
class Velocity(Component):
    """2D velocity in units/second."""
    dx: float = 0.0
    dy: float = 0.0


@dataclass
class Health(Component):
    """Current and maximum hit points."""
    hp: float
    max_hp: float

    def __post_init__(self) -> None:
        if self.max_hp <= 0:
            raise ValueError("max_hp must be > 0")
        if self.hp < 0:
            self.hp = 0.0
        self.hp = min(self.hp, self.max_hp)

    @property
    def is_alive(self) -> bool:
        """Return True if hp > 0."""
        return self.hp > 0

    @property
    def percentage(self) -> float:
        """Return HP as a fraction 0.0–1.0."""
        return self.hp / self.max_hp

    def take_damage(self, amount: float) -> None:
        """Reduce HP by amount (minimum 0)."""
        self.hp = max(0.0, self.hp - amount)

    def heal(self, amount: float) -> None:
        """Increase HP by amount (maximum max_hp)."""
        self.hp = min(self.max_hp, self.hp + amount)


@dataclass
class Sprite(Component):
    """Visual representation."""
    name: str
    layer: int = 0


@dataclass
class Collider(Component):
    """Circular collision shape."""
    radius: float
    is_trigger: bool = False   # trigger: detect overlap but don't resolve


# ===========================================================================
# World — entity registry and component storage
# ===========================================================================

class World:
    """
    Central ECS registry.

    Components are stored in a dict-of-dicts:
        _components[ComponentType][entity_id] = component_instance
    """

    def __init__(self) -> None:
        self._entity_manager = EntityManager()
        self._components: dict[type[Component], dict[Entity, Component]] = {}
        self._systems: list[System] = []

    # --- Entity management ---

    def create_entity(self) -> Entity:
        """Create a new entity and return its ID."""
        return self._entity_manager.create()

    def destroy_entity(self, entity: Entity) -> None:
        """Remove all components for this entity."""
        for store in self._components.values():
            store.pop(entity, None)

    # --- Component management ---

    def add_component(self, entity: Entity, component: Component) -> None:
        """Attach a component to an entity."""
        comp_type = type(component)
        if comp_type not in self._components:
            self._components[comp_type] = {}
        self._components[comp_type][entity] = component

    def get_component(self, entity: Entity, comp_type: type[T]) -> T | None:  # type: ignore[type-var]
        """Return the component of comp_type for entity, or None."""
        return self._components.get(comp_type, {}).get(entity)  # type: ignore[return-value]

    def has_component(self, entity: Entity, comp_type: type[Component]) -> bool:
        """Return True if entity has a component of comp_type."""
        return entity in self._components.get(comp_type, {})

    def get_entities_with(self, *comp_types: type[Component]) -> list[Entity]:
        """Return all entities that have ALL of the specified component types."""
        if not comp_types:
            return []
        candidates = set(self._components.get(comp_types[0], {}).keys())
        for ct in comp_types[1:]:
            candidates &= set(self._components.get(ct, {}).keys())
        return list(candidates)

    # --- System management ---

    def add_system(self, system: System) -> None:
        """Register a system."""
        self._systems.append(system)

    def update(self, dt: float) -> None:
        """Run all registered systems with timestep dt."""
        for system in self._systems:
            system.update(self, dt)


# ===========================================================================
# System ABC
# ===========================================================================

class System(ABC):
    """Base class for ECS systems."""

    @abstractmethod
    def update(self, world: World, dt: float) -> None:
        """Process all relevant entities for one frame."""


# ===========================================================================
# Concrete Systems
# ===========================================================================

class MovementSystem(System):
    """
    Moves entities that have both Position and Velocity components.
    Position += Velocity * dt
    """

    def update(self, world: World, dt: float) -> None:
        for entity in world.get_entities_with(Position, Velocity):
            pos = world.get_component(entity, Position)
            vel = world.get_component(entity, Velocity)
            if pos and vel:
                pos.x += vel.dx * dt
                pos.y += vel.dy * dt


class CollisionSystem(System):
    """
    Detects overlapping Collider+Position pairs.
    Fires collision events on the EventBus (if injected).
    """

    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._bus = event_bus
        self.collisions: list[tuple[Entity, Entity]] = []

    def update(self, world: World, dt: float) -> None:
        self.collisions = []
        entities = world.get_entities_with(Position, Collider)
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                ea, eb = entities[i], entities[j]
                pos_a = world.get_component(ea, Position)
                pos_b = world.get_component(eb, Position)
                col_a = world.get_component(ea, Collider)
                col_b = world.get_component(eb, Collider)
                if pos_a and pos_b and col_a and col_b:
                    dist = pos_a.distance_to(pos_b)
                    if dist < col_a.radius + col_b.radius:
                        self.collisions.append((ea, eb))
                        if self._bus:
                            self._bus.emit(CollisionEvent(ea, eb, dist))


class RenderSystem(System):
    """
    'Renders' entities with Sprite + Position by collecting render commands.
    In a real game this would draw to a surface; here we collect strings.
    """

    def __init__(self) -> None:
        self.render_log: list[str] = []

    def update(self, world: World, dt: float) -> None:
        entities = world.get_entities_with(Sprite, Position)
        sorted_entities = sorted(
            entities,
            key=lambda e: (
                world.get_component(e, Sprite).layer  # type: ignore[union-attr]
                if world.get_component(e, Sprite) else 0
            ),
        )
        for entity in sorted_entities:
            sprite = world.get_component(entity, Sprite)
            pos    = world.get_component(entity, Position)
            if sprite and pos:
                self.render_log.append(
                    f"DRAW {sprite.name} @ ({pos.x:.1f}, {pos.y:.1f}) [layer {sprite.layer}]"
                )

    def render(self, world: World) -> list[str]:
        """Convenience: update then return log."""
        self.render_log = []
        self.update(world, 0)
        return list(self.render_log)


# ===========================================================================
# State machine — CharacterState
# ===========================================================================

class CharacterState(Enum):
    """Possible character states."""
    IDLE    = auto()
    RUNNING = auto()
    JUMPING = auto()
    DEAD    = auto()


# Valid state transitions
_TRANSITIONS: dict[CharacterState, set[CharacterState]] = {
    CharacterState.IDLE:    {CharacterState.RUNNING, CharacterState.JUMPING, CharacterState.DEAD},
    CharacterState.RUNNING: {CharacterState.IDLE, CharacterState.JUMPING, CharacterState.DEAD},
    CharacterState.JUMPING: {CharacterState.IDLE, CharacterState.RUNNING, CharacterState.DEAD},
    CharacterState.DEAD:    set(),   # terminal state
}


class StateMachineError(Exception):
    """Raised on invalid state transition."""


class CharacterStateMachine:
    """
    Finite state machine for a character.
    Enforces allowed transitions.
    """

    def __init__(self, initial: CharacterState = CharacterState.IDLE) -> None:
        self._state = initial
        self._history: list[CharacterState] = [initial]

    @property
    def state(self) -> CharacterState:
        """Current state."""
        return self._state

    def transition(self, new_state: CharacterState) -> None:
        """
        Move to new_state if the transition is valid.

        Raises:
            StateMachineError: if the transition is not allowed.
        """
        allowed = _TRANSITIONS.get(self._state, set())
        if new_state not in allowed:
            raise StateMachineError(
                f"Cannot transition from {self._state.name} to {new_state.name}"
            )
        self._state = new_state
        self._history.append(new_state)

    @property
    def history(self) -> list[CharacterState]:
        """All states visited, in order."""
        return list(self._history)


# ===========================================================================
# EventBus — observer for game events
# ===========================================================================

@dataclass
class CollisionEvent:
    """Fired when two entities collide."""
    entity_a: Entity
    entity_b: Entity
    distance: float


@dataclass
class DamageEvent:
    """Fired when an entity takes damage."""
    entity: Entity
    amount: float
    source: Entity | None = None


GameEvent = CollisionEvent | DamageEvent


class EventBus:
    """
    Simple event bus for game events.
    Listeners are callables keyed by event type.
    """

    def __init__(self) -> None:
        self._listeners: dict[type, list[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: type[T], listener: Callable[[T], None]) -> None:
        """Register a listener for a specific event type."""
        self._listeners.setdefault(event_type, []).append(listener)  # type: ignore[arg-type]

    def unsubscribe(self, event_type: type[T], listener: Callable[[T], None]) -> None:
        """Unregister a listener."""
        self._listeners.get(event_type, []).remove(listener)  # type: ignore[arg-type]

    def emit(self, event: Any) -> None:
        """Dispatch event to all registered listeners."""
        for listener in self._listeners.get(type(event), []):
            listener(event)


# ===========================================================================
# Main demo
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 26 — Game Entities (ECS)")
    print("=" * 60)

    # Setup
    bus = EventBus()
    world = World()

    collision_log: list[str] = []
    bus.subscribe(CollisionEvent, lambda e: collision_log.append(
        f"Collision: {e.entity_a} ↔ {e.entity_b} (dist={e.distance:.2f})"
    ))

    movement  = MovementSystem()
    collision = CollisionSystem(event_bus=bus)
    render    = RenderSystem()

    world.add_system(movement)
    world.add_system(collision)
    world.add_system(render)

    # Create entities
    player = world.create_entity()
    world.add_component(player, Position(0, 0))
    world.add_component(player, Velocity(10, 5))
    world.add_component(player, Health(100, 100))
    world.add_component(player, Sprite("player_sprite", layer=1))
    world.add_component(player, Collider(radius=1.0))

    enemy = world.create_entity()
    world.add_component(enemy, Position(5, 0))
    world.add_component(enemy, Velocity(-3, 0))
    world.add_component(enemy, Health(50, 50))
    world.add_component(enemy, Sprite("enemy_sprite", layer=1))
    world.add_component(enemy, Collider(radius=1.0))

    print("\n--- Simulation (3 frames, dt=0.1) ---")
    for frame in range(3):
        world.update(dt=0.1)
        pos_p = world.get_component(player, Position)
        pos_e = world.get_component(enemy, Position)
        print(f"Frame {frame+1}: player=({pos_p.x:.2f},{pos_p.y:.2f}) enemy=({pos_e.x:.2f},{pos_e.y:.2f})")

    print("\nCollision events:", collision_log)

    # State machine
    print("\n--- CharacterState machine ---")
    sm = CharacterStateMachine()
    sm.transition(CharacterState.RUNNING)
    sm.transition(CharacterState.JUMPING)
    sm.transition(CharacterState.IDLE)
    sm.transition(CharacterState.DEAD)
    print(f"State history: {[s.name for s in sm.history]}")

    try:
        sm.transition(CharacterState.IDLE)
    except StateMachineError as e:
        print(f"Error (expected): {e}")

    # Render
    print("\n--- Render ---")
    for line in render.render(world):
        print(" ", line)
