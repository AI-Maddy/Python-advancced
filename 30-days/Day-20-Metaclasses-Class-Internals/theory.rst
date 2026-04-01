Day 20 — Metaclasses & Class Internals
========================================

Classes Are Objects
--------------------

Every class is an instance of ``type`` (or a subclass of ``type``).

.. code-block:: python

    class Foo: pass
    type(Foo)      # <class 'type'>
    type(Foo())    # <class '__main__.Foo'>

    # Equivalent dynamic creation:
    Foo = type("Foo", (object,), {"x": 10})

Metaclass Creation Order
-------------------------

When Python processes ``class Body(Base, metaclass=Meta):``:

1. ``Meta.__prepare__(name, bases)`` → returns namespace dict (default: ``{}``)
2. Class body executes, populating the namespace.
3. ``Meta.__new__(mcs, name, bases, namespace)`` → creates and returns the class object.
4. ``Meta.__init__(cls, name, bases, namespace)`` → initialises the class object.

``__prepare__``
---------------

Return an ``OrderedDict`` (or custom mapping) to capture definition order.

.. code-block:: python

    class OrderedMeta(type):
        @classmethod
        def __prepare__(mcs, name, bases, **kw):
            return OrderedDict()

        def __new__(mcs, name, bases, ns, **kw):
            cls = super().__new__(mcs, name, bases, dict(ns))
            cls._field_order = [k for k in ns if not k.startswith("__")]
            return cls

SingletonMeta
-------------

.. code-block:: python

    class SingletonMeta(type):
        _instances: ClassVar[dict] = {}
        def __call__(cls, *a, **kw):
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*a, **kw)
            return cls._instances[cls]

RegistryMeta
------------

.. code-block:: python

    class RegistryMeta(type):
        def __init__(cls, name, bases, ns):
            super().__init__(name, bases, ns)
            if not hasattr(cls, "_registry"):
                cls._registry = {}
            elif not name.startswith("_"):
                cls._registry[name] = cls

``__init_subclass__`` — Lightweight Alternative
-------------------------------------------------

For most use cases, prefer ``__init_subclass__`` over metaclasses:

.. code-block:: python

    class Base:
        _registry = {}
        def __init_subclass__(cls, name="", **kw):
            super().__init_subclass__(**kw)
            if name:
                Base._registry[name] = cls

    class MyPlugin(Base, name="my"): ...

Introspection Tools
--------------------

.. list-table::
   :header-rows: 1

   * - Function
     - Returns
   * - ``vars(obj)``
     - ``obj.__dict__`` (instance/class dict)
   * - ``dir(obj)``
     - All accessible names including inherited
   * - ``getattr(obj, "x", default)``
     - Attribute value or default
   * - ``setattr(obj, "x", val)``
     - Sets attribute dynamically
   * - ``hasattr(obj, "x")``
     - True/False
   * - ``type(obj)``
     - Class of obj
   * - ``isinstance(obj, T)``
     - Subclass-aware type check

When to Use Metaclasses
------------------------

* Framework-level code (ORMs, serialisers, plugin registries).
* Enforcing class invariants at *definition* time (not runtime).
* Usually prefer ``__init_subclass__`` — simpler and equally powerful.
