Day 11 — Generic OOP Design
============================

Generic Repository Pattern
----------------------------
.. code-block:: python

    class Repository(Generic[T, ID]):
        def save(self, id: ID, entity: T) -> None: ...
        def find_by_id(self, id: ID) -> T | None: ...
        def find_all(self) -> list[T]: ...

Result[T, E] — Explicit Error Handling
-----------------------------------------
.. code-block:: python

    class Ok(Generic[T]):
        def __init__(self, value: T) -> None: ...
        def is_ok(self) -> bool: return True
        def unwrap(self) -> T: return self._value

    class Err(Generic[E]):
        def __init__(self, error: E) -> None: ...
        def is_ok(self) -> bool: return False
        def unwrap(self): raise self._error

Result types avoid exceptions for expected failures, making error handling
explicit in the type system.  C++ equivalent: ``std::expected<T, E>`` (C++23).

Generic Event Bus
------------------
.. code-block:: python

    class EventBus(Generic[T]):
        def subscribe(self, handler: Callable[[T], None]) -> None: ...
        def publish(self, event: T) -> None: ...
