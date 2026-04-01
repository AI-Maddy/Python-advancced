Day 22 — Performance & Profiling in OOP
=========================================

Micro-Benchmarking with timeit
--------------------------------

.. code-block:: python

    import timeit

    t = timeit.timeit("x = [i for i in range(1000)]", number=10_000)
    # or with a callable:
    t = timeit.timeit(lambda: my_function(), number=1_000)

* ``number`` — how many times to call the function.
* Returns total elapsed time in seconds.
* Use ``timeit.repeat(number=N, repeat=R)`` for statistical stability.

cProfile + pstats
------------------

.. code-block:: python

    import cProfile, pstats, io

    pr = cProfile.Profile()
    pr.enable()
    slow_function()
    pr.disable()

    buf = io.StringIO()
    ps = pstats.Stats(pr, stream=buf)
    ps.sort_stats("cumulative")   # tottime, cumtime, calls, etc.
    ps.print_stats(10)            # top 10 lines

Key columns: ``ncalls``, ``tottime`` (excluding callees), ``cumtime``
(including callees), ``percall``.

Command-line: ``python -m cProfile -s cumulative my_script.py``

``__slots__``
-------------

* Replaces per-instance ``__dict__`` with fixed descriptor slots.
* Reduces memory by ~40-60 bytes per instance (varies by platform).
* Prevents adding arbitrary attributes at runtime.
* Cannot pickle unless ``__getstate__``/``__setstate__`` are defined, or
  ``__dict__`` is in ``__slots__``.

.. code-block:: python

    class Point:
        __slots__ = ("x", "y")   # no __dict__ created

tracemalloc
-----------

.. code-block:: python

    import tracemalloc
    tracemalloc.start()
    do_work()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Peak: {peak / 1024:.1f} KB")

lru_cache Performance
----------------------

Memoization trades memory for time.  For pure recursive functions like
Fibonacci, lru_cache turns O(2^n) into O(n).

Common Pitfalls
---------------

.. list-table::
   :header-rows: 1

   * - Pitfall
     - Fix
   * - Repeated attribute lookup in loop
     - Cache as local variable before loop
   * - ``list = list + [item]`` in loop
     - Use ``list.append(item)`` or list comprehension
   * - Calling bound method via dotted path each iteration
     - Cache bound method: ``f = obj.method``
   * - Large list for membership test
     - Use ``set`` or ``dict`` (O(1) lookup)
   * - ``__dict__`` on millions of instances
     - Use ``__slots__``

When to Profile
---------------

1. Identify the bottleneck first (``cProfile``).
2. Micro-benchmark only the hot path (``timeit``).
3. Check memory only if RSS is growing unexpectedly (``tracemalloc``).
4. Don't optimise what you haven't measured.
