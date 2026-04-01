"""
Example 2 — tracemalloc comparison of slots vs dict memory usage.
"""
from __future__ import annotations

import tracemalloc

from slots_idiom import PointWithDict, PointWithSlots


def peak_memory(cls: type, n: int = 10_000) -> int:
    tracemalloc.start()
    objects = [cls(float(i), float(i)) for i in range(n)]  # type: ignore[call-arg]
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del objects
    return peak


def main() -> None:
    n = 10_000
    dict_peak = peak_memory(PointWithDict, n)
    slots_peak = peak_memory(PointWithSlots, n)

    print(f"Peak memory for {n:,} instances:")
    print(f"  PointWithDict : {dict_peak:>10,} bytes")
    print(f"  PointWithSlots: {slots_peak:>10,} bytes")
    if dict_peak > 0:
        saving_pct = (dict_peak - slots_peak) / dict_peak * 100
        print(f"  Savings       : {saving_pct:.1f}%")


if __name__ == "__main__":
    main()
