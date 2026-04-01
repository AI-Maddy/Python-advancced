"""
Example 2 — Running statistics coroutine using send().
"""
from __future__ import annotations

from typing import Generator


def statistics_collector() -> Generator[dict, float, None]:
    """Coroutine that accumulates statistics.

    Send float values; each send() returns a dict of {count, mean, min, max}.
    """
    count = 0
    total = 0.0
    minimum: float | None = None
    maximum: float | None = None

    while True:
        value = yield {
            "count": count,
            "mean": total / count if count else 0.0,
            "min": minimum,
            "max": maximum,
        }
        if value is None:
            break
        count += 1
        total += value
        minimum = value if minimum is None else min(minimum, value)
        maximum = value if maximum is None else max(maximum, value)


def main() -> None:
    data = [4.0, 7.0, 1.0, 9.0, 2.0, 6.0, 3.0, 8.0, 5.0]

    stats = statistics_collector()
    next(stats)  # prime

    for val in data:
        result = stats.send(val)

    print("Final statistics:")
    for k, v in result.items():
        print(f"  {k}: {v}")

    stats.close()


if __name__ == "__main__":
    main()
