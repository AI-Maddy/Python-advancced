# :material-lightning-bolt: Day 23 — Async & Coroutines

!!! abstract "Day at a Glance"
    **Goal:** Master Python's cooperative-concurrency model — write, compose, and reason about `async`/`await` coroutines using `asyncio`.
    **C++ Equivalent:** Day 23 of Learn-Modern-CPP-OOP-30-Days (`std::future`, `std::async`, C++20 `co_await`)
    **Estimated Time:** 60–90 minutes

<div class="grid cards" markdown>
- :material-lightbulb-on: **Core Concept** — A coroutine is a function that can pause itself and yield control back to the event loop without blocking the OS thread.
- :material-snake: **Python Way** — `async def` + `await`; compose with `asyncio.gather()` and `create_task()`; share state safely with `asyncio.Lock` and `asyncio.Queue`.
- :material-alert: **Watch Out** — Calling a blocking function (e.g., `time.sleep`, file I/O via `open()`) inside a coroutine stalls the entire event loop.
- :material-check-circle: **By End of Day** — You can build an async producer-consumer pipeline and write async context managers / iterators.
</div>

---

## :material-lightbulb-on: Intuition

!!! info "Core Idea"
    Python's Global Interpreter Lock (GIL) means only one thread runs Python bytecode at a time.  For **I/O-bound** work (network, disk), threads spend most of their time waiting — the GIL is released during that wait.  Async takes this further: instead of OS threads (which have a ~1 MB stack each), you write coroutines that explicitly `await` at every blocking point.  The single-threaded **event loop** schedules hundreds of thousands of coroutines with negligible overhead.

!!! success "Python vs C++"
    | Concept | C++ | Python |
    |---|---|---|
    | Suspendable function | `co_await` (C++20) | `async def` + `await` |
    | Run one coroutine | `std::future::get()` | `asyncio.run(coro())` |
    | Run many concurrently | `std::async` × N + wait | `asyncio.gather(*coros)` |
    | Async mutex | `std::mutex` (blocks thread) | `asyncio.Lock` (yields to loop) |
    | Async queue | `std::queue` + condition variable | `asyncio.Queue` |
    | CPU-bound parallel | `std::thread` / OpenMP | `concurrent.futures.ProcessPoolExecutor` |

---

## :material-transit-connection-variant: Event Loop Scheduling Two Coroutines

```mermaid
sequenceDiagram
    participant Loop as Event Loop
    participant A as coroutine_a
    participant B as coroutine_b

    Loop->>A: resume
    A->>Loop: await asyncio.sleep(1)
    Loop->>B: resume
    B->>Loop: await asyncio.sleep(0.5)
    Note over Loop: 0.5 s passes
    Loop->>B: resume (sleep done)
    B->>Loop: return "B done"
    Note over Loop: 0.5 s more passes
    Loop->>A: resume (sleep done)
    A->>Loop: return "A done"
```

Both coroutines overlap in time even though they run on a single OS thread.

---

## :material-book-open-variant: Lesson

### 1. `async def` and `await` Basics

```python
import asyncio

async def greet(name: str, delay: float) -> str:
    print(f"[{name}] starting …")
    await asyncio.sleep(delay)          # yields control to the event loop
    print(f"[{name}] done after {delay}s")
    return f"Hello, {name}!"

async def main():
    # Run sequentially (total ~3 s)
    r1 = await greet("Alice", 1)
    r2 = await greet("Bob",   2)
    print(r1, r2)

asyncio.run(main())
```

`asyncio.run()` creates a new event loop, runs the coroutine to completion, then closes the loop.

---

### 2. `asyncio.gather()` — Concurrent Execution

```python
import asyncio
import time

async def fetch(url: str, latency: float) -> str:
    await asyncio.sleep(latency)    # simulate network I/O
    return f"<html from {url}>"

async def main():
    start = time.perf_counter()
    results = await asyncio.gather(
        fetch("https://example.com",  1.0),
        fetch("https://python.org",   1.5),
        fetch("https://asyncio.dev",  0.8),
    )
    elapsed = time.perf_counter() - start
    print(f"Fetched {len(results)} pages in {elapsed:.2f}s")  # ~1.5 s, not 3.3 s
    for r in results:
        print(r)

asyncio.run(main())
```

