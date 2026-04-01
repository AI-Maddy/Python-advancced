Day 28 — Code Review: Common Python Pitfalls
=============================================

Pitfall 1: Mutable Default Argument
-------------------------------------

Default argument objects are created **once at definition time**, not on each call.

.. code-block:: python

    # BAD
    def f(lst=[]):       # same list object reused every call!
        lst.append(1)
        return lst

    # FIX
    def f(lst=None):
        if lst is None:
            lst = []
        lst.append(1)
        return lst

Pitfall 2: Late Binding Closure
----------------------------------

Lambda/closures capture the **variable**, not its value at creation time.

.. code-block:: python

    fns = [lambda: i for i in range(5)]   # all return 4
    fns = [lambda i=i: i for i in range(5)]  # fixed: capture value

Pitfall 3: ``is`` vs ``==``
-----------------------------

``is`` tests **identity** (same object in memory).
``==`` tests **equality** (same value).

.. code-block:: python

    s = "hello"
    s is "hello"   # True only due to string interning — unreliable
    s == "hello"   # Always correct

Pitfall 4: Shadowing Builtins
-------------------------------

Assigning to ``list``, ``type``, ``id``, ``sum``, ``input``, etc. replaces
the built-in for the rest of the scope.

.. code-block:: python

    list = [1, 2, 3]   # now list() is gone!
    list([4, 5])        # TypeError

Use descriptive variable names instead.

Pitfall 5: Bare ``except:``
-----------------------------

Bare ``except:`` catches **everything**: ``SystemExit``, ``KeyboardInterrupt``,
``MemoryError`` — you can't Ctrl-C out of it.

.. code-block:: python

    # BAD
    try: ...
    except: ...

    # FIX
    try: ...
    except (ValueError, TypeError) as e: ...

Pitfall 6: Modifying List During Iteration
--------------------------------------------

Removing items from a list while iterating skips the element after each
removed item (internal index advances past it).

.. code-block:: python

    # BAD: skips elements
    for n in lst:
        if pred(n):
            lst.remove(n)

    # FIX 1: iterate copy
    for n in lst[:]:
        if pred(n):
            lst.remove(n)

    # FIX 2: list comprehension (clearest)
    lst = [n for n in lst if not pred(n)]

Pitfall 7: Missing ``super().__init__()``
-------------------------------------------

In multiple inheritance, always use ``super().__init__(**kwargs)`` and pass
keyword args cooperatively so the MRO chain calls all ``__init__`` methods.

Pitfall 8: Overusing isinstance
---------------------------------

``isinstance`` breaks duck typing.  Prefer ``hasattr`` checks or just let
the ``TypeError`` propagate naturally.

Pitfall 9: Missing ``__all__``
--------------------------------

Without ``__all__``, ``from module import *`` exports everything, including
all imported names (``from os import path`` becomes visible to importers).

Pitfall 10: I/O in ``__init__``
----------------------------------

``__init__`` should be a lightweight constructor.  Keep network connections,
file reads, and database queries out.  Use lazy initialization or factory
methods:

.. code-block:: python

    class Service:
        def __init__(self, url: str) -> None:
            self.url = url
            self._conn = None   # not connected yet

        def connect(self) -> None:
            self._conn = create_connection(self.url)
