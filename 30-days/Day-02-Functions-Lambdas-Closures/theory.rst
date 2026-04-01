Day 02 — Functions, Lambdas, and Closures
==========================================

Why This Day Matters
--------------------

Functions are the primary unit of abstraction in Python. Understanding how
arguments are passed, how closures capture variables, and how to use
higher-order functions enables expressive, composable code.


Parameter Passing: Python vs C++
----------------------------------

Python uses **pass-by-object-reference** (sometimes called "pass-by-assignment"):

- Immutable objects (int, str, tuple): behave like pass-by-value (rebinding
  the parameter doesn't affect the caller).
- Mutable objects (list, dict): the caller's object is modified in-place.

.. code-block:: python

    def modify(lst: list[int]) -> None:
        lst.append(99)   # modifies caller's list

    def rebind(x: int) -> None:
        x = 100   # only affects local name; caller's int is unchanged

C++ has explicit value/reference/pointer semantics.  Python's model is
equivalent to C++ pass-by-pointer where the pointer itself is passed by value.


Parameter Kinds (Python 3.8+)
-------------------------------

.. code-block:: python

    def f(pos_only, /, normal, *args, kw_only, **kwargs):
        ...

+-------------------+-------------------------------------+
| Kind              | Syntax                              |
+===================+=====================================+
| Positional-only   | Before ``/``                        |
+-------------------+-------------------------------------+
| Normal            | Between ``/`` and ``*``             |
+-------------------+-------------------------------------+
| Variadic positional| ``*args`` — tuple                  |
+-------------------+-------------------------------------+
| Keyword-only      | After ``*`` or ``*args``            |
+-------------------+-------------------------------------+
| Variadic keyword  | ``**kwargs`` — dict                 |
+-------------------+-------------------------------------+


Mutable Default Argument Gotcha
---------------------------------

.. code-block:: python

    # BAD: list created ONCE at function definition
    def append(item, lst=[]):
        lst.append(item)
        return lst

    # GOOD: use None sentinel
    def append(item, lst=None):
        if lst is None:
            lst = []
        lst.append(item)
        return lst

Default arguments are evaluated when the ``def`` statement executes, not on
each call.  Mutable defaults persist between calls — a common bug.


First-Class Functions
---------------------

.. code-block:: python

    def apply(f, x):
        return f(x)

    apply(str.upper, "hello")   # "HELLO"
    apply(abs, -5)              # 5

Functions are objects in Python.  They can be stored in variables, passed as
arguments, returned from other functions, and stored in data structures.


Lambda Expressions
-------------------

.. code-block:: python

    # Use for short, obvious, one-use callables
    sorted(data, key=lambda d: d["age"])

    # Use def for everything else
    def meaningful_name(x: int) -> int:
        return x * 2 + 1

Lambda limitations:
- Single expression only (no ``if/else`` statements, no ``for``)
- Cannot contain type annotations
- No docstring support


Closures and nonlocal
----------------------

.. code-block:: python

    def make_adder(n: int):
        def adder(x: int) -> int:
            return x + n    # n captured from enclosing scope
        return adder

    add5 = make_adder(5)
    add5(3)   # 8 — n=5 is "closed over"

To modify a captured variable, declare it ``nonlocal``:

.. code-block:: python

    def make_counter():
        count = 0
        def increment():
            nonlocal count
            count += 1
            return count
        return increment

**Late-binding gotcha:**

.. code-block:: python

    # All closures capture the SAME variable i
    funcs = [lambda: i for i in range(3)]
    [f() for f in funcs]   # [2, 2, 2] — all see the final value of i

    # Fix: capture by default argument
    funcs = [(lambda i=i: i) for i in range(3)]
    [f() for f in funcs]   # [0, 1, 2]


map, filter, reduce vs Comprehensions
---------------------------------------

.. code-block:: python

    nums = [1, 2, 3, 4, 5]

    # map / filter — functional style
    squares = list(map(lambda x: x*x, nums))
    evens   = list(filter(lambda x: x%2==0, nums))

    # Comprehensions — usually clearer
    squares = [x*x for x in nums]
    evens   = [x for x in nums if x % 2 == 0]

    # reduce — use only for actual left-fold operations
    from functools import reduce
    product = reduce(lambda a,b: a*b, nums)  # 120

Prefer comprehensions for map/filter; use ``reduce`` only when no built-in
(``sum``, ``max``, ``any``, ``all``) applies.


functools.partial
------------------

.. code-block:: python

    import functools

    def power(base, exp):
        return base ** exp

    square = functools.partial(power, exp=2)
    square(5)   # 25


Self-Check Questions
--------------------

**Q1: What is the difference between** ``*args`` **and** ``**kwargs``**?**

``*args`` collects extra positional arguments into a tuple; ``**kwargs``
collects extra keyword arguments into a dict.  They allow functions to accept
a variable number of arguments without explicitly naming each one.

**Q2: What is a closure and what is the "late-binding gotcha"?**

A closure is a function that captures variables from its enclosing scope.
The late-binding gotcha: closures capture the *variable*, not its value at
creation time.  In a loop, all closures in the same loop body share the same
loop variable, so they all see the final value.  Fix: bind the current value
as a default argument.

**Q3: When should you use** ``lambda`` **vs** ``def``**?**

Use ``lambda`` for short, obvious, anonymous callables used inline (sort
keys, simple predicates).  Use ``def`` for anything that needs a docstring,
spans multiple expressions, has complex logic, or will be reused.

**Q4: What is** ``functools.partial`` **and when is it useful?**

``partial`` creates a new callable with some arguments of the original
function pre-filled.  It is useful when you need to pass a function as a
callback but the callback interface accepts fewer parameters than the
function you want to call.
