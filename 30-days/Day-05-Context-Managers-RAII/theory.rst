Day 05 — Context Managers and RAII
=====================================

Why This Day Matters
--------------------

Python's garbage collector is non-deterministic — you cannot rely on
``__del__`` running at a predictable time.  The ``with`` statement is
Python's answer to C++ RAII: it guarantees that cleanup code runs
when a block exits, regardless of exceptions or early returns.


Python's RAII Equivalent
--------------------------

.. code-block:: text

    C++ RAII:                           Python with statement:
    {                                   with resource_manager() as r:
        ScopedResource r{...};              use(r)
        use(r);                         # __exit__ always called here
    }  // ~ScopedResource() called

The ``with`` guarantee: ``__exit__`` is **always** called, even if an
exception is raised inside the block.


The Context Manager Protocol
------------------------------

Two methods define a context manager:

.. code-block:: python

    class MyContext:
        def __enter__(self):
            # setup; return value becomes 'as' variable
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            # cleanup always runs here
            if exc_type is not None:
                # an exception occurred
                pass
            return False  # False/None: propagate; True: suppress

- ``exc_type``, ``exc_val``, ``exc_tb``: exception info (all ``None`` if no exception)
- Return ``True`` to suppress the exception; return ``False``/``None`` to propagate


@contextmanager — Generator Form
----------------------------------

.. code-block:: python

    from contextlib import contextmanager

    @contextmanager
    def managed_resource():
        # setup (= __enter__)
        resource = acquire()
        try:
            yield resource     # value becomes 'as' variable
        finally:
            # teardown (= __exit__) — always runs
            release(resource)

The generator form is simpler for most cases.  The class form is needed
when you want the context manager itself to be reusable or to store state
between enter and exit.


contextlib Utilities
---------------------

.. code-block:: python

    from contextlib import suppress, nullcontext, ExitStack

    # suppress: ignore specific exceptions
    with suppress(FileNotFoundError):
        open("/nonexistent")

    # nullcontext: no-op (for conditional context managers)
    lock = threading.Lock() if threaded else None
    with (lock or nullcontext()):
        do_work()

    # ExitStack: manage a dynamic number of context managers
    with ExitStack() as stack:
        files = [stack.enter_context(open(f)) for f in filenames]
        # all files closed on exit, even if one raises


When to Suppress Exceptions
-----------------------------

Returning ``True`` from ``__exit__`` suppresses the exception — the ``with``
block continues as if nothing happened.  Use this sparingly:

- ``contextlib.suppress``: for intentionally ignoring expected errors
- Custom transaction managers: to rollback and re-raise (usually don't suppress)
- Never use it to hide unexpected errors


C++ vs Python Resource Management
------------------------------------

+--------------------+-------------------------------+-------------------------------+
| Scenario           | C++                           | Python                        |
+====================+===============================+===============================+
| File handle        | ``RAII + std::fstream``        | ``with open(path) as f:``     |
+--------------------+-------------------------------+-------------------------------+
| Mutex              | ``std::lock_guard``            | ``with threading.Lock():``    |
+--------------------+-------------------------------+-------------------------------+
| Timer              | ``ScopedTimer`` destructor     | ``with Timer() as t:``        |
+--------------------+-------------------------------+-------------------------------+
| DB transaction     | RAII + destructor              | ``with Transaction() as tx:`` |
+--------------------+-------------------------------+-------------------------------+
| Multiple resources | Scope order                   | ``ExitStack``                 |
+--------------------+-------------------------------+-------------------------------+


Self-Check Questions
--------------------

**Q1: What is the execution order in a** ``with`` **block?**

1. ``__enter__`` is called; its return value is bound to the ``as`` variable.
2. The body of the ``with`` block executes.
3. ``__exit__`` is called — always, whether the block exits normally or raises.

**Q2: How do you suppress an exception in** ``__exit__``**?**

Return a truthy value (e.g., ``True`` or ``1``) from ``__exit__``.  Python
treats this as "the exception has been handled" and does not propagate it.
The ``with`` statement completes normally.

**Q3: What is the difference between class-based and** ``@contextmanager`` **forms?**

Both are equivalent in capability.  The class form is better when the context
manager needs to store state (reusable, introspectable).  The generator form
is more concise for one-off managers.  Use whatever reads more clearly.

**Q4: Why shouldn't you rely on** ``__del__`` **for resource cleanup in Python?**

Python's garbage collector may delay calling ``__del__`` (due to reference
cycles, ``gc`` module, or interpreter shutdown order).  ``__del__`` is not
guaranteed to run promptly or at all.  Always use ``with`` for deterministic
cleanup.
