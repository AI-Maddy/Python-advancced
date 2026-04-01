Day 14 — Descriptors and Properties
======================================

Descriptor Protocol
--------------------
.. code-block:: python

    class MyDescriptor:
        def __set_name__(self, owner, name):
            self._name = name          # called when assigned to class

        def __get__(self, obj, objtype):
            if obj is None: return self
            return obj.__dict__.get(self._name)

        def __set__(self, obj, value):
            obj.__dict__[self._name] = value

        def __delete__(self, obj):
            del obj.__dict__[self._name]

Data vs Non-Data Descriptors
-----------------------------
- **Data descriptor**: defines ``__set__`` or ``__delete__`` — takes priority over instance dict
- **Non-data descriptor**: only ``__get__`` — instance dict takes priority (used for ``LazyProperty``)

property Is a Descriptor
-------------------------
.. code-block:: python

    # These are identical:
    @property
    def radius(self): return self._radius

    radius = property(fget=lambda self: self._radius)

__set_name__
------------
Called when the descriptor is assigned in a class body.  Gives the descriptor
access to its own attribute name without requiring it to be passed manually.

Lazy Property Pattern
----------------------
.. code-block:: python

    class LazyProperty:
        def __get__(self, obj, objtype):
            if obj is None: return self
            value = self._func(obj)
            obj.__dict__[self._name] = value  # cache in instance dict
            return value                       # future access bypasses descriptor
