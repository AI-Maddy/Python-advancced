Day 26 — Mini-Project 3: Game Entities (ECS)
=============================================

Entity Component System Architecture
--------------------------------------

Traditional OOP inheritance for game objects becomes unwieldy:
``Player(Character)`` vs ``Enemy(Character)`` vs ``FlyingEnemy(Enemy)``...

ECS replaces deep hierarchies with composition:

* **Entity** — just an integer ID.  No data, no behaviour.
* **Component** — pure data (position, health, sprite).  No behaviour.
* **System** — behaviour that operates on entities having specific components.

.. code-block:: text

    World
    ├── EntityManager (creates IDs)
    ├── Component Store: {ComponentType: {EntityID: Component}}
    └── Systems: [MovementSystem, CollisionSystem, RenderSystem, ...]

Benefits: easy to add behaviour (new System), easy to mix components
(flying + shooting + health), no deep class hierarchies.

World API
---------

.. code-block:: python

    world = World()
    player = world.create_entity()
    world.add_component(player, Position(0, 0))
    world.add_component(player, Velocity(5, 0))

    entities = world.get_entities_with(Position, Velocity)
    pos = world.get_component(player, Position)

    world.update(dt=0.016)   # runs all systems

State Machine
-------------

.. code-block:: python

    class CharacterState(Enum):
        IDLE = auto()
        RUNNING = auto()
        DEAD = auto()

    sm = CharacterStateMachine()
    sm.transition(CharacterState.RUNNING)   # OK
    sm.transition(CharacterState.DEAD)      # OK
    sm.transition(CharacterState.IDLE)      # raises StateMachineError

EventBus
--------

Decouples collision detection from damage handling:

.. code-block:: python

    bus = EventBus()
    bus.subscribe(CollisionEvent, lambda e: apply_damage(e.entity_a))
    bus.emit(CollisionEvent(entity_a=0, entity_b=1, distance=0.5))

Pattern Connections
--------------------

.. list-table::
   :header-rows: 1

   * - Concept
     - Pattern Used
   * - Component storage
     - Registry (dict of dicts)
   * - System pipeline
     - Chain of Responsibility
   * - Event notification
     - Observer (EventBus)
   * - State transitions
     - State Machine
   * - Composite entity grouping
     - Composite (ShapeGroup equivalent)
