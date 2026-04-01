Day 13 — Decorators In Depth
==============================

Decorator Anatomy
------------------
.. code-block:: python

    import functools

    def my_decorator(func):
        @functools.wraps(func)   # preserves __name__, __doc__
        def wrapper(*args, **kwargs):
            # before
            result = func(*args, **kwargs)
            # after
            return result
        return wrapper

Parameterised Decorator (Factory)
-----------------------------------
.. code-block:: python

    def retry(max_attempts=3):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for i in range(max_attempts):
                    try: return func(*args, **kwargs)
                    except Exception: pass
                raise RuntimeError("max retries exceeded")
            return wrapper
        return decorator

    @retry(max_attempts=5)
    def flaky_operation(): ...

Stacking Decorators
--------------------
.. code-block:: python

    @timer          # applied second (outermost)
    @memoize        # applied first (innermost)
    def compute(n): ...
    # equivalent to: compute = timer(memoize(compute))

functools.lru_cache
--------------------
.. code-block:: python

    @functools.lru_cache(maxsize=128)
    def fib(n):
        if n <= 1: return n
        return fib(n-1) + fib(n-2)

    fib.cache_info()   # CacheInfo(hits=..., misses=..., maxsize=128, currsize=...)
    fib.cache_clear()  # clear the cache
