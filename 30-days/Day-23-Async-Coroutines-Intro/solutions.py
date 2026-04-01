"""
Day 23 — Solutions: Async Coroutines
======================================
"""
from __future__ import annotations

import asyncio
import time
from typing import Any


# ---------------------------------------------------------------------------
# Solution 1 — Async fetch simulation
# ---------------------------------------------------------------------------

async def async_fetch(url: str, delay: float = 0.1) -> dict[str, Any]:
    """Simulate async HTTP fetch."""
    await asyncio.sleep(delay)
    return {"url": url, "status": 200, "body": f"Content of {url}"}


async def fetch_all(urls: list[str]) -> list[dict[str, Any]]:
    """Fetch all URLs concurrently."""
    return list(await asyncio.gather(*[async_fetch(u) for u in urls]))


async def exercise1_fetch() -> tuple[list[dict[str, Any]], float]:
    urls = ["http://a.com", "http://b.com", "http://c.com"]
    delays = [0.3, 0.1, 0.2]

    start = time.perf_counter()
    results = await asyncio.gather(*[
        async_fetch(url, delay) for url, delay in zip(urls, delays)
    ])
    elapsed = time.perf_counter() - start
    return (list(results), elapsed)


# ---------------------------------------------------------------------------
# Solution 2 — asyncio.gather parallel tasks
# ---------------------------------------------------------------------------

async def compute(name: str, n: int) -> int:
    await asyncio.sleep(0.1)
    return n * n


async def exercise2_gather() -> list[int]:
    results = await asyncio.gather(*[compute(f"task{n}", n) for n in range(1, 6)])
    return list(results)


# ---------------------------------------------------------------------------
# Solution 3 — Async queue producer-consumer
# ---------------------------------------------------------------------------

async def producer(queue: asyncio.Queue[str], items: list[str]) -> None:
    for item in items:
        await asyncio.sleep(0.05)
        await queue.put(item)


async def consumer(queue: asyncio.Queue[str], n_items: int) -> list[str]:
    results: list[str] = []
    for _ in range(n_items):
        item = await queue.get()
        results.append(item)
        queue.task_done()
    return results


async def exercise3_queue() -> list[str]:
    items = [f"task_{i}" for i in range(5)]
    q: asyncio.Queue[str] = asyncio.Queue()
    prod = asyncio.create_task(producer(q, items))
    cons = asyncio.create_task(consumer(q, len(items)))
    await prod
    return await cons


# ---------------------------------------------------------------------------
# Solution 4 — Async context manager
# ---------------------------------------------------------------------------

class AsyncTimer:
    """Async context manager that measures elapsed time."""

    def __init__(self) -> None:
        self.elapsed: float = 0.0
        self._start: float = 0.0

    async def __aenter__(self) -> AsyncTimer:
        self._start = time.perf_counter()
        return self

    async def __aexit__(self, *exc_info: Any) -> bool:
        self.elapsed = time.perf_counter() - self._start
        return False


async def exercise4_async_cm() -> float:
    async with AsyncTimer() as timer:
        await asyncio.sleep(0.1)
    return timer.elapsed


# ---------------------------------------------------------------------------
# Solution 5 — asyncio.Lock shared counter
# ---------------------------------------------------------------------------

async def exercise5_lock() -> int:
    counter = [0]
    lock = asyncio.Lock()

    async def increment() -> None:
        for _ in range(100):
            async with lock:
                val = counter[0]
                await asyncio.sleep(0)
                counter[0] = val + 1

    await asyncio.gather(*[increment() for _ in range(10)])
    return counter[0]


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

async def main() -> None:
    results, elapsed = await exercise1_fetch()
    print(f"Exercise 1: {len(results)} fetched in {elapsed:.2f}s (< 0.5s expected)")
    print("Exercise 2:", await exercise2_gather())
    print("Exercise 3:", await exercise3_queue())
    t = await exercise4_async_cm()
    print(f"Exercise 4: elapsed={t:.2f}s")
    print("Exercise 5:", await exercise5_lock())


if __name__ == "__main__":
    asyncio.run(main())
