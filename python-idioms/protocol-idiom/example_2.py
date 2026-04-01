"""
Example 2 — Duck typing vs nominal subtyping.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


# Nominal (ABC)
class NominalDrawable(ABC):
    @abstractmethod
    def draw(self) -> str: ...


# Structural (Protocol)
@runtime_checkable
class StructuralDrawable(Protocol):
    def draw(self) -> str: ...


class ExplicitShape(NominalDrawable):
    """Must explicitly inherit NominalDrawable."""

    def draw(self) -> str:
        return "ExplicitShape drawn"


class ImplicitShape:
    """Does NOT inherit anything — but has .draw()."""

    def draw(self) -> str:
        return "ImplicitShape drawn"


def render_nominal(item: NominalDrawable) -> str:
    return item.draw()


def render_structural(item: StructuralDrawable) -> str:
    return item.draw()


def main() -> None:
    explicit = ExplicitShape()
    implicit = ImplicitShape()

    print("--- Nominal (ABC) ---")
    print(render_nominal(explicit))
    try:
        render_nominal(implicit)  # type: ignore[arg-type] — works at runtime
        print(f"ImplicitShape works at runtime even without inheritance: True")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Structural (Protocol) ---")
    print(render_structural(explicit))
    print(render_structural(implicit))

    print(f"\nIsInstance checks:")
    print(f"  explicit isinstance(NominalDrawable): {isinstance(explicit, NominalDrawable)}")
    print(f"  implicit isinstance(NominalDrawable): {isinstance(implicit, NominalDrawable)}")
    print(f"  implicit isinstance(StructuralDrawable): {isinstance(implicit, StructuralDrawable)}")


if __name__ == "__main__":
    main()
