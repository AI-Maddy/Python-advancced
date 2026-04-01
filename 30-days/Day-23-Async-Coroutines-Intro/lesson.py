"""
Day 23 — Async Coroutines (Intro)
===================================
Topics:
  - async def, await, coroutine objects
  - asyncio.run(), event loop
  - asyncio.gather(), asyncio.create_task()
  - async with (async context manager __aenter__/__aexit__)
  - async for (async iterator __aiter__/__anext__)
  - asyncio.Queue producer-consumer
  - asyncio.Lock, asyncio.Semaphore
  - When to use async vs threads vs multiprocessing
"""
from __future__ import annotations

import asyncio
import random
import time
from collections.abc import AsyncIterator
from typing import Any


# ===========================================================================
# 1. async def, await, coroutine objects
# ===========================================================================

async def greet(name: str, delay: float = 0.1) -> str:
    """Suspend for `delay` seconds, then return greeting."""
    await asyncio.sleep(delay)
    return f"Hello, {name}!"


async def demo_basic_coroutine() -> None:
    """A coroutine is just an awaitable object."""
    # asyncio.run() spins up an event loop, runs the coroutine, closes the loop.
    result = await greet("World", delay=0.05)
    print(result)

    # Coroutine object — not started until awaited
    coro = greet("Python")
    print(f"type(coro): {type(coro)}")   # <class 'coroutine'>
    print(await coro)


# ===========================================================================
# 2. asyncio.gather() — concurrent tasks
# ===========================================================================

async def fetch(resource: str, delay: float) -> str:
    """Simulate a network fetch."""
    await asyncio.sleep(delay)
    return f"Fetched {resource}"


async def demo_gather() -> None:
    """gather() runs coroutines concurrently — total time ≈ max(delays)."""
    start = time.perf_counter()
    results = await asyncio.gather(
        fetch("page_A", 0.2),
        fetch("page_B", 0.15),
        fetch("page_C", 0.3),
    )
    elapsed = time.perf_counter() - start
    for r in results:
        print(f"  {r}")
    print(f"gather total: {elapsed:.2f}s (sequential would be 0.65s)")


# ===========================================================================
# 3. asyncio.create_task() — fire and forget / independent scheduling
# ===========================================================================

async def background_task(name: str, delay: float) -> str:
    """Simulates background processing."""
    await asyncio.sleep(delay)
    print(f"  [task] {name} completed")
    return f"result:{name}"


async def demo_create_task() -> None:
    """Tasks run concurrently without blocking the caller."""
    t1 = asyncio.create_task(background_task("upload", 0.3))
    t2 = asyncio.create_task(background_task("compress", 0.1))

    print("Tasks created, doing other work...")
    await asyncio.sleep(0.05)   # simulate main work
    print("Waiting for tasks to finish...")

    r1 = await t1
    r2 = await t2
    print(f"Results: {r1}, {r2}")


# ===========================================================================
# 4. async with — async context manager
# ===========================================================================

class AsyncDB:
    """
    Simulated async database connection.
    Implements __aenter__ and __aexit__.
    """

    async def __aenter__(self) -> AsyncDB:
        """Open the connection."""
        print("  DB: connecting...")
        await asyncio.sleep(0.05)
        return self

    async def __aexit__(self, *exc_info: Any) -> bool:
        """Close the connection."""
        print("  DB: disconnecting...")
        await asyncio.sleep(0.02)
        return False   # don't suppress exceptions

    async def query(self, sql: str) -> list[dict[str, Any]]:
        """Simulate a database query."""
        await asyncio.sleep(0.05)
        return [{"row": sql}]


async def demo_async_with() -> None:
    """async with ensures __aexit__ is called even on error."""
    async with AsyncDB() as db:
        rows = await db.query("SELECT * FROM users")
        print(f"  Query result: {rows}")


# ===========================================================================
# 5. async for — async iterator
# ===========================================================================

class AsyncRange:
    """
    Async iterator equivalent of range().
    Yields values with a small delay between each.
    """

    def __init__(self, stop: int, delay: float = 0.01) -> None:
        self._stop = stop
        self._delay = delay
        self._current = 0

    def __aiter__(self) -> AsyncRange:
        """Return the iterator itself."""
        return self

    async def __anext__(self) -> int:
        """Return next value or raise StopAsyncIteration."""
        if self._current >= self._stop:
            raise StopAsyncIteration
        await asyncio.sleep(self._delay)
        value = self._current
        self._current += 1
        return value