`gather` returns results **in the same order** as the arguments, regardless of completion order.

---

### 3. `create_task()` — Fire and Forget

```python
import asyncio

async def background_job(n: int) -> None:
    await asyncio.sleep(0.1 * n)
    print(f"job {n} finished")

async def main():
    # Schedule tasks without immediately awaiting them
    tasks = [asyncio.create_task(background_job(i)) for i in range(5)]
    print("All tasks scheduled, doing other work …")
    await asyncio.sleep(0)          # yield once so tasks can start
    await asyncio.gather(*tasks)    # now wait for all

asyncio.run(main())
```

---

### 4. `async with` — Async Context Managers

Implement `__aenter__` and `__aexit__` (both must be coroutines):

```python
import asyncio

class AsyncDBConnection:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self._conn = None

    async def __aenter__(self) -> "AsyncDBConnection":
        print(f"Connecting to {self.dsn} …")
        await asyncio.sleep(0.05)           # simulate async connect
        self._conn = object()               # placeholder
        print("Connected.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        print("Closing connection.")
        await asyncio.sleep(0.01)           # simulate async teardown
        self._conn = None
        return False                        # do not suppress exceptions

    async def query(self, sql: str) -> list:
        await asyncio.sleep(0.02)
        return [{"id": 1, "sql": sql}]

async def main():
    async with AsyncDBConnection("postgresql://localhost/mydb") as db:
        rows = await db.query("SELECT * FROM users")
        print(rows)

asyncio.run(main())
```

---

### 5. `async for` — Async Iterators

Implement `__aiter__` (returns `self`) and `__anext__` (coroutine):

```python
import asyncio

class AsyncCounter:
    def __init__(self, stop: int) -> None:
        self._stop = stop
        self._current = 0

    def __aiter__(self) -> "AsyncCounter":
        return self

    async def __anext__(self) -> int:
        if self._current >= self._stop:
            raise StopAsyncIteration
        await asyncio.sleep(0.01)       # simulate async data source
        value = self._current
        self._current += 1
        return value

async def main():
    async for number in AsyncCounter(5):
        print(number)

asyncio.run(main())
```

---

### 6. `asyncio.Queue` — Async Producer-Consumer

```python
import asyncio
import random

async def producer(queue: asyncio.Queue, n: int) -> None:
    for i in range(n):
        item = random.randint(1, 100)
        await queue.put(item)
        print(f"Produced {item}")
        await asyncio.sleep(0.05)
    await queue.put(None)           # sentinel

async def consumer(queue: asyncio.Queue) -> None:
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"  Consumed {item}")
        await asyncio.sleep(0.1)    # slower consumer
        queue.task_done()

async def main():
    q: asyncio.Queue = asyncio.Queue(maxsize=5)
    await asyncio.gather(
        producer(q, 10),
        consumer(q),
    )

asyncio.run(main())
```

---

### 7. `asyncio.Lock` — Mutual Exclusion

```python
import asyncio

class AsyncCounter:
    def __init__(self) -> None:
        self._value = 0
        self._lock  = asyncio.Lock()

    async def increment(self) -> None:
        async with self._lock:
            current = self._value
            await asyncio.sleep(0)  # yield — without lock, another task could race
            self._value = current + 1

async def main():
    counter = AsyncCounter()
    await asyncio.gather(*[counter.increment() for _ in range(1000)])
    print(f"Final value: {counter._value}")  # always 1000

asyncio.run(main())
```

---

### 8. Async vs Threads vs Multiprocessing

| | `asyncio` | `threading` | `multiprocessing` |
|---|---|---|---|
| **Best for** | I/O-bound (network, DB) | I/O-bound, legacy blocking code | CPU-bound computation |
| **Parallelism** | Cooperative (1 thread) | Concurrent (GIL limits CPU) | True parallel (separate processes) |
| **Overhead** | Very low | Medium (~1 MB / thread) | High (~50 ms startup) |
| **Shared state** | Simple (single thread) | Needs locks | Needs multiprocessing primitives |
| **C++ analogy** | `co_await` event loop | `std::thread` | `fork()` / `std::process` |

---

## :material-alert: Common Pitfalls

