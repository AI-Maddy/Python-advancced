"""
__slots__ Idiom — memory-efficient attribute storage.

Demonstrates:
* __slots__ elimination of __dict__
* Memory comparison (sys.getsizeof)
* Slots with inheritance
* Interaction with __dict__ and __weakref__
"""
from __future__ import annotations

import sys
import tracemalloc
import weakref


# ---------------------------------------------------------------------------
# Without slots
# ---------------------------------------------------------------------------
class PointWithDict:
    """Regular class — stores attributes in a __dict__."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


# ---------------------------------------------------------------------------
# With slots
# ---------------------------------------------------------------------------
class PointWithSlots:
    """Slots class — no __dict__, lower memory footprint.

    Only ``x`` and ``y`` are valid attributes.
    """

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


# ---------------------------------------------------------------------------
# Slots with __weakref__ support
# ---------------------------------------------------------------------------
class WeakRefPoint:
    """Slots class that also supports weak references."""

    __slots__ = ("x", "y", "__weakref__")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


# ---------------------------------------------------------------------------
# Slots inheritance — subclass must re-declare slots to avoid __dict__
# ---------------------------------------------------------------------------
class ColoredPoint(PointWithSlots):
    """Subclass adds a color slot; no __dict__ on instances."""

    __slots__ = ("color",)

    def __init__(self, x: float, y: float, color: str = "black") -> None:
        super().__init__(x, y)
        self.color = color


class ColoredPointBad(PointWithSlots):
    """Subclass that does NOT declare __slots__ — gets a __dict__ back."""

    # No __slots__ — Python adds __dict__ to this subclass
    def __init__(self, x: float, y: float, color: str = "black") -> None:
        super().__init__(x, y)
        self.color = color


# ---------------------------------------------------------------------------
# Memory comparison utility
# ---------------------------------------------------------------------------
def measure_memory_n(cls: type, n: int = 100_000) -> int:
    """Return peak memory used (bytes) when creating n instances of cls."""
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()
    instances = [cls(float(i), float(i)) for i in range(n)]  # type: ignore[call-arg]
    snapshot2 = tracemalloc.take_snapshot()
    tracemalloc.stop()
    stats = snapshot2.compare_to(snapshot1, "lineno")
    total = sum(s.size_diff for s in stats if s.size_diff > 0)
    del instances
    return total


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # __dict__ presence
    pd = PointWithDict(1.0, 2.0)
    ps = PointWithSlots(1.0, 2.0)

    print(f"PointWithDict  has __dict__: {hasattr(pd, '__dict__')}")  # True
    print(f"PointWithSlots has __dict__: {hasattr(ps, '__dict__')}")  # False

    # getsizeof
    print(f"\nsys.getsizeof(PointWithDict  instance): {sys.getsizeof(pd)}")
    print(f"sys.getsizeof(PointWithSlots instance): {sys.getsizeof(ps)}")

    # Dynamic attribute assignment
    pd.z = 3.0   # works
    try:
        ps.z = 3.0  # type: ignore[attr-defined]
    except AttributeError as e:
        print(f"\nSlots blocks dynamic attrs: {e}")

    # weakref support
    wr_pt = WeakRefPoint(3.0, 4.0)
    ref = weakref.ref(wr_pt)
    print(f"\nweak ref alive: {ref() is not None}")
    del wr_pt
    print(f"weak ref after del: {ref()}")  # None

    # Slots inheritance
    cp = ColoredPoint(5.0, 6.0, "red")
    print(f"\nColoredPoint has __dict__: {hasattr(cp, '__dict__')}")  # False
    print(f"ColoredPoint.color: {cp.color}")

    cpb = ColoredPointBad(5.0, 6.0, "blue")
    print(f"ColoredPointBad has __dict__: {hasattr(cpb, '__dict__')}")  # True

    # Memory comparison
    n = 50_000
    dict_mem = measure_memory_n(PointWithDict, n)
    slots_mem = measure_memory_n(PointWithSlots, n)
    print(f"\n{n} instances: dict={dict_mem:,}B  slots={slots_mem:,}B")
    print(f"Slots saves approx {(1 - slots_mem / max(dict_mem, 1)) * 100:.0f}% memory")
