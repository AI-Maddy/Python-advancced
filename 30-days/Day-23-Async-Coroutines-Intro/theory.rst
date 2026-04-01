Day 23 — Async Coroutines (Intro)
===================================

Core Concepts
-------------

**Coroutine** — a function defined with ``async def``.  Not executed until
awaited.  Returns a coroutine object when called without ``await``.

**Event loop** — a single-threaded loop that multiplexes I/O.  Only one
coroutine runs at a time; others are suspended at ``await`` points.

**await** — suspends the current coroutine and yields control to the event
loop.  Can only be used inside ``async def``.

Running Coroutines
------------------

.. code-block:: python

    asyncio.run(main())          # top-level entry point (Python 3.7+)
    result = await my_coro()    # inside an async function

asyncio.gather vs create_task
------------------------------

.. code-block:: python

    # gather: run multiple coroutines concurrently, wait for all
    results = await asyncio.gather(coro1(), coro2(), coro3())

    # create_task: schedule coroutine as independent task, get a handle
    task = asyncio.create_task(background_work())
    # ... do other things ...
    result = await task

Async Context Manager
----------------------

.. code-block:: python

    class AsyncResource:
        async def __aenter__(self):
            await self._open()
            return self

        async def __aexit__(self, *exc):
            await self._close()
            return False   # don't suppress exceptions

    async with AsyncResource() as r:
        await r.use()

Async Iterator
--------------

.. code-block:: python

    class AsyncStream:
        def __aiter__(self):
            return self

        async def __anext__(self):
            data = await self._fetch_next()
            if data is None:
                raise StopAsyncIteration
            return data

    async for chunk in AsyncStream():
        process(chunk)

asyncio.Queue (Producer-Consumer)
-----------------------------------

.. code-block:: python

    q = asyncio.Queue(maxsize=10)
    await q.put(item)
    item = await q.get()
    q.task_done()
    await q.join()   # wait until all tasks_done

Synchronisation Primitives
----------------------------

.. list-table::
   :header-rows: 1

   * - Primitive
     - Usage
   * - ``asyncio.Lock``
     - Mutual exclusion — one coroutine at a time
   * - ``asyncio.Semaphore(n)``
     - Limit to n concurrent coroutines
   * - ``asyncio.Event``
     - Signal between coroutines (set/wait)
   * - ``asyncio.Condition``
     - Complex producer-consumer coordination

When to Use async vs Threads vs Processes
------------------------------------------

.. list-table::
   :header-rows: 1

   * - Workload
     - Best Choice
   * - I/O-bound, many connections
     - ``asyncio``
   * - I/O-bound, blocking libs
     - ``threading``
   * - CPU-bound
     - ``multiprocessing`` / ``concurrent.futures``

Pitfalls
---------

* Calling a blocking function inside ``async def`` blocks the entire event loop.
  Wrap it with ``asyncio.to_thread()`` (Python 3.9+) or ``loop.run_in_executor()``.
* ``asyncio.run()`` cannot be called from inside a running event loop (e.g. Jupyter).
  Use ``await`` directly instead.
* Don't create tasks without awaiting them — they may not run.
