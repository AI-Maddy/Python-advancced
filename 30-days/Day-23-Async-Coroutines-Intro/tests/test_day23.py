"""
Tests for Day 23 — Async Coroutines
Run with: pytest tests/test_day23.py -v
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import asyncio
import time
from typing import Any

import pytest


# ---------------------------------------------------------------------------
# Helper: async fetch
# ---------------------------------------------------------------------------

async def async_fetch(url: str, delay: float = 0.0) -> dict[str, Any]:
    await asyncio.sleep(delay)
    return {"url": url, "status": 200}


# ---------------------------------------------------------------------------
# Basic coroutine tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_basic_coroutine_returns_value() -> None:
    result = await async_fetch("http://example.com")
    assert result["status"] == 200
    assert result["url"] == "http://example.com"


@pytest.mark.asyncio
async def test_coroutine_object_not_started() -> None:
    """A coroutine is not executed until awaited."""
    executed = [False]

    async def track() -> None:
        executed[0] = True

    coro = track()               # not started yet
    assert not executed[0]
    await coro                   # now it runs
    assert executed[0]


# ---------------------------------------------------------------------------
# asyncio.gather tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gather_returns_all_results() -> None:
    results = await asyncio.gather(
        async_fetch("a"),
        async_fetch("b"),
        async_fetch("c"),
    )
    urls = [r["url"] for r in results]
    assert urls == ["a", "b", "c"]


@pytest.mark.asyncio
async def test_gather_is_concurrent() -> None:
    """Total time for gather should be close to max delay, not sum."""
    start = time.perf_counter()
    await asyncio.gather(
        asyncio.sleep(0.1),
        asyncio.sleep(0.1),
        asyncio.sleep(0.1),
    )
    elapsed = time.perf_counter() - start
    # Sequential would take ~0.3s; concurrent should be ~0.1s
    assert elapsed < 0.25


@pytest.mark.asyncio
async def test_gather_preserves_order() -> None:
    """gather() preserves the order of results matching input order."""
    results = await asyncio.gather(
        async_fetch("first", 0.1),
        async_fetch("second", 0.05),  # finishes sooner but listed second
        async_fetch("third", 0.0),
    )
    assert [r["url"] for r in results] == ["first", "second", "third"]


# ---------------------------------------------------------------------------
# create_task tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_task_completes() -> None:
    executed = [False]

    async def work() -> str:
        executed[0] = True
        return "done"

    task = asyncio.create_task(work())
    result = await task
    assert result == "done"
    assert executed[0]


@pytest.mark.asyncio
async def test_multiple_tasks_concurrent() -> None:
    log: list[str] = []

    async def step(name: str, delay: float) -> None:
        await asyncio.sleep(delay)
        log.append(name)

    t1 = asyncio.create_task(step("slow", 0.1))
    t2 = asyncio.create_task(step("fast", 0.01))
    await asyncio.gather(t1, t2)
    # fast finishes before slow
    assert log == ["fast", "slow"]


# ---------------------------------------------------------------------------
# Async context manager tests
# ---------------------------------------------------------------------------

class AsyncCounter:
    """Counts open/close operations via __aenter__/__aexit__."""
    def __init__(self) -> None:
        self.entered = False
        self.exited = False

    async def __aenter__(self) -> AsyncCounter:
        self.entered = True
        return self

    async def __aexit__(self, *exc: Any) -> bool:
        self.exited = True
        return False


@pytest.mark.asyncio
async def test_async_context_manager_enter_exit() -> None:
    ctx = AsyncCounter()
    async with ctx:
        assert ctx.entered
        assert not ctx.exited
    assert ctx.exited


@pytest.mark.asyncio
async def test_async_context_manager_cleanup_on_exception() -> None:
    ctx = AsyncCounter()
    with pytest.raises(ValueError):
        async with ctx:
            raise ValueError("test error")
    assert ctx.exited   # __aexit__ called even on exception


# ---------------------------------------------------------------------------
# Async iterator tests
# ---------------------------------------------------------------------------

class AsyncCounter2:
    """Yields integers 0..n-1 asynchronously."""
    def __init__(self, n: int) -> None:
        self._n = n
        self._i = 0

    def __aiter__(self) -> AsyncCounter2:
        return self

    async def __anext__(self) -> int:
        if self._i >= self._n:
            raise StopAsyncIteration
        await asyncio.sleep(0)
        val = self._i
        self._i += 1
        return val


@pytest.mark.asyncio
async def test_async_for_collects_values() -> None:
    values = []
    async for v in AsyncCounter2(5):
        values.append(v)
    assert values == [0, 1, 2, 3, 4]


# ---------------------------------------------------------------------------
# asyncio.Queue tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_queue_producer_consumer() -> None:
    q: asyncio.Queue[int] = asyncio.Queue()
    produced: list[int] = []
    consumed: list[int] = []

    async def prod() -> None:
        for i in range(5):
            await q.put(i)
            produced.append(i)

    async def cons() -> None:
        for _ in range(5):
            item = await q.get()
            consumed.append(item)

    await asyncio.gather(prod(), cons())
    assert produced == [0, 1, 2, 3, 4]
    assert consumed == [0, 1, 2, 3, 4]


# ---------------------------------------------------------------------------
# asyncio.Lock tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_lock_prevents_race() -> None:
    counter = [0]
    lock = asyncio.Lock()

    async def increment() -> None:
        for _ in range(50):
            async with lock:
                val = counter[0]
                await asyncio.sleep(0)
                counter[0] = val + 1

    await asyncio.gather(*[increment() for _ in range(4)])
    assert counter[0] == 200   # 4 tasks * 50 increments


# ---------------------------------------------------------------------------
# asyncio.Semaphore tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_semaphore_limits_concurrency() -> None:
    MAX = 2
    sem = asyncio.Semaphore(MAX)
    active = [0]
    max_active = [0]

    async def work() -> None:
        async with sem:
            active[0] += 1
            max_active[0] = max(max_active[0], active[0])
            await asyncio.sleep(0.02)
            active[0] -= 1

    await asyncio.gather(*[work() for _ in range(6)])
    assert max_active[0] <= MAX
