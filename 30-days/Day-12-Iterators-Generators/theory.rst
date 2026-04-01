Day 12 — Iterators and Generators
===================================

Iterator Protocol
------------------
.. code-block:: python

    class Counter:
        def __iter__(self) -> "Counter": return self
        def __next__(self) -> int:
            if done: raise StopIteration
            return next_value

Generators (yield)
-------------------
.. code-block:: python

    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

yield from
-----------
.. code-block:: python

    def flatten(lst):
        for item in lst:
            if isinstance(item, list):
                yield from flatten(item)
            else:
                yield item

Lazy Pipelines
--------------
.. code-block:: python

    # All lazy — no intermediate lists:
    nums = itertools.count(0)
    evens = filter(lambda x: x % 2 == 0, nums)
    result = itertools.islice(evens, 5)
    list(result)  # [0, 2, 4, 6, 8]
