"""
Example 2 — MRO and cooperative super() with diamond inheritance.
"""
from __future__ import annotations


class Base:
    def operation(self) -> list[str]:
        return ["Base.operation"]


class MixinA(Base):
    def operation(self) -> list[str]:
        return ["MixinA.operation"] + super().operation()


class MixinB(Base):
    def operation(self) -> list[str]:
        return ["MixinB.operation"] + super().operation()


class Combined(MixinA, MixinB):
    """MRO: Combined → MixinA → MixinB → Base → object"""

    def operation(self) -> list[str]:
        return ["Combined.operation"] + super().operation()


def main() -> None:
    obj = Combined()
    result = obj.operation()
    print("Call chain:", result)

    print("\nMRO:")
    for i, cls in enumerate(Combined.__mro__):
        print(f"  {i}: {cls.__name__}")

    # Each mixin contributes once — no duplicate Base.operation
    assert result.count("Base.operation") == 1
    print("\nCooperative super(): Base called exactly once ✓")


if __name__ == "__main__":
    main()
