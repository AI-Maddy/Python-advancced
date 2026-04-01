"""
Tests for Day 26 — Game Entities (ECS)
Run with: pytest tests/test_game.py -v
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from lesson import (
    CharacterState, CharacterStateMachine, Collider, CollisionEvent,
    CollisionSystem, Component, Entity, EventBus, Health, MovementSystem,
    Position, RenderSystem, Sprite, StateMachineError, Velocity, World,
)


# ---------------------------------------------------------------------------
# World / Entity creation
# ---------------------------------------------------------------------------

@pytest.fixture
def world() -> World:
    return World()


def test_create_entity_returns_unique_ids(world: World) -> None:
    e1 = world.create_entity()
    e2 = world.create_entity()
    e3 = world.create_entity()
    assert len({e1, e2, e3}) == 3


def test_add_and_get_component(world: World) -> None:
    e = world.create_entity()
    world.add_component(e, Position(3, 4))
    pos = world.get_component(e, Position)
    assert pos is not None
    assert pos.x == 3.0
    assert pos.y == 4.0


def test_get_missing_component_returns_none(world: World) -> None:
    e = world.create_entity()
    assert world.get_component(e, Position) is None


def test_has_component(world: World) -> None:
    e = world.create_entity()
    world.add_component(e, Health(50, 100))
    assert world.has_component(e, Health) is True
    assert world.has_component(e, Position) is False


def test_destroy_entity_removes_components(world: World) -> None:
    e = world.create_entity()
    world.add_component(e, Position(0, 0))
    world.destroy_entity(e)
    assert world.get_component(e, Position) is None


def test_get_entities_with_multiple_components(world: World) -> None:
    e1 = world.create_entity()
    world.add_component(e1, Position(0, 0))
    world.add_component(e1, Velocity(1, 0))

    e2 = world.create_entity()
    world.add_component(e2, Position(5, 5))
    # e2 has no Velocity

    result = world.get_entities_with(Position, Velocity)
    assert e1 in result
    assert e2 not in result


# ---------------------------------------------------------------------------
# Component tests
# ---------------------------------------------------------------------------

def test_health_take_damage() -> None:
    h = Health(100, 100)
    h.take_damage(30)
    assert h.hp == 70


def test_health_cannot_go_below_zero() -> None:
    h = Health(10, 100)
    h.take_damage(50)
    assert h.hp == 0
    assert not h.is_alive


def test_health_heal() -> None:
    h = Health(50, 100)
    h.heal(30)
    assert h.hp == 80


def test_health_cannot_exceed_max() -> None:
    h = Health(90, 100)
    h.heal(50)
    assert h.hp == 100


def test_health_percentage() -> None:
    h = Health(75, 100)
    assert h.percentage == pytest.approx(0.75)


def test_health_invalid_max_hp() -> None:
    with pytest.raises(ValueError):
        Health(10, 0)


def test_position_distance() -> None:
    a = Position(0, 0)
    b = Position(3, 4)
    assert a.distance_to(b) == pytest.approx(5.0)


# ---------------------------------------------------------------------------
# System tests
# ---------------------------------------------------------------------------

def test_movement_system_updates_position(world: World) -> None:
    e = world.create_entity()
    world.add_component(e, Position(0, 0))
    world.add_component(e, Velocity(10, 5))
    world.add_system(MovementSystem())
    world.update(dt=0.5)
    pos = world.get_component(e, Position)
    assert pos is not None
    assert pos.x == pytest.approx(5.0)
    assert pos.y == pytest.approx(2.5)


def test_movement_system_ignores_static_entities(world: World) -> None:
    e = world.create_entity()
    world.add_component(e, Position(3, 3))
    # No Velocity component → should not move
    world.add_system(MovementSystem())
    world.update(dt=1.0)
    pos = world.get_component(e, Position)
    assert pos.x == pytest.approx(3.0)
    assert pos.y == pytest.approx(3.0)


def test_collision_system_detects_overlap(world: World) -> None:
    e1 = world.create_entity()
    world.add_component(e1, Position(0, 0))
    world.add_component(e1, Collider(radius=2.0))

    e2 = world.create_entity()
    world.add_component(e2, Position(1, 0))  # distance=1, sum_radii=4 → overlap
    world.add_component(e2, Collider(radius=2.0))

    cs = CollisionSystem()
    world.add_system(cs)
    world.update(dt=0)
    assert len(cs.collisions) == 1


def test_collision_system_no_overlap(world: World) -> None:
    e1 = world.create_entity()
    world.add_component(e1, Position(0, 0))
    world.add_component(e1, Collider(radius=1.0))

    e2 = world.create_entity()
    world.add_component(e2, Position(100, 0))  # far away
    world.add_component(e2, Collider(radius=1.0))

    cs = CollisionSystem()
    world.add_system(cs)
    world.update(dt=0)
    assert len(cs.collisions) == 0


def test_collision_fires_event(world: World) -> None:
    bus = EventBus()
    events: list[CollisionEvent] = []
    bus.subscribe(CollisionEvent, events.append)

    e1 = world.create_entity()
    world.add_component(e1, Position(0, 0))
    world.add_component(e1, Collider(radius=2.0))

    e2 = world.create_entity()
    world.add_component(e2, Position(1, 0))
    world.add_component(e2, Collider(radius=2.0))

    world.add_system(CollisionSystem(event_bus=bus))
    world.update(dt=0)
    assert len(events) == 1


def test_render_system_orders_by_layer(world: World) -> None:
    rs = RenderSystem()
    world.add_system(rs)

    e1 = world.create_entity()
    world.add_component(e1, Sprite("background", layer=0))
    world.add_component(e1, Position(0, 0))

    e2 = world.create_entity()
    world.add_component(e2, Sprite("player", layer=2))
    world.add_component(e2, Position(0, 0))

    log = rs.render(world)
    layers = [("background" in l, "player" in l) for l in log]
    # background should appear first in log
    bg_idx = next(i for i, (bg, _) in enumerate(layers) if bg)
    pl_idx = next(i for i, (_, pl) in enumerate(layers) if pl)
    assert bg_idx < pl_idx


# ---------------------------------------------------------------------------
# State machine tests
# ---------------------------------------------------------------------------

def test_state_machine_initial_state() -> None:
    sm = CharacterStateMachine()
    assert sm.state == CharacterState.IDLE


def test_state_machine_valid_transition() -> None:
    sm = CharacterStateMachine()
    sm.transition(CharacterState.RUNNING)
    assert sm.state == CharacterState.RUNNING


def test_state_machine_invalid_transition_raises() -> None:
    sm = CharacterStateMachine(CharacterState.DEAD)
    with pytest.raises(StateMachineError):
        sm.transition(CharacterState.IDLE)


def test_state_machine_full_sequence() -> None:
    sm = CharacterStateMachine()
    sm.transition(CharacterState.RUNNING)
    sm.transition(CharacterState.JUMPING)
    sm.transition(CharacterState.DEAD)
    assert sm.history == [
        CharacterState.IDLE,
        CharacterState.RUNNING,
        CharacterState.JUMPING,
        CharacterState.DEAD,
    ]


# ---------------------------------------------------------------------------
# EventBus tests
# ---------------------------------------------------------------------------

def test_event_bus_dispatch() -> None:
    bus = EventBus()
    received: list[CollisionEvent] = []
    bus.subscribe(CollisionEvent, received.append)
    evt = CollisionEvent(entity_a=0, entity_b=1, distance=0.5)
    bus.emit(evt)
    assert received == [evt]


def test_event_bus_unsubscribe() -> None:
    bus = EventBus()
    received: list[CollisionEvent] = []

    def listener(e: CollisionEvent) -> None:
        received.append(e)

    bus.subscribe(CollisionEvent, listener)
    bus.emit(CollisionEvent(0, 1, 0.5))
    bus.unsubscribe(CollisionEvent, listener)
    bus.emit(CollisionEvent(0, 1, 0.5))
    assert len(received) == 1   # only first event


def test_event_bus_different_types() -> None:
    import importlib.util as _il26, os as _oo26, sys as _ss26
    _l_path = _oo26.path.join(_oo26.path.dirname(_oo26.path.dirname(_oo26.path.abspath(__file__))), "lesson.py")
    _lspec = _il26.spec_from_file_location("lesson_day26", _l_path)
    _lmod = _il26.module_from_spec(_lspec)
    _ss26.modules["lesson_day26"] = _lmod
    _lspec.loader.exec_module(_lmod)
    DamageEvent = _lmod.DamageEvent
    bus = EventBus()
    col_log: list[CollisionEvent] = []
    dmg_log: list[DamageEvent] = []

    bus.subscribe(CollisionEvent, col_log.append)
    bus.subscribe(DamageEvent, dmg_log.append)

    bus.emit(CollisionEvent(0, 1, 1.0))
    bus.emit(DamageEvent(entity=0, amount=10))

    assert len(col_log) == 1
    assert len(dmg_log) == 1