!!! warning "Blocking Calls Block the Whole Loop"
    ```python
    # BAD — freezes the event loop for everyone
    async def download():
        import time
        time.sleep(5)               # blocks the OS thread

    # GOOD — run blocking work in a thread pool
    async def download():
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, time.sleep, 5)
    ```

!!! warning "Forgetting to `await` a Coroutine"
    ```python
    async def main():
        result = greet("Alice", 1)  # BUG: coroutine object, never executed!
        result = await greet("Alice", 1)  # correct
    ```
    Python 3.11+ emits a `RuntimeWarning: coroutine 'greet' was never awaited`.

!!! danger "Using `asyncio.run()` Inside a Running Event Loop"
    Inside Jupyter notebooks or FastAPI, a loop is already running.  Use `await coro()` directly, or use `asyncio.create_task()`.  Calling `asyncio.run()` inside a running loop raises `RuntimeError`.

!!! danger "Sharing `asyncio` Primitives Across Threads"
    `asyncio.Lock`, `asyncio.Queue`, etc. are **not** thread-safe.  If you mix `threading` and `asyncio`, use `asyncio.run_coroutine_threadsafe()` to schedule coroutines from other threads.

---

## :material-help-circle: Flashcards

???+ question "What is a coroutine object?"
    When you call an `async def` function **without** `await`, Python returns a **coroutine object** — a suspended generator-like object that has not started running yet.  The event loop (via `await` or `asyncio.run`) resumes it step by step.

???+ question "What is the difference between `gather` and `create_task`?"
    `asyncio.gather(*coros)` wraps each coroutine in a task and waits for **all** of them, returning results as a list.  `create_task(coro)` schedules a single coroutine to run **concurrently** and returns a `Task` you can await later — giving you more control over individual tasks (cancel, add callbacks).

???+ question "How do `__aenter__` and `__aexit__` differ from `__enter__` and `__exit__`?"
    `__aenter__` and `__aexit__` are **coroutines** (declared with `async def`) so they can `await` inside.  They are used with `async with`.  The synchronous counterparts (`__enter__`/`__exit__`) cannot suspend.

???+ question "When should you use `asyncio` instead of `multiprocessing`?"
    Use `asyncio` for **I/O-bound** tasks where most time is spent waiting for network or disk.  Use `multiprocessing` for **CPU-bound** tasks (number crunching, image processing) where you need true parallelism across CPU cores.

---

## :material-clipboard-check: Self Test

=== "Question 1"
    You have a synchronous function `def read_file(path)` that takes 2 seconds.  How do you call it from a coroutine without blocking the event loop?

=== "Answer 1"
    ```python
    import asyncio

    async def load(path: str) -> str:
        loop = asyncio.get_running_loop()
        content = await loop.run_in_executor(None, read_file, path)
        return content
    ```
    `run_in_executor(None, fn, *args)` runs the blocking function in the default `ThreadPoolExecutor`, freeing the event loop to handle other coroutines.

=== "Question 2"
    Write an async context manager `Timer` that prints elapsed time on exit.

=== "Answer 2"
    ```python
    import asyncio, time

    class Timer:
        async def __aenter__(self) -> "Timer":
            self._start = time.perf_counter()
            return self

        async def __aexit__(self, *args) -> bool:
            elapsed = time.perf_counter() - self._start
            print(f"Elapsed: {elapsed:.3f}s")
            return False

    async def main():
        async with Timer():
            await asyncio.sleep(0.5)

    asyncio.run(main())   # prints: Elapsed: 0.500s
    ```

---

## :material-check-circle: Summary

!!! success "Key Takeaways"
    - **`async def` / `await`** define and consume coroutines; the event loop drives them cooperatively on a single thread.
    - **`asyncio.gather()`** runs multiple coroutines concurrently and collects results in order.
    - **`create_task()`** schedules a coroutine without waiting immediately, enabling fire-and-forget patterns.
    - **`async with`** / **`async for`** require `__aenter__`/`__aexit__` and `__aiter__`/`__anext__` as coroutines.
    - **`asyncio.Queue`** and **`asyncio.Lock`** provide concurrency-safe producer-consumer and mutual-exclusion patterns.
    - Never call **blocking I/O** directly inside a coroutine — use `run_in_executor` to offload to a thread pool.
    - Choose `asyncio` for I/O-bound work, `multiprocessing` for CPU-bound work.
