"""
Example 2 — __class_getitem__ for typed containers.
"""
from __future__ import annotations

from classmethod_factory import TypedList


def main() -> None:
    IntList = TypedList[int]
    StrList = TypedList[str]

    ints = IntList([1, 2, 3, 4, 5])
    strs = StrList(["alpha", "beta", "gamma"])

    print(ints)
    print(strs)

    # Wrong type is rejected
    try:
        IntList([1, 2, "three"])
    except TypeError as e:
        print(f"Rejected: {e}")

    try:
        StrList([1, 2, 3])
    except TypeError as e:
        print(f"Rejected: {e}")

    # Subclassing works too
    class PositiveIntList(TypedList[int]):
        def __init__(self, items: list) -> None:
            super().__init__(items)
            if any(v <= 0 for v in self._items):
                raise ValueError("All values must be positive")

    pos = PositiveIntList([1, 2, 3])
    print(pos)

    try:
        PositiveIntList([1, -2, 3])
    except ValueError as e:
        print(f"Rejected negative: {e}")


if __name__ == "__main__":
    main()
