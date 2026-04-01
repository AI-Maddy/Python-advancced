Day 21 — functools, operator & itertools
==========================================

functools
----------

.. list-table::
   :header-rows: 1

   * - Function
     - Purpose
   * - ``reduce(f, iterable[, init])``
     - Fold left with binary function
   * - ``partial(f, *args, **kw)``
     - Pre-fill arguments; return new callable
   * - ``lru_cache(maxsize=128)``
     - Memoize with bounded LRU cache
   * - ``cache``
     - Unbounded memoization (Python 3.9+)
   * - ``cached_property``
     - Compute once, cache on instance; no lock by default
   * - ``total_ordering``
     - Fill in comparison methods from ``__eq__`` + one of ``__lt__``, ``__gt__``
   * - ``singledispatch``
     - Type-based function dispatch on first argument

operator module
----------------

Provides function versions of Python operators — faster than lambdas and
more composable.

.. code-block:: python

    import operator

    operator.attrgetter("salary")      # like: lambda obj: obj.salary
    operator.itemgetter("name")        # like: lambda d: d["name"]
    operator.methodcaller("upper")     # like: lambda s: s.upper()
    operator.add(a, b)                 # a + b
    operator.mul(a, b)                 # a * b

itertools
----------

.. list-table::
   :header-rows: 1

   * - Function
     - Description
   * - ``chain(*iterables)``
     - Concatenate iterables lazily
   * - ``islice(it, stop)``
     - Lazy slice of any iterator
   * - ``count(start, step)``
     - Infinite counter
   * - ``cycle(iterable)``
     - Repeat iterable infinitely
   * - ``groupby(it, key)``
     - Group *consecutive* equal-key items (sort first!)
   * - ``product(*its)``
     - Cartesian product
   * - ``combinations(it, r)``
     - r-length combinations without replacement
   * - ``accumulate(it, f)``
     - Running aggregation (default: add)
   * - ``takewhile(pred, it)``
     - Take items while predicate is True
   * - ``dropwhile(pred, it)``
     - Skip items while predicate is True, then yield rest

Functional Pipeline with reduce
---------------------------------

.. code-block:: python

    from functools import reduce

    def compose(*funcs):
        return reduce(lambda f, g: lambda x: f(g(x)), funcs)

    pipeline = compose(str.upper, str.strip, lambda s: s.replace(",", ""))
    pipeline("  hello, world  ")   # "HELLO WORLD"

Best Practices
--------------

* Use ``lru_cache`` / ``cache`` for pure functions with repeated calls (memoization).
* Prefer ``operator.attrgetter`` / ``itemgetter`` over lambdas in ``sorted`` / ``max``.
* Always sort data by the groupby key before calling ``itertools.groupby``.
* ``cached_property`` is not thread-safe by default — add a lock if needed.
* ``singledispatch`` is more readable than ``isinstance`` chains for type dispatch.