async def demo_async_for() -> None:
    """Consume an async iterator."""
    total = 0
    async for value in AsyncRange(5, delay=0.02):
        total += value
        print(f"  Received: {value}")
    print(f"  Total: {total}")


# ===========================================================================
# 6. asyncio.Queue — producer-consumer
# ===========================================================================

async def producer(queue: asyncio.Queue[int], n: int) -> None:
    """Produce n items and signal done with sentinel."""
    for i in range(n):
        await asyncio.sleep(0.05)   # simulate work
        await queue.put(i)
        print(f"  produced: {i}")
    await queue.put(-1)             # sentinel


async def consumer(queue: asyncio.Queue[int]) -> list[int]:
    """Consume items until sentinel."""
    results: list[int] = []
    while True:
        item = await queue.get()
        if item == -1:
            break
        print(f"  consumed: {item}")
        results.append(item)
        queue.task_done()
    return results


async def demo_queue() -> None:
    """Run producer and consumer concurrently via a Queue."""
    q: asyncio.Queue[int] = asyncio.Queue(maxsize=3)
    prod = asyncio.create_task(producer(q, 5))
    cons = asyncio.create_task(consumer(q))
    await prod
    results = await cons
    print(f"  Queue demo results: {results}")


# ===========================================================================
# 7. asyncio.Lock and asyncio.Semaphore
# ===========================================================================

async def demo_lock() -> None:
    """Lock ensures only one coroutine accesses a resource at a time."""
    shared_counter = [0]
    lock = asyncio.Lock()

    async def increment(n: int) -> None:
        for _ in range(n):
            async with lock:
                val = shared_counter[0]
                await asyncio.sleep(0)   # yield to event loop
                shared_counter[0] = val + 1

    await asyncio.gather(increment(50), increment(50))
    print(f"  Lock demo counter (expected 100): {shared_counter[0]}")


async def demo_semaphore() -> None:
    """Semaphore limits concurrent access to a resource."""
    sem = asyncio.Semaphore(2)   # at most 2 concurrent
    active: list[int] = []

    async def worker(worker_id: int) -> None:
        async with sem:
            active.append(worker_id)
            assert len(active) <= 2, "Semaphore violated!"
            await asyncio.sleep(0.05)
            active.remove(worker_id)

    await asyncio.gather(*[worker(i) for i in range(8)])
    print("  Semaphore demo: all 8 workers completed without exceeding limit of 2")


# ===========================================================================
# 8. When to use async vs threads vs multiprocessing
# ===========================================================================
# async / coroutines: I/O-bound tasks (network, disk), high concurrency with
#   low overhead, single thread — no GIL concern.
#
# threading: I/O-bound tasks when libraries aren't async-aware, or when you
#   need to call blocking C extensions. GIL prevents true parallel CPU work.
#
# multiprocessing: CPU-bound tasks (computation, image processing, ML).
#   Each process has its own GIL — true parallelism.
#
# Rule of thumb:
#   I/O-bound + async library available → asyncio
#   I/O-bound + blocking library        → threading
#   CPU-bound                           → multiprocessing or concurrent.futures


# ===========================================================================
# Main demo
# ===========================================================================

async def main() -> None:
    print("=" * 60)
    print("Day 23 — Async Coroutines (Intro)")
    print("=" * 60)

    print("\n--- Basic coroutine ---")
    await demo_basic_coroutine()

    print("\n--- asyncio.gather ---")
    await demo_gather()

    print("\n--- asyncio.create_task ---")
    await demo_create_task()

    print("\n--- async with (async context manager) ---")
    await demo_async_with()

    print("\n--- async for (async iterator) ---")
    await demo_async_for()

    print("\n--- asyncio.Queue producer-consumer ---")
    await demo_queue()

    print("\n--- asyncio.Lock ---")
    await demo_lock()

    print("\n--- asyncio.Semaphore ---")
    await demo_semaphore()


if __name__ == "__main__":
    asyncio.run(main())
