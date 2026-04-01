Day 08 — Advanced OOP Patterns
================================

Operator Overloading
---------------------

Python uses dunder methods for operator overloading.  Return ``NotImplemented``
(not ``False``) when the types are incompatible — Python will then try the
reversed operation:

.. code-block:: python

    class Vector2D:
        def __add__(self, other):
            if not isinstance(other, Vector2D): return NotImplemented
            return Vector2D(self.x + other.x, self.y + other.y)

        def __rmul__(self, scalar):   # 2 * v calls v.__rmul__(2)
            return self.__mul__(scalar)

Common dunder operators: ``__add__``, ``__sub__``, ``__mul__``, ``__truediv__``,
``__neg__``, ``__abs__``, ``__lt__``, ``__le__``, ``__eq__``, ``__len__``,
``__contains__``, ``__getitem__``, ``__iter__``, ``__matmul__`` (``@``).


__slots__ for Memory Optimisation
-----------------------------------

.. code-block:: python

    class Point:
        __slots__ = ("x", "y")   # no __dict__ — fixed attribute set

        def __init__(self, x, y):
            self.x = x
            self.y = y

- ~30% less memory per instance (no ``__dict__``)
- Slightly faster attribute access
- Prevents adding new attributes (raises ``AttributeError``)
- Cannot use ``__weakref__`` unless added to ``__slots__``


__getattr__ vs __getattribute__
----------------------------------

.. code-block:: python

    class Proxy:
        def __getattr__(self, name):
            # Called ONLY when normal lookup fails
            # Safe: no infinite recursion risk
            return getattr(self._wrapped, name)

        def __getattribute__(self, name):
            # Called for EVERY attribute access — including self._wrapped!
            # Dangerous: self._x causes another __getattribute__ call → recursion
            # Must use: object.__getattribute__(self, name) for own attributes

**Rule:** Use ``__getattr__`` for proxy/fallback patterns.  Avoid
``__getattribute__`` unless you truly need to intercept every access.


__setattr__ — Intercepting All Assignments
--------------------------------------------

.. code-block:: python

    class ReadOnly:
        def __setattr__(self, name, value):
            if hasattr(self, name):
                raise AttributeError(f"{name} is read-only")
            super().__setattr__(name, value)

Call ``super().__setattr__()`` or ``object.__setattr__(self, name, value)``
to actually set the attribute — otherwise you get infinite recursion.


__init_subclass__ — Subclass Hooks
-------------------------------------

.. code-block:: python

    class PluginBase:
        _registry = {}

        def __init_subclass__(cls, plugin_name=None, **kwargs):
            super().__init_subclass__(**kwargs)
            name = plugin_name or cls.__name__
            PluginBase._registry[name] = cls

    class JsonPlugin(PluginBase, plugin_name="json"):
        pass

    PluginBase._registry   # {"json": JsonPlugin}

Called automatically when a subclass is defined.  Useful for auto-registration
patterns (plugins, serializers, validators).


__call__ — Callable Objects
-----------------------------

.. code-block:: python

    class Multiplier:
        def __init__(self, factor):
            self.factor = factor

        def __call__(self, value):
            return value * self.factor

    triple = Multiplier(3)
    triple(7)   # 21 — called like a function but has state

Use callable objects when you need a function-like interface with persistent
state (alternative to closures with ``nonlocal``).
