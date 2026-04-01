Day 10 — Type Hints: Annotated, TypeGuard, and Advanced Typing
================================================================

TypeGuard
----------
.. code-block:: python

    from typing import TypeGuard

    def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
        return all(isinstance(x, str) for x in val)

    items: list[object] = ["a", "b"]
    if is_str_list(items):
        items[0].upper()  # safe: mypy knows items is list[str]

Annotated
----------
.. code-block:: python

    from typing import Annotated
    PositiveInt = Annotated[int, "must be > 0"]

    def f(x: PositiveInt) -> None: ...

The first argument is the type; extra args are metadata for tools/libraries.

Literal and Final
------------------
.. code-block:: python

    from typing import Literal, Final

    Mode = Literal["r", "w", "a"]
    MAX: Final[int] = 100   # cannot be reassigned

TypeAlias
----------
.. code-block:: python

    from typing import TypeAlias
    Vector2D: TypeAlias = tuple[float, float]

Union and Optional
-------------------
.. code-block:: python

    # Python 3.10+
    def f(x: int | None) -> str | None: ...

    # Pre-3.10
    from typing import Optional, Union
    def f(x: Optional[int]) -> Optional[str]: ...
