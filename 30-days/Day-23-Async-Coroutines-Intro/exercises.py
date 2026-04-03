"""
Day 23 — Exercises: Async Coroutines
=======================================
Complete each TODO.  Run with: python exercises.py
"""
from __future__ import annotations

import asyncio
import time
from typing import Any


# ---------------------------------------------------------------------------
# Exercise 1 — Async fetch simulation
# ---------------------------------------------------------------------------
# TODO: Implement async_fetch(url: str, delay: float) -> dict that:
#   - sleeps for `delay` seconds (simulating network latency)
#   - returns {"url": url, "status": 200, "body": f"Content of {url}"}
# Then write fetch_all(urls: list[str]) using asyncio.gather to fetch all
# concurrently.  Verify total time is approx max(delays) not sum(delays).

async def async_fetch(url: str, delay: float = 0.1) -> dict[str, Any]:
    """Simulate async HTTP fetch."""
    await asyncio.sleep(delay)
    return {"url": url, "status": 200, "body": f"Content of {url}"}


async def fetch_all(urls: list[str]) -> list[dict[str, Any]]:
    """Fetch all URLs concurrently using asyncio.gather."""
    return list(await asyncio.gather(*[async_fetch(u) for u in urls]))


async def exercise1_fetch() -> tuple[list[dict[str, Any]], float]:
    """
    Return (results, elapsed_seconds).
    elapsed_seconds should be < 0.5 (not 0.9 = sequential sum).
    """
    urls = ["http://a.com", "http://b.com", "http://c.com"]
    delays = [0.3, 0.1, 0.2]
    start = time.perf_counter()
    results = await asyncio.gather(*[
        async_fetch(url, delay) for url, delay in zip(urls, delays)
    ])
    elapsed = time.perf_counter() - start
    return (list(results), elapsed)


# ---------------------------------------------------------------------------
# Exercise 2 — asyncio.gather parallel tasks
# ---------------------------------------------------------------------------
# TODO: Create a compute(name, n) coroutine that:
#   - Sleeps 0.1 seconds
#   - Returns n * n
# Run 5 such tasks concurrently with gather and return all results.

async def compute(name: str, n: int) -> int:
    """Simulate async computation."""
    await asyncio.sleep(0.1)
    return n * n


async def exercise2_gather() -> list[int]:
    """Run compute for n in [1,2,3,4,5] concurrently; return squared results."""
    results = await asyncio.gather(*[compute(f"task{n}", n) for n in range(1, 6)])
    return list(results)


# ---------------------------------------------------------------------------
# Exercise 3 — Async queue producer-consumer
# ---------------------------------------------------------------------------
# TODO: Implement:
#   producer(queue, items): puts each item in queue with 0.05s delay
#   consumer(queue, n_items): collects n_items from queue, returns list
# Run both concurrently; verify all items consumed in correct order.

async def producer(queue: asyncio.Queue[str], items: list[str]) -> None:
    """Produce items into queue."""
    for item in items:
        await asyncio.sleep(0.05)
        await queue.put(item)


async def consumer(queue: asyncio.Queue[str], n_items: int) -> list[str]:
    """Consume n_items from queue and return them."""
    results: list[str] = []
    for _ in range(n_items):
        item = await queue.get()
        results.append(item)
        queue.task_done()
    return results


async def exercise3_queue() -> list[str]:
    """Return consumed items. Expected: ['task_0', 'task_1', ..., 'task_4']."""
    items = [f"task_{i}" for i in range(5)]
    q: asyncio.Queue[str] = asyncio.Queue()
    prod = asyncio.create_task(producer(q, items))
    cons = asyncio.create_task(consumer(q, len(items)))
    await prod
    return await cons


# ---------------------------------------------------------------------------
# Exercise 4 — Async context manager
# ---------------------------------------------------------------------------
# TODO: Implement AsyncTimer context manager that:
#   - Records start time in __aenter__
#   - Records elapsed time in __aexit__ and stores it as self.elapsed
#   - Demonstrates: async with AsyncTimer() as t: await asyncio.sleep(0.1)
#                   print(t.elapsed)  # ~0.1

class AsyncTimer:
    """Async context manager that measures elapsed time."""

    def __init__(self) -> None:
        self.elapsed: float = 0.0
        self._start: float = 0.0

    async def __aenter__(self) -> AsyncTimer:
        """Record start time."""
        self._start = time.perf_counter()
        return self

    async def __aexit__(self, *exc_info: Any) -> bool:
        """Calculate elapsed time."""
        self.elapsed = time.perf_counter() - self._start
        return False


async def exercise4_async_cm() -> float:
    """Return elapsed time for a 0.1s sleep. Should be ~0.1."""
    async with AsyncTimer() as timer:
        await asyncio.sleep(0.1)
    return timer.elapsed


# ---------------------------------------------------------------------------
# Exercise 5 — asyncio.Lock shared counter
# ---------------------------------------------------------------------------
# TODO: Use asyncio.Lock to safely increment a shared counter from
#       10 concurrent coroutines each incrementing 100 times.
#       Without a lock the counter would be less than 1000.
#       Return final counter value (expected: 1000).

async def exercise5_lock() -> int:
    """Return final counter value (expected: 1000)."""
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
    print("Exercise 1:", await exercise1_fetch())
    print("Exercise 2:", await exercise2_gather())
    print("Exercise 3:", await exercise3_queue())
    print("Exercise 4:", await exercise4_async_cm())
    print("Exercise 5:", await exercise5_lock())


if __name__ == "__main__":
    asyncio.run(main())
